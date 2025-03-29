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
   from control_ipc_defines import SERVE_ANGLE_PARAM, FLAT_ANGLE_PARAM, LOOP_ANGLE_PARAM
   from control_ipc_defines import CHIP_ANGLE_PARAM, TOPSPIN_ANGLE_PARAM, PASS_ANGLE_PARAM

   msg_ok, servo_params = send_msg(GET_METHOD, SRVO_RSRC, channel=CTRL_TRANSPRT)
   if not msg_ok:
      print("Error getting servo parameters")
   else:
      print(f"servo parameters: {servo_params}")

   params = {CENTER_ANGLE_PARAM: 25, DROP_SPEED_PARAM: 284, LOB_SPEED_PARAM: 412}
   ang_params1 = {SERVE_ANGLE_PARAM: 219, FLAT_ANGLE_PARAM: 135, LOOP_ANGLE_PARAM: 145}
   ang_params2 = {CHIP_ANGLE_PARAM: 199, TOPSPIN_ANGLE_PARAM: 250, PASS_ANGLE_PARAM: 215}
   params.update(ang_params1)
   params.update(ang_params2)
   logging.debug(f"params: {params}")
   rc, code = send_msg(PUT_METHOD, SRVO_RSRC, params, channel=CTRL_TRANSPRT)
   if not rc:
      logging.error("PUT servo_values failed, code: {}".format(code))
