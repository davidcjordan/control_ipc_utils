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
   from control_ipc_defines import GET_METHOD, CTRL_TRANSPRT
   from control_ipc_defines import FLTS_RSRC, FLT_CODE_PARAM, FLT_LOCATION_PARAM, FLT_TIMESTAMP_PARAM
   from control_ipc_defines import fault_e, net_device_e
   import sys

   msg_ok, status = send_msg(channel=CTRL_TRANSPRT)
   if not msg_ok:
      print("Error getting status")
   else:
      if (status is not None) and ('hFault' in status) and (status['hFault'] == 0):
         print("No active faults")
      else:
         print(f"{status['hFault'] } active faults: ")

         msg_ok, faults = send_msg(GET_METHOD, FLTS_RSRC, channel=CTRL_TRANSPRT)
         if not msg_ok:
            print("Error getting status")
         else:
            # print(f"faults: {faults}")
            # added an additional check to 
            if len(faults) > 0:
               if FLT_TIMESTAMP_PARAM not in faults[0]:
                  print(f"Error: fault table entry format is unexpected: {fault}")
               else:   
                  print(" Fault                                Device     Time")
                  for fault in faults:
                     timestamp = datetime.datetime.fromtimestamp(fault[FLT_TIMESTAMP_PARAM])
                     date_time = timestamp.strftime("%Y/%m/%d_%H:%M:%S")
                     print(f" {fault_e(fault[FLT_CODE_PARAM]).name:36s} {net_device_e(fault[FLT_LOCATION_PARAM]).name:9s} {date_time}")
