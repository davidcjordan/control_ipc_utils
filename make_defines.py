#!/usr/bin/env python3

"""
Does the following:
 - reads C language .h files looking for start and end indicators
 - converts #defines into python defines
 - writes control_ipc_defines.py

 returns 0 on pass; 1 on failure
"""
import argparse
import logging
import sys

if __name__ == '__main__':
  shell_rc = 1

  COMMENT_PATTERN = "//-=-=- "
  START_PATTERN = COMMENT_PATTERN + "start"
  STOP_PATTERN = COMMENT_PATTERN + "end"
  DEFINE_PATTERN = "#define "
  OUTPUT_FILE = "control_ipc_defines.py"

  parser = argparse.ArgumentParser(description='Start boomer')
  parser.add_argument('-p', '--path', dest='h_file_dir', \
        type=str, default="../ipc/", nargs='?', \
        help='path to directory with h files')
  args = parser.parse_args()
  # print("called with {}: ".format(sys.argv[0]))
  # print("h_file_dir: {}".format(args.h_file_dir))

  in_defines_region = False
  out_file = open(OUTPUT_FILE, 'w')
  define_files = ['ipc_control.h', 'global_parameters.h']
 
  for define_file in define_files:
    with open(args.h_file_dir + define_file) as f: 
      for line in f:
        if line.startswith(START_PATTERN):
          in_defines_region = True
          out_file.write("\n# defines from file: {}\n".format(define_file))
          continue
        if in_defines_region:
          if line.startswith(DEFINE_PATTERN):
            words = line.split()
            #handle comment following define
            for i in range(len(words)):
              if words[i].startswith('//'):
                words[i] = words[i].replace('//', '#')
                break
                # print("words: {}".format(words))
                # sys.exit(1)
            out_file.write(words[1] + " = " + ' '.join(words[2:]) + "\n")
          if line.startswith(STOP_PATTERN):
            in_defines_region = False
            break

  out_file.close()
  print("generated: {}\n".format(OUTPUT_FILE))
