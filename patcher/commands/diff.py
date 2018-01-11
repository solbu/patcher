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
Usage: patcher diff [OPTIONS] [PATHS]

This command will compare your working copy with the originals,
and output a diff.

Options:
    -h      Show this message

Examples:
    patcher diff
    patcher diff dir/file1 dir/file2
"""

def parse_options():
    parser = OptionParser(help=HELP)
    parser.defaults["paths"] = ["."]
    opts, args = parser.parse_args()
    if args:
        opts.paths = args
    return opts

def diff(paths):
    dirorder, direntries = parse_paths(paths)
    for dir in dirorder:
        Manager(dir).diff(direntries[dir])
 
def main():
    do_command(parse_options, diff)

# vim:et:ts=4:sw=4
