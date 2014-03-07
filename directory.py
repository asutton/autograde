
import os
import os.path

from diagnostic import *

# FIXME: Migrate system commands to use the subprocess module.

def check(hw):
  """Check that the student has correctly created the project
  directory and has not committed intermediate files."""

  r = Report()
  if diagnose_hw_dir(r, hw):
    diagnose_build_dir(r, hw)
  return r;

def diagnose_hw_dir(r, hw):
  """If the project directory is missing, try to diagnose the reason
  for it."""
  if os.path.exists(hw):
    return True
  
  # Diagnose the error and try to locate the actual
  # project directory.
  r.diags += [Error("project directory '" + hw + "' is missing")]
  find_project(r, hw)
  return False

def diagnose_build_dir(r, hw):
  """Search for and diagnose commits of build intermediates.

  TODO: This should really be a recursive search through the hw directory
  to find known temporary files.
  """

  os.chdir(hw)
  find_cache(r, hw);
  os.chdir("..")


def find_project(r, hw):
  """Search for a CMakeLists.txt that declares the project hw or
  any other capitalization of that phrase."""

  # Search in the current directory for a CMakeLists.txt file that
  # contains something like the given project.
  cmd = "find . -name CMakeLists.txt -exec grep -Hi {0} {{}} \; | grep -i project".format(hw)
  out = os.popen(cmd)
  txt = out.readlines()
  out.close()

  # Transform the output into something readable.
  for i in txt:
    found = i.split(':')
    
    # Scrub the path name
    path = os.path.dirname(found[0])[2:]
    if not path:
      path = "top-level directory"
    else:
      path = "directory '{0}'".format(path)
    r.diags += [Note("  possible candidate in the {0}".format(path))]


def find_cache(r, hw):
  """Search for a CMakeCache.txt and register a diagnostic if one 
  is found."""

  cmd = "find . -name CMakeCache.txt"
  out = os.popen(cmd)
  txt = out.readlines()
  out.close()
  
  # Transform the output into something readable.
  for i in txt:
    found = i.split(':')
    
    # Scrub the path name
    path = os.path.dirname(found[0])[2:]
    if path == "__build__":
      continue
    r.diags += [Note("found build files in '{0}'".format(path))]
