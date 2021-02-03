#!/usr/bin/env python3

from ctrl_messaging_routines import send_msg, is_active
from control_ipc_defines import GAME_MODE_E, DRILL_MODE_E, \
   MODE_RSRC, STAT_RSRC, STRT_RSRC, STOP_RSRC, \
   GET_METHOD, PUT_METHOD
import logging
import sys

logger = logging.getLogger(__name__)
# log_format = ('[%(asctime)s] %(levelname)-6s %(name)-12s %(message)s')
log_format = ('[%(asctime)s] %(levelname)-6s %(message)s')

logging.basicConfig(
    level=logging.DEBUG,
    # level=logging.INFO,
    format=log_format,
    # filename=('debug.log'),
)

# logging.info("status: {}".format(send_msg(GET_METHOD, STATUS)))

# mode_default = {'mode': 1, 'drill_workout_id': 0, 'drill_step': 0} #, 'iterations': 0}
mode_default = {'mode': 1, 'id': 0, 'step': 0, 'doubles': 0, 'tiebreaker': 0}
params_default = {'level': 2, 'speed': 100, 'height': 0, 'delay': 0}
cam_test = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':5, 'g':7, 'h':8, 'i':9, 'j':10, 'k':11, 'l':12, 'm':13, 'n':1014}

def run_tests():
   # print("Game test result: {}\n".format(test_game(doubles=False, tie_breaker=True)))
   # print("Game test result: {}\n".format(test_game(doubles=True, tie_breaker=False)))
   print("Drill test result: {}\n".format(test_drill(drill_id=39)))
   # print("Mode test result: {}\n".format(test_register(RSRC_MODE, mode_default)))
   # print("Params test result: {}\n".format(test_register(RSRS_LDSH, params_default)))


def test_game(doubles=False, tie_breaker=False):
   # sets mode, params; starts game; stops game
   test_rc = True
   active = is_active()
   if (type(active) is not bool):
      return False
   if active:
      print("Base is already active")
      return False

   int_doubles = int(doubles == True)
   int_tiebreaker = int(tie_breaker == True)

   mode = {'mode': GAME_MODE_E, 'doubles': int_doubles, 'tie_breaker': int_tiebreaker}
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
      if (('doubles' in register) and (register['doubles'] != str(int_doubles))):
         logging.error("test_game: doubles check failed, expected: {}, got {}:".format(int_doubles, register['doubles']))
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


def test_register(register_under_test, default_values):
    test_pattern = {}
    read_back_compare = True
    msg_ok, register_original = send_msg(GET_METHOD, register_under_test)
    if not msg_ok:
        logging.error("GET {} failed.".format(register_under_test))
        return False
   #  if len(register_original) == 0:
   #      register_original = default_values
    full_dict = default_values
    logging.debug("register before test: {}".format(register_original))
    for i in range(len(full_dict)):
        j = 0
        for key in full_dict:
            if j == i:
                test_pattern[key] = 1
            else:
                test_pattern[key] = 2
            j += 1
        logging.debug("Setting {} to: {}".format(register_under_test, test_pattern))
        if send_msg(PUT_METHOD, register_under_test, test_pattern) == False:
            logging.error("PUT {} failed".format(register_under_test))
            break
        msg_ok, reg_read_back = send_msg(GET_METHOD, register_under_test)
        if not msg_ok:
            logging.error("GET {} failed.".format(register_under_test))
            return False
        for key in full_dict:
            if reg_read_back[key] != test_pattern[key]:
                logging.error("{}: read: {} not equal to mode write: {}".format(register_under_test,test_pattern, reg_read_back))
                read_back_compare = False
                break
        if not read_back_compare:
            break
    #restore 
    if (send_msg(PUT_METHOD, register_under_test, register_original) == False):
        logging.error("restore {} failed".format(register_under_test))
    logging.info("Register test done: {} restored to: {}".format(register_under_test, register_original))
    return(read_back_compare)

if __name__ == "__main__":
    run_tests()
