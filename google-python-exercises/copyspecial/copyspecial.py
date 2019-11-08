#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands

"""
Copy Special exercise

'special' file is one where the name contains the pattern __w__ somewhere,
where the w is one or more word chars. Write functions to implement
the features below and modify main() to call your functions.

Suggested functions for your solution:

get_special_paths(dir) -- returns a list of the absolute paths of the special files in the given directory
copy_to(paths, dir) -- given a list of file paths, copies those files into the given directory
zip_to(paths, zippath) -- given a list of file paths, zip those files up into the given zipfile

"""

# +++your code here+++
"""A. Given a dirname, returns a list of all its special files."""
def get_special_paths(dirname):
  
  result = []
  paths = os.listdir(dirname)  # list of paths in that dir
  for fname in paths:
    match = re.search(r'__(\w+)__', fname)
    if match:
      result.append(os.path.abspath(os.path.join(dirname, fname)))
  return result


"""B. Copy all of the given files to the given dir, creating it if necessary.
      Use the python module "shutil" for file copying."""
def copy_to(paths, to_dir):
  
  if not os.path.exists(to_dir):
    os.mkdir(to_dir) 
  for path in paths:
    fname = os.path.basename(path)
    shutil.copy(path, os.path.join(to_dir, fname))
    # could error out if already exists os.path.exists():
    

"""C. Zip up all of the given files into a new zip file with the given name."""
def zip_to(paths, zipfile):
  
  cmd = 'zip -j ' + zipfile + ' ' + ' '.join(paths)
  print "Command I'm going to do:" + cmd
  (status, output) = commands.getstatusoutput(cmd)
  # If command had a problem (status is non-zero),
  # print its output to stderr and exit.
  if status:
    sys.stderr.write(output)
    sys.exit(1)


def main():
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  # +++your code here+++
  # Call your functions
  
  # Gather all the special files
  paths = []
  for dirname in args:
    paths.extend(get_special_paths(dirname))

  if todir:
    copy_to(paths, todir)
  elif tozip:
    zip_to(paths, tozip)
  else:
    print '\n'.join(paths)
  
if __name__ == "__main__":
  main()

# ./copyspecial.py dirname

# ./copyspecial.py --todir /tmp/fooby .
# ls /tmp/fooby

# ./copyspecial.py --tozip tmp.zip .
# to test error: write a zip file to a directory that does not exist.
# ./copyspecial.py --tozip /no/way.zip .
