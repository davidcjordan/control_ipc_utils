#!/usr/bin/env python3
"""
Sends stop/pause/resume message to boomer_base
"""
from ctrl_messaging_routines import send_msg, is_active
from control_ipc_defines import PUT_METHOD, STOP_RSRC, PAUS_RSRC, RESU_RSRC
import logging
import sys

if __name__ == '__main__':
   # print("argv[0]: {}".format(sys.argv[0]))
   resource = None
   if "stop" in sys.argv[0]:
      resource = STOP_RSRC
   elif "pause" in sys.argv[0]:
      resource = PAUS_RSRC
   elif "resume" in sys.argv[0]:
      resource = RESU_RSRC
   else:
      print("command not recognized: %s", sys.argv[0])
      sys.exit(1)

   rc, code = send_msg(PUT_METHOD, resource)
   if not rc:
      # the following logging is already performed by send_mgs
      # logging.error("PUT {} failed, code: {}".format(resource, code))
      sys.exit(1)

   if resource is STOP_RSRC:
      active = is_active()
      if (type(active) is not bool):
         logging.error("GET Status failed")
         sys.exit(1)
      if active:
         logging.error("Base didn't go INactive after stop command")
         sys.exit(1)
