#!/usr/bin/python
from distutils.core import setup
import sys
import re

verpat = re.compile("VERSION *= *\"(.*)\"")
data = open("ptr").read()
m = verpat.search(data)
if not m:
    sys.exit("error: can't find VERSION")
VERSION = m.group(1)

setup(name="patcher",
      version = VERSION,
      description = "Tool for quick creation of patches against a source tree",
      author = "Gustavo Niemeyer",
      author_email = "gustavo@niemeyer.net",
      url = "http://labix.org/patcher",
      license = "GPL",
      long_description =
"""\
Patcher is a tool for quick creation of patches against a project
source tree.  Patcher functionality resembles a lightweight
version control system. It has no repository, and only controls
differences between a pristine version and a working copy.
""",
      packages = ["patcher",
		  "patcher.commands"],
      scripts = ["ptr"]
      )
