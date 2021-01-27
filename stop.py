#!/usr/bin/env python3
"""
Sends stop message to boomer_base
"""
from ctrl_messaging_routines import *
import logging
import sys

if __name__ == '__main__':
   # start and check for active
   rc, code = send_msg(PUT, STOP)
   if not rc:
      logging.error("PUT STOP failed, code: {}".format(code))
      sys.exit(1)
   active = is_active()
   if (type(active) is not bool):
      logging.error("GET Status failed")
      sys.exit(1)
   if active:
      logging.error("Base didn't go INactive after stop command")
      sys.exit(1)
