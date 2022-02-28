
__all__ = ["send_msg", "is_active"]

import os as _os
from sys import platform as _platform
import errno as _errno
from select import select as _select
import logging
import time
import json

from control_ipc_defines import RSRC_OFFSET, GET_METHOD, PUT_METHOD, RSP_METHOD, STAT_RSRC, base_state_e, \
   RESP_OK, MAX_MESSAGE_SIZE, HEADER_LENGTH, BASE_NAME, CTRL_NAME, UI_NAME, CTRL_TRANSPRT, UI_TRANSPRT

_RESP_CODE_START = RSRC_OFFSET + 1
_OK = bytearray(RSP_METHOD + "  " + str(RESP_OK), 'utf-8')

_fd_read = None
_fd_write = None
_non_empty_pipe_count = 0

# normally inherits log level from calling scripts
# logging.basicConfig(level=logging.DEBUG)

def init(channel=CTRL_TRANSPRT):
   global _fd_read
   global _fd_write

   if _fd_write is not None:
      return True

   if channel == CTRL_TRANSPRT:
      logging.debug("Using control channel")
      fifo_base_to_x_name = BASE_NAME + "To" + CTRL_NAME + ".fifo"
      fifo_x_to_base_name = CTRL_NAME + "To" + BASE_NAME + ".fifo"
   else:
      logging.debug("Using UI channel")
      fifo_base_to_x_name = BASE_NAME + "To" + UI_NAME + ".fifo"
      fifo_x_to_base_name = UI_NAME + "To" + BASE_NAME + ".fifo"

   if 'darwin' in _platform:
      read_fifo = "/tmp/" + fifo_base_to_x_name
      write_fifo = "/tmp/" + fifo_x_to_base_name
   else:
      read_fifo = "/dev/shm/" + fifo_base_to_x_name
      write_fifo  = "/dev/shm/" + fifo_x_to_base_name

   try:
      _os.mkfifo(write_fifo)
      _os.mkfifo(read_fifo)
   except OSError as oe:
      if oe.errno != _errno.EEXIST:
         raise

   # logging.debug('Opening {} for writing.'.format(write_fifo))
   # the following does NOT block until read end is open
   # _fd_write = _os.open(write_fifo, _os.O_WRONLY)
   # the following will get an exception if the IPC is not open
   try:
      _fd_write = _os.open(write_fifo, _os.O_WRONLY | _os.O_NONBLOCK)
   except:
   # except Exception as err:
   #    exception_type = type(err).__name__
   #    print("Unable to open write: " + exception_type)
      logging.warning("can not connect to boomer_base.")
      return False
   
   logging.debug("{} opened.".format(write_fifo))

   # logging.debug('Opening {} for reading.'.format(read_fifo))
   # the following does! block until write end is open
   _fd_read = _os.open(read_fifo, _os.O_RDONLY)
   # _fd_read = _os.open(read_fifo, _os.O_RDONLY | _os.O_NONBLOCK)
   logging.debug("{} opened.".format(read_fifo))
   return True

def dict_to_bytes(a_dict):
   ret_str = ""
   a_dict_len = len(a_dict)
   i = 0
   for k, v in a_dict.items():
      ret_str += k + ":"
      if type(v) != str:
         ret_str += str(v)
      else:
         ret_str += v
      if i < a_dict_len-1:
         ret_str += ","
      i += 1
   return str.encode(ret_str)


def empty_pipe():
   global _non_empty_pipe_count
   global _fd_read
   if _fd_write is None:
      init()

   pipe_empty = False
   while not pipe_empty:
      fd_r, _, _ = _select([_fd_read], [], [], 0)
      if _fd_read in fd_r:
         print("read pipe before sending msg: {}".format(
            _os.read(_fd_read, MAX_MESSAGE_SIZE)))
         _non_empty_pipe_count += 1
      else:
         pipe_empty = True


def send_msg(method=GET_METHOD, resource=STAT_RSRC, settings={}, channel=CTRL_TRANSPRT):
   global _fd_read
   global _fd_write
   if not init(channel):
      return False, "444"
   # time.sleep(0.2)
   empty_pipe()

   msg = None
   rc = False
   send_encoded_msg = b''
   header_bytes = str.encode(method + " " + resource + " ")
   if (method is PUT_METHOD):
      send_encoded_msg = dict_to_bytes(settings)

   # print("header type: {} -- msg type: {}".format(type(header_bytes), type(send_encoded_msg)))
   bytes_written = _os.write(_fd_write, header_bytes + send_encoded_msg)

   if bytes_written < 1:
      logging.debug("FIFO write failed; read end closed?")
   else:
      logging.debug("Wrote {} {}".format(header_bytes, send_encoded_msg))

   data = _os.read(_fd_read, MAX_MESSAGE_SIZE)
   ''' the following was for a non-blocking read - didn't work
       it was unncessary because opening the write FIFO in non-blocking mode gets an exception
   data_available = False
   for _ in range(6):
      fd_r, _, _ = _select([_fd_read], [], [], 0)
      if _fd_read in fd_r:
         break
      else:
         time.sleep(0.3)

   if data_available:
      print("reading data")
      data = _os.read(_fd_read, MAX_MESSAGE_SIZE)
   else:
      print("data not available after sending data")
      return rc, "444"
   '''

   if len(data) == 0:
      logging.debug("FIFO read failed; write end closed?")
   else:
      logging.debug(f"Read: {data[0:HEADER_LENGTH]}{data[HEADER_LENGTH:]}")
      code = data[_RESP_CODE_START:HEADER_LENGTH]
      if data.startswith(_OK):
         rc = True
         if len(data) > HEADER_LENGTH:
            msg = json.loads(data[HEADER_LENGTH:].decode("utf-8"))
      else:
            logging.error(
               "{} {} rejected - code: {}".format(method, resource, code))
            
   if (method is PUT_METHOD):
      return rc, code
   else:
      return rc, msg


def is_active():
   msg_ok, status_msg = send_msg()
   if not msg_ok:
      print("Error getting status")
      return "error"
   else:
      print("Status: {}".format(status_msg))
      if (status_msg is not None) and ('status' in status_msg) and (status_msg['status'] == base_state_e.PAUSED.value):
         return True
      else:
         return False
