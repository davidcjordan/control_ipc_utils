#!/usr/bin/env python3

from ctrl_messaging_routines import send_msg, is_state
# from control_ipc_defines import GET_METHOD, PUT_METHOD, \
#    MODE_RSRC, STAT_RSRC, STRT_RSRC, STOP_RSRC, BCFG_RSRC, DCFG_RSRC, GCFG_RSRC
# from control_ipc_defines import base_mode_e
# from control_ipc_defines import LEVEL_MIN, SPEED_MOD_MIN, DELAY_MOD_MIN, ELEVATION_ANGLE_MOD_MIN
# from control_ipc_defines import LEVEL_MAX, SPEED_MOD_MAX, DELAY_MOD_MAX, ELEVATION_ANGLE_MOD_MAX
from control_ipc_defines import *
import logging
import sys

logger = logging.getLogger(__name__)
# log_format = ('[%(asctime)s] %(levelname)-6s %(name)-12s %(message)s')
log_format = ('[%(asctime)s] %(levelname)-6s %(message)s')

logging.basicConfig(
   #  level=logging.DEBUG,
    level=logging.INFO,
    format=log_format,
    # filename=('debug.log'),
)

mode_test_patterns= []
mode_test_patterns.append({f'{MODE_PARAM}': base_mode_e.WORKOUT.value, f'{ID_PARAM}': 22, f'{STEP_PARAM}': 2})
mode_test_patterns.append({f'{MODE_PARAM}': base_mode_e.GAME.value, f'{ID_PARAM}': 100, f'{STEP_PARAM}': 1})

base_cfg_test_patterns= []
base_cfg_test_patterns.append({f'{LEVEL_PARAM}': LEVEL_MAX, f'{GRUNTS_PARAM}': 0, f'{TRASHT_PARAM}': 1})
base_cfg_test_patterns.append({f'{LEVEL_PARAM}': 30, f'{GRUNTS_PARAM}': 1, f'{TRASHT_PARAM}': 0})

game_cfg_test_patterns= []
game_cfg_test_patterns.append({f'{SERVE_MODE_PARAM}': serve_mode_e.BOOMER_ALL_SERVES.value, \
   f'{POINTS_DELAY_PARAM}': 1.5, f'{TIEBREAKER_PARAM}': 1})

drill_cfg_test_patterns= []
drill_cfg_test_patterns.append({f'{SPEED_MOD_PARAM}': SPEED_MOD_MAX, \
   f'{ELEVATION_MOD_PARAM}': ELEVATION_ANGLE_MOD_MIN, f'{DELAY_MOD_PARAM}': DELAY_MOD_MAX})
drill_cfg_test_patterns.append({f'{SPEED_MOD_PARAM}': SPEED_MOD_MIN, \
   f'{ELEVATION_MOD_PARAM}': ELEVATION_ANGLE_MOD_MAX, f'{DELAY_MOD_PARAM}': DELAY_MOD_MIN})

def run_tests():
   print("Mode test result: {}".format(test_register(MODE_RSRC, mode_test_patterns)))
   print("base config test result: {}".format(test_register(BCFG_RSRC, base_cfg_test_patterns)))
   print("game config test result: {}".format(test_register(GCFG_RSRC, game_cfg_test_patterns)))
   print("drill config test result: {}".format(test_register(DCFG_RSRC, drill_cfg_test_patterns)))
   # print("Drill test result: {}".format(test_drill(drill_id=39)))
   # print("Game test result: {}".format(test_game(tie_breaker=True)))

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

   mode = {'mode': GAME_MODE_E}
   rc, code = send_msg(PUT_METHOD, MODE_RSRC, mode, channel=CTRL_TRANSPRT)
   if not rc:
      logging.error("test_game: initial PUT mode failed, code: {}".format(code))
      return False

   # start and check for active
   rc, code = send_msg(PUT_METHOD, STRT_RSRC, channel=CTRL_TRANSPRT)
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
   rc, code = send_msg(PUT_METHOD, STOP_RSRC,channel=CTRL_TRANSPRT)
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
   rc, register = send_msg(GET_METHOD, MODE_RSRC, channel=CTRL_TRANSPRT)
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
   rc, code = send_msg(PUT_METHOD, MODE_RSRC, mode, channel=CTRL_TRANSPRT)
   if not rc:
      logging.error("test_drill: initial PUT mode failed, code: {}".format(code))
      return False

   # start and check for active
   rc, code = send_msg(PUT_METHOD, STRT_RSRC, channel=CTRL_TRANSPRT)
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
   rc, code = send_msg(PUT_METHOD, STOP_RSRC, channel=CTRL_TRANSPRT)
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
   msg_ok, register_original = send_msg(GET_METHOD, register_under_test, channel=CTRL_TRANSPRT)
   if not msg_ok:
      logging.error("GET {} failed.".format(register_under_test))
      return False
   #  if len(register_original) == 0:
   #      register_original = default_values
   logging.debug(f"register before test: {register_original}")

   for pattern in patterns:
      logging.debug(f"Setting {register_under_test} to: {pattern}")
      if send_msg(PUT_METHOD, register_under_test, pattern, channel=CTRL_TRANSPRT) == False:
         logging.error(f"PUT {register_under_test} failed")
         read_back_compare = False
         break
      msg_ok, reg_read_back = send_msg(GET_METHOD, register_under_test, channel=CTRL_TRANSPRT)
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
   if (send_msg(PUT_METHOD, register_under_test, register_original, channel=CTRL_TRANSPRT) == False):
      logging.error(f"restore {register_under_test} failed")
   logging.info(f"Register test done: {register_under_test} restored to: {register_original}")
   return(read_back_compare)

if __name__ == "__main__":
    run_tests()
