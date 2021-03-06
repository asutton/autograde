
import sys
import os
import os.path
import time

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
  p = Popen("ctest -VV", shell=True, stdout=PIPE, stderr=STDOUT)
  out = p.stdout.read()
  p.stdout.close()

  t = time.time()
  while p.poll() is None and (time.time() - t) < 10:
    time.sleep(.1)

  # If the child hasn't finished yet, then fail hard.
  if p.poll() is not None:
    r.error("make test timed out")
    r.note("test suite output so far:\n\n" + out + "\n")
    return False

  # If it did finish but didn't return 0, also fail hard.
  if p.returncode != 0:
    r.error("errors reported in test suite")
    r.note("test suite output:\n\n" + out + "\n")
    return False
  return True

def make_manifest(r):
  """Build the manifest.

  TODO: If the Makefile does not have a manifest target, then don't
  try to build a manifest."""


  p = Popen("make manifest", shell=True, stdout=PIPE, stderr=STDOUT)
  out = p.stdout.read()
  p.stdout.close()
  if p.wait() != 0:
    r.error("error building manifest")
    r.note("build output:\n\n" + out + "\n")
    return False
  return True
