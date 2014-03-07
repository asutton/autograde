autograde
=========

A tool that helps automate the more mechanical aspects of grading
homework assignments. The program is designed to configure, build,
and test student assignments written in C++.

CMake is used to support cross-platform builds, allowing students to
work in whatever IDEs are supported by that system (e.g., VS, Eclipse,
or just a shell and editor).

It is assumed that students will write portable code. That is, they
should not rely features specific to any operating system. Projects
with external dependencies should guarantee that those dependencies
are also portable. That is, they can be compiled or linked against on 
any system on which the student or evaluator might build and run the 
project).


Installing autograde
====================

The project has a several dependencies:
- python-2.7
- cmake
- pandoc
- ps2pdf
- a2ps

Installation is triival. Just clone this direcory. You can put it
on path, create an alias to the `autograde` executable, or create
a symlink in a directory that is already on path.

Running autograde
=================

Usage: `autograde <dir>`

The `<dir>` is the top-level directory of the project. For example, an 
assignmennt to implement a `Linked_list` class might be developed in a 
`list` directory. So, the project would be graded by running:


```bash
$ autograde list
```

Autograde will attempt to configure a build system, build the project,
run the test suite, and assemble a manifest for grading. Autograde
creates a file within the target directory (e.g., `list`) called
`eval-$dir.log` (e.g., `eval-list`.log) that 

If any stages
of this process fail, the results ar write

Note that autograde does *not* assign grades to student projects. Grades
are assigned by evaluating the results of autograde and the project as
a whole.


Project layout
==============

Student projects must contain a CMakeLists.txt file that can be used to
configure a build, a test suite, and a manifest (or submission). A
sample `CMakeLists.txt` can be found in the `cmake` directory of this
project.

The `CMakeLists.txt` must have the following build components:

- Testing must be enabled
- The project must have at least one test (add_test)
- The project must include a manifest (make_manifest)

The project may include a README.md file -- I prefer to use 
[Markdown](http://daringfireball.net/projects/markdown/) to document
project or include written components of the project.


Manifest
========

The manifest is a PDF containing project documentation (i.e., README.md)
and source code listits.


