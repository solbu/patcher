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
Usage: patcher stop [OPTIONS] [DIR]

This command will remove the necessary structures for patcher to
work. If DIR is not given, the current directory will be used.

Options:
    -h      Show this message

Examples:
    patcher stop
"""

def parse_options():
    parser = OptionParser(help=HELP)
    parser.defaults["dir"] = "."
    opts, args = parser.parse_args()
    if len(args) == 1:
        opts.dir = args[0]
    elif args:
        raise Error, "invalid arguments"
    return opts

def stop(dir="."):
    Manager(dir).stop()
    
def main():
    do_command(parse_options, stop)

# vim:et:ts=4:sw=4
