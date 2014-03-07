
import sys
import os
import os.path

from subprocess import *
from diagnostic import *

# The name of the build directory.
build_dir = "__build__"

def all(r):
  os.chdir(build_dir)
  result = make_all(r)
  os.chdir("..")
  return result

def test(r):
  os.chdir(build_dir)
  result = make_test(r)
  os.chdir("..")
  return result

def manifest(r):
  os.chdir(build_dir)
  result = make_manifest(r)
  os.chdir("..")
  return result


def make_all(r):
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

def make_test(r):
  # This isn't really a make command since I want to get extra
  # verbose output, but it's close enough.
  p = Popen("ctest -W", shell=True, stdout=PIPE, stderr=STDOUT)
  out = p.stdout.read()
  p.stdout.close()

  # Close and detect if there was an error.
  if p.wait() != 0:
    r.error("error building test suite")
    r.note("test suite output:\n\n" + out + "\n")
    return False
  return True

def make_manifest(r):
  p = Popen("make manifest", shell=True, stdout=PIPE, stderr=STDOUT)
  out = p.stdout.read()
  p.stdout.close()
  if p.wait() != 0:
    r.error("error building manifest")
    r.note("build output:\n\n" + out + "\n")
    return False
  return True
