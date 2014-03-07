#!/usr/bin/python

import sys
import os
import os.path

import directory
import build

"""This program performs a number of common operations on a student's
homework assignment, and produces a report of the evaluation.

The usage of autograde is:

    autograde <hw>

where <hw> is the name of the assignment. Note that that the program must
be run from within a student directory.
"""

def log(f, s):
  sys.stdout.write(s)
  f.write(s)

def summarize(diags, hw):
  """Create a single report in the user's directory containing a list
  of errors and diagnostics."""

  p = os.getcwd()
  u = os.path.basename(p)

  f = open("eval-{0}.log".format(hw), "w")
  log(f, "== results for {0} ==\n".format(u))
  n = 0;
  for d in diags:
    if d.diags:
      log(f, str(d) + "\n")
      n = n + 1;
  if n == 0:
    log(f, "success\n")
  log(f, "\n\n");
  f.flush()
  sys.stdout.flush()


def check(hw):
  """Check the homework assignment by performing a number of operations
  within the user's directory.

  - Check the project directory
  - Build the project
  - Run the tests (if any)
  - Assemble a summary document
  """

  # Keep a list of diagnostics for each successive check
  # of the project directory.
  diags = []

  diags += [directory.check(hw)]

  if diags[-1]:
    diags += [build.check(hw)]

  # if diags[-1]:
  #   diags += [check_tests(hw)]:

  return summarize(diags, hw)


def usage():
  """Print usage information."""
  print "usage: autograde <hw>"

def main():
  """Run the main program."""
  if len(sys.argv) < 2:
    usage()
    return

  cwd = os.getcwd() # current workdin directory
  hw = sys.argv[1]   # assignment name

  check(hw);

if __name__ == "__main__":
  main()

