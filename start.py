#!/usr/bin/env python3

"""
Does the following:
 - configures mode and parameters (level, speed, etc)
 - sends the start message
 - checks for Active

 returns 0 on pass; 1 on failure
"""
from ctrl_messaging_routines import send_msg, is_active
# from control_ipc_defines import PUT_METHOD, STRT_RSRC, MODE_RSRC, LDSH_RSRC
from control_ipc_defines import PUT_METHOD, STRT_RSRC, MODE_RSRC, LDSH_RSRC, \
   LEVEL_MIN, LEVEL_MAX, LEVEL_DEFAULT, \
   DELAY_MIN, DELAY_MAX, DELAY_DEFAULT, \
   SPEED_MIN, SPEED_MAX, SPEED_DEFAULT, \
   HEIGHT_MIN, HEIGHT_MAX, HEIGHT_DEFAULT
import argparse
import logging
import sys

if __name__ == '__main__':
   shell_rc = 1

   parser = argparse.ArgumentParser(description='Start boomer')
   # parser.add_argument('on_off', type=int, nargs='?', choices=range(0, 8), default=0, \
   #                     help=': 0 for off; 1 for on; 2..7 to turn on for that many minutes')
   parser.add_argument('-m', '--mode', dest='mode_setting', \
         type=int, choices=range(1, 4), default=1, nargs='?', \
         help='mode: game=1, drill=2, more TBD')
   parser.add_argument('-l', '--level', dest='level_setting', \
         type=int, choices=range(LEVEL_MIN, LEVEL_MAX+1), default=LEVEL_DEFAULT, nargs='?', \
         help='player skill level')
   parser.add_argument('-d', '--doubles', dest='doubles_setting', \
         type=bool, default=False, nargs='?', \
         help='defaults to singles game mode')
   parser.add_argument('-t', '--tiebreaker', dest='tiebreaker_setting', \
         type=bool, default=False, nargs='?', \
         help='defaults to regular game mode')
   parser.add_argument('-s', '--speed', dest='speed_setting', \
         type=int, choices=range(SPEED_MIN, SPEED_MAX+1), default=SPEED_DEFAULT, nargs='?', \
         help='percentage to increase/decrease ball speed')
   parser.add_argument('-g', '--height', dest='height_setting', \
         type=int, choices=range(HEIGHT_MIN, HEIGHT_MAX+1), default=HEIGHT_DEFAULT, nargs='?', \
         help='number of degrees to increase or decrease (negative numbers) height')
   parser.add_argument('-e', '--delay', dest='delay_setting', \
         type=int, choices=range(DELAY_MIN, DELAY_MAX+1), default=DELAY_DEFAULT, nargs='?', \
         help='number of 0.1 seconds to delay the next ball, can be negative')
   parser.add_argument('-n', '--drill_id', dest='drill_id_setting', \
         type=int, choices=range(0, 1000), default=0, nargs='?', \
         help='drill number')
   args = parser.parse_args()
   # print("called with {}: ".format(sys.argv[0]))
   # print("mode: {}  level: {}  doubles: {}  tiebreaker: {}".format(args.mode_setting,\
   #     args.level_setting, args.doubles_setting, args.tiebreaker_setting))


   active = is_active()
   if (type(active) is not bool):
      logging.error("GET Status failed")
      sys.exit(1)
   if active:
      logging.error("Base already active")
      sys.exit(1)


   mode = {'mode': args.mode_setting, \
      'id': args.drill_id_setting, \
      'doubles': args.doubles_setting, \
      'tiebreak': args.tiebreaker_setting}
   rc, code = send_msg(PUT_METHOD, MODE_RSRC, mode)
   if not rc:
      logging.error("PUT Mode failed, code: {}".format(code))
      sys.exit(1)

   params = {'level': args.level_setting, \
         'speed': args.speed_setting, \
         'height': args.height_setting, \
         'delay': args.delay_setting}
   rc, code = send_msg(PUT_METHOD, LDSH_RSRC, params)
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