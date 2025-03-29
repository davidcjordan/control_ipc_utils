#!/usr/bin/env python3
"""
get list of faults from boomer_base
"""
import datetime
import logging
log_format = ('[%(asctime)s] %(levelname)-6s %(message)s')
logging.basicConfig(format=log_format, level=logging.INFO)
# logging.basicConfig(format=log_format, level=logging.DEBUG)


if __name__ == '__main__':
   from ctrl_messaging_routines import send_msg
   from control_ipc_defines import GET_METHOD, PUT_METHOD, CTRL_TRANSPRT, SRVO_RSRC
   from control_ipc_defines import CENTER_ANGLE_PARAM, DROP_SPEED_PARAM, LOB_SPEED_PARAM

   msg_ok, servo_params = send_msg(GET_METHOD, SRVO_RSRC, channel=CTRL_TRANSPRT)
   if not msg_ok:
      print("Error getting servo parameters")
   else:
      print(f"servo parameters: {servo_params}")

   params = {CENTER_ANGLE_PARAM: 11, DROP_SPEED_PARAM: 22, LOB_SPEED_PARAM: 33}
   rc, code = send_msg(PUT_METHOD, SRVO_RSRC, params, channel=CTRL_TRANSPRT)
   if not rc:
      logging.error("PUT servo_values failed, code: {}".format(code))
