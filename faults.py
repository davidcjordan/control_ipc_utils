#!/usr/bin/env python3
"""
get list of faults from boomer_base
"""
import logging
log_format = ('[%(asctime)s] %(levelname)-6s %(message)s')
logging.basicConfig(format=log_format, level=logging.INFO)
# logging.basicConfig(format=log_format, level=logging.DEBUG)


if __name__ == '__main__':
   from ctrl_messaging_routines import send_msg
   from control_ipc_defines import GET_METHOD, FLTS_RSRC, UI_TRANSPRT, fault_e, net_device_e
   import sys

   msg_ok, status = send_msg()
   if not msg_ok:
      print("Error getting status")
   else:
      if (status is not None) and ('hFault' in status) and (status['hFault'] == 0):
         print("No active faults")
      else:
         print(f"{status['hFault'] } active faults")

         msg_ok, faults = send_msg(GET_METHOD, FLTS_RSRC)
         if not msg_ok:
            print("Error getting status")
         else:
            # print(f"faults: {faults}")
            if len(faults) > 0:
               print("Fault                                Device")
               for fault in faults:
                  print(f"{fault_e(fault['C']).name:36} {net_device_e(fault['L']).name}")
