
import os
import os.path

from subprocess import *
from diagnostic import *

def eval(hw, r):
  """Evaluate the project directory. This determines if the directory
  exists. If not, try to determine where the directory might be and
  emit appropriate diagnostics."""

  # Check that the hw path exists and is a directory. If so, try
  # to determine if the student has committed a build directory.
  if os.path.isdir(hw):
    find_build_dir(hw, r)
    return True
  else:
    # Diagnose the error and try to locate the actual
    # project directory.
    r.error("project directory '" + hw + "' is missing")
    find_project(hw, r)
    return False


def find_project(hw, r):
  """Search for a CMakeLists.txt that declares the project hw or
  any other capitalization of that phrase."""

  # Search in the current directory for a CMakeLists.txt file that
  # contains something like the given project.
  cmd = "find . -name CMakeLists.txt -exec grep -Hi {0} {{}} \; | grep -i project".format(hw)
  p = Popen(cmd, shell=True, stdout=PIPE)
  out = p.stdout.read()
  p.stdout.close()
  p.wait()

  # Transform the output into something readable.
  for i in out:
    found = i.split(':')
    
    # Scrub the path name
    path = os.path.dirname(found[0])[2:]
    if not path:
      path = "top-level directory"
    else:
      path = "directory '{0}'".format(path)
    r.note("  possible candidate in the {0}".format(path))


def find_build_dir(hw, r):
  """Search for and diagnose commits of build intermediates.

  TODO: This should really be a recursive search through the hw directory
  to find known temporary files.
  """
  os.chdir(hw)
  find_cache(hw, r);
  os.chdir("..")


def find_cache(hw, r):
  """Search for a CMakeCache.txt and register a diagnostic if one 
  is found."""

  cmd = "find . -name CMakeCache.txt"
  p = Popen(cmd, shell=True, stdout=PIPE)
  out = p.stdout.readlines()
  p.stdout.close()
  p.wait()
  
  # Transform the output into something readable.
  for i in out:
    found = i.split(':')
    
    # Scrub the path name
    path = os.path.dirname(found[0])[2:]
    if path == "__build__":
      continue
    r.note("found build files in '{0}'".format(path))
