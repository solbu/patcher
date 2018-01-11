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
import optparse
import sys, os

__all__ = ["OptionParser", "do_command", "parse_paths"]

class CapitalizeHelpFormatter(optparse.IndentedHelpFormatter):

    def format_usage(self, usage):
        return optparse.IndentedHelpFormatter \
                .format_usage(self, usage).capitalize()

    def format_heading(self, heading):
        return optparse.IndentedHelpFormatter \
                .format_heading(self, heading).capitalize()

class OptionParser(optparse.OptionParser):

    def __init__(self, usage=None, help=None, **kwargs):
        if not "formatter" in kwargs:
            kwargs["formatter"] = CapitalizeHelpFormatter()
        optparse.OptionParser.__init__(self, usage, **kwargs)
        self._overload_help = help

    def format_help(self, formatter=None):
        if self._overload_help:
            return self._overload_help
        else:
            return optparse.OptionParser.format_help(self, formatter)

    def error(self, msg):
        raise Error, msg

def do_command(parse_options_func, main_func):
    try:
        opt = parse_options_func()
        main_func(**opt.__dict__)
    except Error, e:
        sys.stderr.write("error: %s\n" % str(e))
        sys.exit(1)

def parse_paths(paths):
    dirorder = []
    direntries = {}
    for path in paths:
        if os.path.isdir(path):
            dir = path
            entry = None
        else:
            dir = os.path.dirname(path)
            if not dir:
                dir = "."
            entry = os.path.basename(path)
        if not direntries.has_key(dir):
            dirorder.append(dir)
            direntries[dir] = []
        if entry:
            direntries[dir].append(entry)
    return dirorder, direntries

# vim:et:ts=4:sw=4
