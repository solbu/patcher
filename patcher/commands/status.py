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
Usage: patcher status [OPTIONS] [PATHS]

This command will show the status of given paths.

Options:
    -v      Be more verbose
    -h      Show this message

Examples:
    patcher status
    patcher status dir/file1 dir/file2
"""

def parse_options():
    parser = OptionParser(help=HELP)
    parser.defaults["paths"] = ["."]
    parser.add_option("-v", dest="verbose", action="count", default=0)
    opts, args = parser.parse_args()
    if args:
        opts.paths = args
    return opts

def status(paths, verbose):
    dirorder, direntries = parse_paths(paths)
    if not verbose:
        hide = "?_"
    elif verbose == 1:
        hide = "_"
    else:
        hide = ""
    for dir in dirorder:
        status = Manager(dir).status(direntries[dir])
        for letter, path in status:
            if letter not in hide:
                print letter, "  ", path
 
def main():
    do_command(parse_options, status)

# vim:et:ts=4:sw=4
