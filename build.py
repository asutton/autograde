
import sys
import os
import os.path
from subprocess import *
from diagnostic import *

# The name of the build directory.
build_dir = "__build__"

def check(hw):
  r = Report()

  os.chdir(hw)

  # Reset and create the build directory.
  reset()
  os.mkdir(build_dir)
  os.chdir(build_dir)

  # Check the config and build.
  if check_config(r):
    check_build(r)

  os.chdir("..") # Leave the build directory
  # reset()        # Clean up previous work
  os.chdir("..") # Leave the hw directory
  return r


def reset():
  os.system("rm -rf {0}".format(build_dir))


def log(f, s):
  """Write output to the given log file."""
  l = open("../" + f, "w")
  l.write(s)
  l.close()


def check_config(r):
  """Check the configuration by running CMake. Returns true if 
  configuration succeeds and false otherwise."""

  p = Popen("cmake ..", shell=True, stdin=None, stdout=PIPE, stderr=STDOUT, close_fds=True)
  out = p.stdout.read()
  p.stdout.close()

  if p.wait() != 0:
    r.error("could not configure the project")
    r.note("configuration output:\n\n + " + out + "\n")
    return False

  return True

def check_build(r):
  """Check the builds actually works."""

  # Yes... build in VERBOSE mode.
  p = Popen("VERBOSE=1 make", shell=True, stdin=None, stdout=PIPE, stderr=STDOUT, close_fds=True)
  out = p.stdout.read()
  p.stdout.close()

  # Close and detect if there was an error.
  if p.wait() != 0:
    r.error("could not build all targets")
    r.note("build output:\n\n" + out + "\n")
    return False

  return True
