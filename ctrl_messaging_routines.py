
__all__ = ["send_msg", "is_active"]

import os as _os
from sys import platform as _platform
import errno as _errno
from select import select as _select
import logging

from control_ipc_defines import RSRC_OFFSET, GET_METHOD, PUT_METHOD, RSP_METHOD, STAT_RSRC, \
   RESP_OK, MAX_MESSAGE_SIZE, HEADER_LENGTH

_logger = logging.getLogger(__name__)
# log_format = ('[%(asctime)s] %(levelname)-6s %(name)-12s %(message)s')
_log_format = ('[%(asctime)s] %(levelname)-6s %(message)s')

logging.basicConfig(
   # level=logging.DEBUG,
   level=logging.INFO,
   format=_log_format,
   # filename=('debug.log'),
)

# _HEADER_LENGTH = 8
_RESP_CODE_START = RSRC_OFFSET + 1
# _MAX_BYTES_TO_READ = 80

# _OK = bytearray("RSP  200", 'utf-8')
_OK = bytearray(RSP_METHOD + "  " + str(RESP_OK), 'utf-8')

if 'darwin' in _platform:
   _FIFO_BASE_TO_CTRL = "/tmp/BaseToCtrl.fifo"
   _FIFO_CTRL_TO_BASE = "/tmp/CtrlToBase.fifo"
else:
   _FIFO_BASE_TO_CTRL = "/dev/shm/BaseToCtrl.fifo"
   _FIFO_CTRL_TO_BASE = "/dev/shm/CtrlToBase.fifo"

_fd_read = None
_fd_write = None
_non_empty_pipe_count = 0


def init(read_fifo=_FIFO_BASE_TO_CTRL, write_fifo=_FIFO_CTRL_TO_BASE):
   global _fd_read
   global _fd_write

   try:
      _os.mkfifo(write_fifo)
      _os.mkfifo(read_fifo)
   except OSError as oe:
      if oe.errno != _errno.EEXIST:
         raise

   # logging.debug('Opening {} for writing.'.format(write_fifo))
   # the following does NOT block until read end is open
   _fd_write = _os.open(write_fifo, _os.O_WRONLY)
   logging.debug("{} opened.".format(write_fifo))

   # logging.debug('Opening {} for reading.'.format(read_fifo))
   # the following does! block until write end is open
   _fd_read = _os.open(read_fifo, _os.O_RDONLY)
   logging.debug("{} opened.".format(read_fifo))

def string_to_dict(a_str):
   dict_out = {}
   kv_list = a_str.split(',')
   for kv in kv_list: 
      pair = kv.split(':')
      dict_out[pair[0]] = pair[1]
   return dict_out

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


def send_msg(method=GET_METHOD, resource=STAT_RSRC, settings={}):
   global _fd_read
   global _fd_write
   msg = None
   rc = False
   if _fd_write is None:
      init()

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
   if len(data) == 0:
      logging.debug("FIFO read failed; write end closed?")
   else:
      logging.debug("Read: {}{}".format(data[0:HEADER_LENGTH], data[HEADER_LENGTH:]))
      code = data[_RESP_CODE_START:HEADER_LENGTH]
      if data.startswith(_OK):
         rc = True
         if len(data) > HEADER_LENGTH:
            msg = string_to_dict(data[HEADER_LENGTH:].decode("utf-8"))
      else:
            logging.error(
               "{} {} rejected - code: {}".format(method, resource, code))
            
   if (method is PUT_METHOD):
      return rc, code
   else:
      return rc, msg


def is_active():
   msg_ok, status = send_msg()
   if not msg_ok:
      print("Error getting status")
      return "error"
   else:
      print("Status: {}".format(status))
      if (status is not None) and ('active' in status) and (int(status['active']) == 1):
         return True
      else:
         return False
