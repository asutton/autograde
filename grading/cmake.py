
import sys
import os
import os.path

from subprocess import *
from diagnostic import *

# The name of the build directory.
build_dir = "__build__"

def config(r):
  """Configure the build system. Note that the current directory must be
  the top-level of the project directory."""

  # Reset and create and enter the build directory.
  os.system("rm -rf {0}".format(build_dir))
  os.mkdir(build_dir)
  os.chdir(build_dir)

  # Try to configure the build.
  result = cmake(r)

  # Back out to the previous directory.
  os.chdir("..")
  return result


def cmake(r):
  """Check the configuration by running CMake. Returns true if 
  configuration succeeds and false otherwise."""

  p = Popen("cmake ..", shell=True, stdout=PIPE, stderr=STDOUT)
  out = p.stdout.read()
  p.stdout.close()

  # Get the result of configuration, and dignose failure.
  if p.wait() != 0:
    r.error("could not configure the project")
    r.note("configuration output:\n\n + " + out + "\n")
    return False

  return True

def check_build(r):
  """Check the builds actually works."""

  # Yes... build in VERBOSE mode.
  p = Popen("VERBOSE=1 make", shell=True, stdout=PIPE, stderr=STDOUT)
  out = p.stdout.read()
  p.stdout.close()

  # Close and detect if there was an error.
  if p.wait() != 0:
    r.error("could not build all targets")
    r.note("build output:\n\n" + out + "\n")
    return False

  return True
