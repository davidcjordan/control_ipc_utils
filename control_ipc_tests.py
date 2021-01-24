#!/usr/bin/env python3

import ctrl_messaging_routines as cipc
# from ctrl_messaging_routines import *
import message_pb2 as mpb
import logging
import sys

logger = logging.getLogger(__name__)
# log_format = ('[%(asctime)s] %(levelname)-6s %(name)-12s %(message)s')
log_format = ('[%(asctime)s] %(levelname)-6s %(message)s')

logging.basicConfig(
    # level=logging.DEBUG,
    level=logging.INFO,
    format=log_format,
    # filename=('debug.log'),
)

# logging.info("status: {}".format(cipc.send_msg(cipc.GET, cipc.STATUS)))

mode_default = {'mode': 1, 'drill_workout_id': 0, 'drill_step': 0} #, 'iterations': 0}
params_default = {'level': 2, 'speed': 100, 'height': 0, 'delay': 0}

def run_tests():
   print("Game test result: {}\n".format(test_game(doubles=False, tie_breaker=True)))
   # print("Game test result: {}\n".format(test_game(doubles=True, tie_breaker=False)))
   print("Drill test result: {}\n".format(test_drill(drill_id=39)))
   # print("Mode test result: {}\n".format(test_register(cipc.MODE, mode_default)))
   # print("Params test result: {}\n".format(test_register(cipc.PARAMS, params_default)))


def test_game(doubles=False, tie_breaker=False):
   # sets mode, params; starts game; stops game
   test_rc = True
   active = cipc.is_active()
   if (type(active) is not bool):
      return False
   if active:
      print("Base is already active")
      return False

   int_doubles = int(doubles == True)
   int_tiebreaker = int(tie_breaker == True)

   mode = {'mode': mpb.GAME, 'doubles': int_doubles, 'tie_breaker': int_tiebreaker}
   rc, code = cipc.send_msg(cipc.PUT, cipc.MODE, mode)
   if not rc:
      logging.error("test_game: initial PUT mode failed, code: {}".format(code))
      return False

   # start and check for active
   rc, code = cipc.send_msg(cipc.PUT, cipc.START)
   if not rc:
      logging.error("test_game: PUT START failed, code: {}".format(code))
      return False
   active = cipc.is_active()
   if (type(active) is not bool):
      return False
   if not active:
      logging.error("Base didn't go active after start command")
      test_rc = False

   # stop and check for inactive
   rc, code = cipc.send_msg(cipc.PUT, cipc.STOP)
   if not rc:
      logging.error("test_game: PUT STOP failed, code: {}".format(code))
      return False
   active = cipc.is_active()
   if (type(active) is not bool):
      return False
   if active:
      logging.error("Base didn't go inactive after stop command")
      test_rc = False

   # check mode for doubles, tieb_break
   rc, register = cipc.send_msg(cipc.GET, cipc.MODE)
   if not rc:
      logging.error("test_game: final GET mode failed")
      return False
   if (register is not None):
      if register['mode'] != mpb.GAME:
         logging.error("test_game: mode check failed, expected: {}, got {}:".format(mpb.GAME, register['mode']))
         test_rc = False
      if ( (('doubles' not in register) and doubles) or \
           (('doubles' in register) and (register['doubles'] != int_doubles))):
         logging.error("test_game: mode check failed, expected: {}, got {}:".format(int_doubles, register['doubles']))
         test_rc = False
      if ( (('tie_breaker' not in register) and tie_breaker) or \
           (('tie_breaker' in register) and (register['tie_breaker'] != int_tiebreaker))):
         logging.error("test_game: mode check failed, expected: {}, got {}:".format(int_tiebreaker, register['tie_breaker']))
         test_rc = False
   
   return test_rc

def test_drill(drill_id=39):
   # sets mode, params; starts drill; stops drill
   test_rc = True
   active = cipc.is_active()
   if (type(active) is not bool):
      return False
   if active:
      print("Base is already active")
      return False

   mode = {'mode': mpb.DRILL, 'drill_workout_id': drill_id}
   rc, code = cipc.send_msg(cipc.PUT, cipc.MODE, mode)
   if not rc:
      logging.error("test_drill: initial PUT mode failed, code: {}".format(code))
      return False

   # start and check for active
   rc, code = cipc.send_msg(cipc.PUT, cipc.START)
   if not rc:
      logging.error("test_drill: PUT START failed, code: {}".format(code))
      return False
   active = cipc.is_active()
   if (type(active) is not bool):
      return False
   if not active:
      logging.error("Base didn't go active after start command")
      test_rc = False

   # stop and check for inactive
   rc, code = cipc.send_msg(cipc.PUT, cipc.STOP)
   if not rc:
      logging.error("test_game: PUT STOP failed, code: {}".format(code))
      return False
   active = cipc.is_active()
   if (type(active) is not bool):
      return False
   if active:
      logging.error("Base didn't go inactive after stop command")
      test_rc = False

   return test_rc



def test_register(register_under_test, default_values):
    test_pattern = {}
    read_back_compare = True
    msg_ok, register_original = cipc.send_msg(cipc.GET, register_under_test)
    if not msg_ok:
        logging.error("GET {} failed.".format(register_under_test))
        return False
    if len(register_original) == 0:
        register_original = default_values
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
        if cipc.send_msg(cipc.PUT, register_under_test, test_pattern) == False:
            logging.error("PUT {} failed".format(register_under_test))
            break
        msg_ok, reg_read_back = cipc.send_msg(cipc.GET, register_under_test)
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
    if (cipc.send_msg(cipc.PUT, register_under_test, register_original) == False):
        logging.error("restore {} failed".format(register_under_test))
    logging.info("Register test done: {} restored to: {}".format(register_under_test, cipc.get(register_under_test)))
    return(read_back_compare)

if __name__ == "__main__":
    run_tests()
