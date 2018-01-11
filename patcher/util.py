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
import sys, os
import md5
#import commands

# Our own version of commands' getstatusoutput(). We have a commands
# module directory, so we can't import Python's standard module
def commands_getstatusoutput(cmd):
    """Return (status, output) of executing cmd in a shell."""
    import os
    pipe = os.popen('{ ' + cmd + '; } 2>&1', 'r')
    text = pipe.read()
    sts = pipe.close()
    if sts is None: sts = 0
    if text[-1:] == '\n': text = text[:-1]
    return sts, text

def execcmd(*cmd, **kwargs):
    cmdstr = " ".join(cmd)
    if kwargs.get("show"):
        status = os.system(cmdstr)
        output = ""
    else:
        status, output = commands_getstatusoutput(cmdstr)
    if status != 0 and not kwargs.get("noerror"):
        sys.stderr.write(cmdstr)
        sys.stderr.write("\n")
        sys.stderr.write(output)
        raise Error, "command failed: "+cmdstr
    return status, output

def filedigest(filename):
    file = open(filename)
    digest = md5.md5()
    data = file.read(8192)
    while data:
        digest.update(data)
        data = file.read(8192)
    return digest.hexdigest()

def fileisbinary(filename):
    file = open(filename)
    data = file.read(8192)
    file.close()
    if "\x00" in data or \
       "\x01" in data or \
       "\x02" in data or \
       "\x03" in data or \
       "\x04" in data or \
       "\x05" in data:
        return 1
    return 0


# vim:et:ts=4:sw=4
