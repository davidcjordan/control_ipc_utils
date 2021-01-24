
__all__ = ["send_msg", "is_active", "GET", "PUT", "STATUS", "MODE", "PARAMS", "START", "STOP"]

import os as _os
from sys import platform as _platform
import errno as _errno
from select import select as _select
import logging

from protobuf_to_dict import protobuf_to_dict, dict_to_protobuf

from message_pb2 import b_status_msg as _b_status_msg
from message_pb2 import b_mode_msg as _b_mode_msg
from message_pb2 import b_params_msg as _b_params_msg

_logger = logging.getLogger(__name__)
# log_format = ('[%(asctime)s] %(levelname)-6s %(name)-12s %(message)s')
_log_format = ('[%(asctime)s] %(levelname)-6s %(message)s')

logging.basicConfig(
   level=logging.DEBUG,
   format=_log_format,
   # filename=('debug.log'),
)

_BIPC_HEADER_LENGTH = 15
_MAX_BYTES_TO_READ = 80

GET = "GET"
PUT = "PUT"
STATUS = "STATU"
MODE = "MODE_"
PARAMS = "PARMS"
START = "START"
STOP = "STOP_"

_OK = bytearray("BIPC 200 ", 'utf-8')

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
               _os.read(_fd_read, _MAX_BYTES_TO_READ)))
            _non_empty_pipe_count += 1
      else:
            pipe_empty = True


def send_msg(method=GET, resource=STATUS, settings={}):
   global _fd_read
   global _fd_write
   msg = None
   rc = False
   if _fd_write is None:
      init()

   rcvd_encoded_msg = None
   send_encoded_msg = None
   if (method is GET):
      header_bytes = str.encode("BIPC " + GET + " " + resource + " ")
      if (resource is STATUS):
         rcvd_encoded_msg = _b_status_msg()
      elif (resource is MODE):
         rcvd_encoded_msg = _b_mode_msg()
      elif (resource is PARAMS):
         rcvd_encoded_msg = _b_params_msg()
      else:
         logging.error("{} {} not supported".format(GET, resource))
   elif (method is PUT):
      header_bytes = str.encode("BIPC PUT " + resource + " ")
      if (resource is MODE):
         send_encoded_msg = dict_to_protobuf(
               _b_mode_msg, values=settings).SerializeToString()
      elif (resource is PARAMS):
         send_encoded_msg = dict_to_protobuf(
               _b_params_msg, values=settings).SerializeToString()

   if (rcvd_encoded_msg is not None or method is PUT):
      if (send_encoded_msg is not None):
         bytes_written = _os.write(_fd_write, header_bytes + send_encoded_msg)
      else:
         bytes_written = _os.write(_fd_write, header_bytes)

      if bytes_written < 1:
         logging.debug("FIFO write failed; read end closed?")
      else:
         logging.debug("Wrote {}".format(header_bytes))

      data = _os.read(_fd_read, _MAX_BYTES_TO_READ)
      if len(data) == 0:
         logging.debug("FIFO read failed; write end closed?")
      else:
         logging.debug("Read: Header: {}   Body: {}".format(
               data[0:14], data[_BIPC_HEADER_LENGTH:]))
         code = data[5:8]
         if data.startswith(_OK):
               rc = True
               if len(data) > _BIPC_HEADER_LENGTH:
                  bytes_parsed = rcvd_encoded_msg.ParseFromString(
                     data[_BIPC_HEADER_LENGTH:])
                  if (bytes_parsed != len(data)-_BIPC_HEADER_LENGTH):
                     logging.error("Message parse error: parsed: {} - should be {}".
                                    format(bytes_parsed, len(data)-_BIPC_HEADER_LENGTH))
                  else:
                     msg = protobuf_to_dict(rcvd_encoded_msg)
         else:
               logging.error(
                  "{} {} rejected - code: {}".format(method, resource, code))
               
   if (method is PUT):
      return rc, code
   else:
      return rc, msg


def is_active():
   msg_ok, status = send_msg()
   if not msg_ok:
      print("Error getting status")
      return "error"
   else:
      if (status is not None) and ('active' in status) and (status['active'] == 1):
         return True
      else:
         return False
