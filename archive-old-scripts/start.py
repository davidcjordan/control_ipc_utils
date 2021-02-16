#!/usr/bin/env python3

"""
Does the following:
 - configures mode and parameters (level, speed, etc)
 - sends the start message
 - checks for Active

 returns 0 on pass; 1 on failure
"""
from ctrl_messaging_routines import send_msg, is_active
from control_ipc_defines import PUT_METHOD, STRT_RSRC, MODE_RSRC, OPTS_RSRC, \
   LEVEL_MIN, LEVEL_MAX, LEVEL_DEFAULT, \
   DELAY_MIN, DELAY_MAX, DELAY_DEFAULT, \
   SPEED_MIN, SPEED_MAX, SPEED_DEFAULT, \
   HEIGHT_MIN, HEIGHT_MAX, HEIGHT_DEFAULT, \
   MODE_PARAM, ID_PARAM, STEP_PARAM, TIEBREAKER_PARAM, \
   LEVEL_PARAM, SPEED_PARAM, DELAY_PARAM, HEIGHT_PARAM 

import argparse
import logging
import sys

if __name__ == '__main__':
   shell_rc = 1

   parser = argparse.ArgumentParser(description='Start boomer')
   parser.add_argument('-m', '--mode', dest='mode_setting', \
         type=int, choices=range(1, 4), default=1, nargs='?', \
         )
   parser.add_argument('-l', '--level', dest='level_setting', \
         type=int, default=LEVEL_DEFAULT, nargs='?', \
         help='player skill level; range 10 to 70')
         # choices=range(LEVEL_MIN, LEVEL_MAX+1), <- removed because it enumerated the range
   parser.add_argument('-t', '--tiebreaker', dest='tiebreaker_setting', \
         type=int, choices=range(0, 2), default=0, nargs='?', \
         help='defaults to game mode')
   parser.add_argument('-s', '--speed', dest='speed_setting', \
         type=int, default=SPEED_DEFAULT, nargs='?', \
         help='percent to increase/decrease ball speed: 80 to 100')
         # choices=range(SPEED_MIN, SPEED_MAX+1),
   parser.add_argument('-H', '--height', dest='height_setting', \
         type=int, default=HEIGHT_DEFAULT, nargs='?', \
         help='number of 1/2 degrees to change height of the ball throw; range -32 to 32')
         #choices=range(HEIGHT_MIN, HEIGHT_MAX+1),
   parser.add_argument('-d', '--delay', dest='delay_setting', \
         type=int, default=DELAY_DEFAULT, nargs='?', \
         help='milliseoncds of delay the next ball; range -2000 to 2000')
         # choices=range(DELAY_MIN, DELAY_MAX+1), 
   parser.add_argument('-n', '--drill_id', dest='drill_id_setting', \
         type=int,  default=0, nargs='?', \
         help='drill number; range 0-999')
         # choices=range(0, 1000),
   args = parser.parse_args()
   # print("called with {}: ".format(sys.argv[0]))
   # print("mode: {}  level: {}  doubles: {}  tiebreaker: {}".format(args.mode_setting,\
   #     args.level_setting, args.doubles_setting, args.tiebreaker_setting))


   if args.speed_setting < SPEED_MIN or args.speed_setting > SPEED_MAX:
      print("speed not between {} and {}".format(SPEED_MIN, SPEED_MAX))
      sys.exit(1)
   if args.height_setting < HEIGHT_MIN or args.height_setting > HEIGHT_MAX:
      print("height not between {} and {}".format(HEIGHT_MIN, HEIGHT_MAX))
      sys.exit(1)
   if args.delay_setting < DELAY_MIN or args.delay_setting > DELAY_MAX:
      print("delay not between {} and {}".format(DELAY_MIN, DELAY_MAX))
      sys.exit(1)
   if args.drill_id_setting < 0 or args.drill_id_setting > 999:
      print("drill_id not between 0 and 999")
      sys.exit(1)
   if args.level_setting < LEVEL_MIN or args.level_setting > LEVEL_MAX:
      print("level not between {} and {}".format(LEVEL_MIN, LEVEL_MAX))
      sys.exit(1)

   active = is_active()
   if (type(active) is not bool):
      logging.error("GET Status failed")
      sys.exit(1)
   if active:
      logging.error("Base already active")
      sys.exit(1)


   mode = {MODE_PARAM: args.mode_setting, \
      ID_PARAM: args.drill_id_setting, \
      TIEBREAKER_PARAM: args.tiebreaker_setting}
   rc, code = send_msg(PUT_METHOD, MODE_RSRC, mode)
   if not rc:
      logging.error("PUT Mode failed, code: {}".format(code))
      sys.exit(1)

   params = {LEVEL_PARAM: args.level_setting, \
         SPEED_PARAM: args.speed_setting, \
         HEIGHT_PARAM: args.height_setting, \
         DELAY_PARAM: args.delay_setting}
   rc, code = send_msg(PUT_METHOD, OPTS_RSRC, params)
   if not rc:
      logging.error("PUT PARAMS failed, code: {}".format(code))
      sys.exit(1)

   # start and check for active
   rc, code = send_msg(PUT_METHOD, STRT_RSRC)
   if not rc:
      logging.error("PUT START failed, code: {}".format(code))
      sys.exit(1)
   active = is_active()
   if (type(active) is not bool):
      logging.error("GET Status failed")
      sys.exit(1)
   if not active:
      logging.error("Base didn't go active after start command")
      sys.exit(1)