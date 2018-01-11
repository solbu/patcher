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
import sys
import getopt

HELP = """\
Usage: patcher start [OPTIONS] [DIR]

This command will create the necessary structures for patcher to
work. If DIR is not given, the current directory will be used.

Options:
    -e      Consider files to be empty when adding (useful for new files)
    -n      Start tree structure, but don't include any files
    -h      Show this message

Examples:
    patcher start
"""

def parse_options():
    parser = OptionParser(help=HELP)
    parser.defaults["dir"] = "."
    parser.add_option("-e", dest="empty", action="store_true")
    parser.add_option("-n", dest="nofiles", action="store_true")
    opts, args = parser.parse_args()
    if len(args) == 1:
        opts.dir = args[0]
    elif args:
        raise Error, "invalid arguments"
    return opts

def start(dir, empty, nofiles):
    Manager(dir).start(empty, nofiles)
    
def main():
    do_command(parse_options, start)

# vim:et:ts=4:sw=4
