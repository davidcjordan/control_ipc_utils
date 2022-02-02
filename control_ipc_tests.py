#!/usr/bin/env python3

from ctrl_messaging_routines import send_msg, is_active
from control_ipc_defines import GAME_MODE_E, DRILL_MODE_E, \
   MODE_RSRC, STAT_RSRC, STRT_RSRC, STOP_RSRC, OPTS_RSRC, \
   GET_METHOD, PUT_METHOD
from control_ipc_defines import LEVEL_DEFAULT, SPEED_DEFAULT, DELAY_DEFAULT, HEIGHT_DEFAULT
from control_ipc_defines import LEVEL_MIN, SPEED_MIN, DELAY_MIN, HEIGHT_MIN
from control_ipc_defines import LEVEL_MAX, SPEED_MAX, DELAY_MAX, HEIGHT_MAX
import logging
import sys

logger = logging.getLogger(__name__)
# log_format = ('[%(asctime)s] %(levelname)-6s %(name)-12s %(message)s')
log_format = ('[%(asctime)s] %(levelname)-6s %(message)s')

logging.basicConfig(
    level=logging.DEBUG,
   #  level=logging.INFO,
    format=log_format,
    # filename=('debug.log'),
)

# logging.info("status: {}".format(send_msg(GET_METHOD, STATUS)))

# mode_default = {'mode': 1, 'drill_workout_id': 0, 'drill_step': 0} #, 'iterations': 0}
mode_default = {'mode': 1, 'id': 0, 'step': 0, 'tiebreaker': 0}
params_default = {'level': LEVEL_DEFAULT, 'speed': SPEED_DEFAULT, 'height': HEIGHT_DEFAULT, 'delay': DELAY_DEFAULT}
params_pattern1 = {'level': LEVEL_MAX, 'speed': SPEED_MIN, 'height': HEIGHT_MAX, 'delay': DELAY_MIN, \
   "wServes":2,"reduceRun":0,"ptDelay":1,"grunts":0}
params_pattern2 = {'level': LEVEL_MIN, 'speed': SPEED_MAX, 'height': HEIGHT_MIN, 'delay': DELAY_MAX, \
   "wServes":1,"reduceRun":1,"ptDelay":-2,"grunts":1}
params_patterns = [params_pattern1, params_pattern2]

def run_tests():
   # print("Game test result: {}".format(test_game(tie_breaker=True)))
   # print("Game test result: {}".format(test_game(tie_breaker=False)))
   # print("Drill test result: {}".format(test_drill(drill_id=39)))
   # print("Mode test result: {}".format(test_register(MODE_RSRC, mode_default)))
   print("Params test result: {}".format(test_register(OPTS_RSRC, params_patterns)))


def test_game(tie_breaker=False):
   # sets mode, params; starts game; stops game
   test_rc = True
   active = is_active()
   if (type(active) is not bool):
      return False
   if active:
      print("Base is already active")
      return False

   int_tiebreaker = int(tie_breaker == True)

   mode = {'mode': GAME_MODE_E, 'tie_breaker': int_tiebreaker}
   rc, code = send_msg(PUT_METHOD, MODE_RSRC, mode)
   if not rc:
      logging.error("test_game: initial PUT mode failed, code: {}".format(code))
      return False

   # start and check for active
   rc, code = send_msg(PUT_METHOD, STRT_RSRC)
   if not rc:
      logging.error("test_game: PUT START failed, code: {}".format(code))
      return False
   active = is_active()
   if (type(active) is not bool):
      return False
   if not active:
      logging.error("Base didn't go active after start command")
      test_rc = False

   # stop and check for inactive
   rc, code = send_msg(PUT_METHOD, STOP_RSRC)
   if not rc:
      logging.error("test_game: PUT STOP failed, code: {}".format(code))
      return False
   active = is_active()
   if (type(active) is not bool):
      return False
   if active:
      logging.error("Base didn't go inactive after stop command")
      test_rc = False

   # check mode for doubles, tieb_break
   rc, register = send_msg(GET_METHOD, MODE_RSRC)
   if not rc:
      logging.error("test_game: final GET mode failed")
      return False
   if (register is not None):
      if register['mode'] != str(GAME_MODE_E):
         logging.error("test_game: mode check failed, expected: {}, got {}:".format(GAME_MODE_E, register['mode']))
         test_rc = False
      if (('tie_breaker' in register) and (register['tie_breaker'] != str(int_tiebreaker))):
         logging.error("test_game: tiebreaker check failed, expected: {}, got {}:".format(int_tiebreaker, register['tie_breaker']))
         test_rc = False
   
   return test_rc

def test_drill(drill_id=39):
   # sets mode, params; starts drill; stops drill
   test_rc = True
   active = is_active()
   if (type(active) is not bool):
      return False
   if active:
      print("Base is already active")
      return False

   mode = {'mode': DRILL_MODE_E, 'id': drill_id}
   rc, code = send_msg(PUT_METHOD, MODE_RSRC, mode)
   if not rc:
      logging.error("test_drill: initial PUT mode failed, code: {}".format(code))
      return False

   # start and check for active
   rc, code = send_msg(PUT_METHOD, STRT_RSRC)
   if not rc:
      logging.error("test_drill: PUT START failed, code: {}".format(code))
      return False
   active = is_active()
   if (type(active) is not bool):
      return False
   if not active:
      logging.error("Base didn't go active after start command")
      test_rc = False

   # stop and check for inactive
   rc, code = send_msg(PUT_METHOD, STOP_RSRC)
   if not rc:
      logging.error("test drill: PUT STOP failed, code: {}".format(code))
      return False
   active = is_active()
   if (type(active) is not bool):
      return False
   if active:
      logging.error("Base didn't go inactive after stop command")
      test_rc = False

   return test_rc


def test_register(register_under_test, patterns):
   test_pattern = {}
   read_back_compare = True
   msg_ok, register_original = send_msg(GET_METHOD, register_under_test)
   if not msg_ok:
      logging.error("GET {} failed.".format(register_under_test))
      return False
   #  if len(register_original) == 0:
   #      register_original = default_values
   logging.debug(f"register before test: {register_original}")

   for pattern in patterns:
      logging.debug(f"Setting {register_under_test} to: {pattern}")
      if send_msg(PUT_METHOD, register_under_test, pattern) == False:
         logging.error(f"PUT {register_under_test} failed")
         read_back_compare = False
         break
      msg_ok, reg_read_back = send_msg(GET_METHOD, register_under_test)
      if not msg_ok:
         logging.error(f"GET {register_under_test} failed.")
         read_back_compare = False
         break
      for key in pattern:
         if reg_read_back[key] != pattern[key]:
               logging.error(f"{register_under_test}: read: {pattern} not equal to values written: {reg_read_back}")
               read_back_compare = False
               break
      if not read_back_compare:
         break

   #restore 
   if (send_msg(PUT_METHOD, register_under_test, register_original) == False):
      logging.error(f"restore {register_under_test} failed")
   logging.info(f"Register test done: {register_under_test} restored to: {register_original}")
   return(read_back_compare)

if __name__ == "__main__":
    run_tests()
