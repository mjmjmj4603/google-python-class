#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

A. Implement the extract_names(filename) function, filename e.g.baby1990.html
returns file data as a sorted single list: the year string at the start
followed by the name-rank strings. ['2006', 'Aaliyah 91', 'Abagail 895', ...]
Modify main() so it calls extract_names() and prints what it returns

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...
Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
 

B. Instead of printing to standard output,
write a new file 'babyxxxx.html.summary' that contains the summary text
for that file if the flag --summaryfile is present.
Run the program on all the files using * like this:
 "./babynames.py --summaryfile baby*.html"
This generates all the summaries in one step.


C. Hints: Regular expression
          year: r'Popularity\sin\s(\d\d\d\d)'
          names: r'<td>(\d+)</td><td>(\w+)</td>\<td>(\w+)</td>'

"""

def extract_names(filename):
  """
  Given a file e.g.baby1990.html, returns a list starting with the year string
  followed by the name-rank strings in alphabetical order.
  ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """
  # The list [year, name_rank, name_rank, ...] we'll eventually return.
  names = []

  # Open and read the file.
  f = open(filename, 'rU')
  text = f.read()

  # Get the year.
  year_match = re.search(r'Popularity\sin\s(\d\d\d\d)', text)
  if not year_match:
    # We didn't find a year, so we'll exit with an error message.
    sys.stderr.write('Couldn\'t find the year!\n')
    sys.exit(1)
  year = year_match.group(1)
  names.append(year)

  # Extract all the data tuples with a findall()
  # each tuple is: (rank, boy-name, girl-name)
  tuples = re.findall(r'<td>(\d+)</td><td>(\w+)</td>\<td>(\w+)</td>', text)
  #print tuples

  # Store data into a dict using each name as key, rank number as value.
  # (if the name is already in there, don't add it, since
  # this new rank will be bigger than the previous rank).
  names_to_rank =  {}
  for rank_tuple in tuples:
    (rank, boyname, girlname) = rank_tuple  # unpack the tuple into 3 vars
    if boyname not in names_to_rank:
      names_to_rank[boyname] = rank
    if girlname not in names_to_rank:
      names_to_rank[girlname] = rank

  # Get the names, sorted in the right order
  sorted_names = sorted(names_to_rank.keys())
  
  # Build up result list, one element per line
  for name in sorted_names:
    names.append(name + " " + names_to_rank[name])

  return names


def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print 'usage: [--summaryfile] file [file ...]'
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]

  # +++your code here+++
  # For each filename, get the names, then either print the text output
  # or write it to a summary file

  for filename in args:
    names = extract_names(filename)

    # Make text out of the whole list
    text = '\n'.join(names)

    if summary:
      outf = open(filename + '.summary', 'w')
      outf.write(text + '\n')
      outf.close()
    else:
      print text
  
if __name__ == '__main__':
  main()


# With the data organized into summary files
# you can see patterns over time with shell commands, like this:
# grep 'Trinity ' *.summary
# grep 'Nick ' *.summary
# grep 'Miguel ' *.summary
# grep 'Emily ' *.summary
