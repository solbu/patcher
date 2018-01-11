#!/usr/bin/python
#
# Copyright (c) 2002 Gustavo Niemeyer <niemeyer@conectiva.com>
#
# This file is part of patcher.
# 
# pybot is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# pybot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with pybot; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
from patcher import Error
from patcher.manager import Manager
from patcher.command import *
import sys, os
import getopt

HELP = """\
Usage: patcher remove [OPTIONS] PATHS

This command will remove given paths from patcher control. Notice that
once you do that, the pristine version is lost. You may want to use
the ignore command instead.

Options:
    -h      Show this message

Examples:
    patcher remove dir/file1 dir/file2
"""

def parse_options():
    parser = OptionParser(help=HELP)
    opts, args = parser.parse_args()
    if not args:
        raise Error, "no entry to remove provided"
    opts.paths = args
    return opts

def remove(paths):
    dirorder, direntries = parse_paths(paths)
    for dir in dirorder:
        removeed = Manager(dir).remove(direntries[dir])
        for path in removeed:
            print "R   ", path
 
def main():
    do_command(parse_options, remove)

# vim:et:ts=4:sw=4
