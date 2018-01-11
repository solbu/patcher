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
Usage: patcher add [OPTIONS] PATHS

This command will include given paths in patcher control.

Options:
    -e      Consider files to be empty when adding (useful for new files)
    -n      When adding directories, don't include any files
    -h      Show this message

Examples:
    patcher add dir/file1 dir/file2
"""

def parse_options():
    parser = OptionParser(help=HELP)
    parser.add_option("-e", dest="empty", action="store_true")
    parser.add_option("-n", dest="nofiles", action="store_true")
    opts, args = parser.parse_args()
    if not args:
        raise Error, "no entry to add provided"
    opts.paths = args
    return opts

def add(paths, empty, nofiles):
    dirorder, direntries = parse_paths(paths)
    for dir in dirorder:
        added = Manager(dir).add(direntries[dir], empty, nofiles)
        for path in added:
            print "A   ", path
 
def main():
    do_command(parse_options, add)

# vim:et:ts=4:sw=4
