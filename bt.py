#!/usr/bin/env python3

import curses
#import time
#import sys

import logging
logger = logging.getLogger(__name__)
log_format = ('[%(asctime)s] %(levelname)-6s %(message)s')

logging.basicConfig(
   #  level=logging.DEBUG,
    level=logging.INFO,
    format=log_format,
    # filename=('debug.log'),
)


from ctrl_messaging_routines import send_msg, is_state
from control_ipc_defines import *

def game_start():
   rc, code = send_msg(PUT_METHOD, STOP_RSRC)
   mode_reg = {MODE_PARAM: base_mode_e.GAME.value}
   rc, code = send_msg(PUT_METHOD, MODE_RSRC, mode_reg)
   rc, code = send_msg(PUT_METHOD, STRT_RSRC)

def drill_start(drill_id):
   rc, code = send_msg(PUT_METHOD, STOP_RSRC)
   mode_reg = {MODE_PARAM: base_mode_e.DRILL.value, ID_PARAM: drill_id}
   rc, code = send_msg(PUT_METHOD, MODE_RSRC, mode_reg)
   rc, code = send_msg(PUT_METHOD, STRT_RSRC)

def workout_start(workout_id):
   rc, code = send_msg(PUT_METHOD, STOP_RSRC)
   mode_reg = {MODE_PARAM: base_mode_e.WOKROUT.value, ID_PARAM: workout_id}
   rc, code = send_msg(PUT_METHOD, MODE_RSRC, mode_reg)
   rc, code = send_msg(PUT_METHOD, STRT_RSRC)


def main(main_screen):
   screen = curses.initscr()
   # lines, columns, start line, start column
   my_window = curses.newwin(3, 48, 0, 0)
   refresh_count = 1
   while True:
      mode = ''
      drill_worko_id = ''
      toss_it, state = is_state()
      if (state is None):
         state = 'Not_Running'
      else:
         msg_ok, mode_reg = send_msg(GET_METHOD, MODE_RSRC)
         if not msg_ok:
            logging.error(f"GET Mode register failed.")
         else:
            if (mode_reg is not None) and (MODE_PARAM in mode_reg):
               mode = base_mode_e(mode_reg[MODE_PARAM]).name
               if (base_mode_e(mode_reg[MODE_PARAM]) == base_mode_e.DRILL):
                  drill_worko_id = mode_reg[ID_PARAM]

      my_window.clear() #clears warning from ctrl_messaging_routines
      my_window.addstr(0, 0, state)
      my_window.addstr(0, 14, f"{mode} {str(drill_worko_id)}")
      my_window.addstr(0, 30, f"Faults: {refresh_count}")
      my_window.addstr(1, 0, "Command (d,g,w,t,e,q,?): ")
      my_window.refresh()
      my_window.timeout(2000) #millisec
      c = my_window.getch()
      refresh_count += 1
      if c == ord('q'):
         break
      if c == ord('?'):
         my_window.addstr(1, 0, "d=drill, g=game, w=workout, t=toggle_pause")
         my_window.addstr(2, 8, "e=end game/drill/wo, q=quit")
         my_window.refresh()
         curses.napms(3000)
      if c == ord('g'): 
         game_start()
      if c == ord('d'): 
         # window.clrtoeol()
         my_window.clear()
         my_window.addstr(1, 0, "Enter drill number: ")
         curses.echo()
         my_window.refresh()
         my_window.timeout(-1)
         entry = my_window.getstr().decode(encoding="utf-8")
         curses.noecho()
         drill_start(entry)
      if c == ord('w'): 
         my_window.clear()
         my_window.addstr(1, 0, "Enter workout number: ")
         curses.echo()
         my_window.refresh()
         my_window.timeout(-1)
         entry = my_window.getstr().decode(encoding="utf-8")
         curses.noecho()
         workout_start(entry)
 
   curses.endwin()
   # raise Exception

curses.wrapper(main)