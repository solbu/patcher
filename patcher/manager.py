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
from patcher.util import execcmd, filedigest, fileisbinary
import shutil
import sys, os

PATCHERDIR = ".patcher"

class Manager(object):

    def __init__(self, dir="."):
        self.dir = dir;
        self.patcherdir = os.path.join(dir, PATCHERDIR)
        self.pristinedir = os.path.join(dir, PATCHERDIR, "pristine")
        self.digestfilepath = os.path.join(self.patcherdir, "digest")
        self.ignorefilepath = os.path.join(self.patcherdir, "ignore")
        self.submanagers = {}
        self.digests = {}
        self.ignores = {}

        # Collect existent submanagers
        if os.path.isdir(self.patcherdir):
            for entry in os.listdir(self.dir):
                entrypath = os.path.join(self.dir, entry)
                if entry == PATCHERDIR or not os.path.isdir(entrypath):
                    continue
                if os.path.isdir(os.path.join(entrypath, PATCHERDIR)):
                    manager = Manager(entrypath)
                    self.submanagers[entry] = manager

        # Collect existent digests
        if os.path.isfile(self.digestfilepath):
            file = open(self.digestfilepath)
            for line in file.readlines():
                entry, digest = line.rsplit(None, 1)
                self.digests[entry] = digest
            file.close()

        # Collect existent ignores
        if os.path.isfile(self.ignorefilepath):
            file = open(self.ignorefilepath)
            for entry in file.read().split():
                self.ignores[entry] = True
            file.close()

    def start(self, empty=False, nofiles=False):
        if not os.path.isdir(self.patcherdir):
            os.mkdir(self.patcherdir)
            os.mkdir(self.pristinedir)
        digestfile = open(self.digestfilepath, "a")
        ignorefile = open(self.ignorefilepath, "a")
        for entry in os.listdir(self.dir):
            if entry[0] == ".":
                continue
            entrypath = os.path.join(self.dir, entry)
            pristinepath = os.path.join(self.pristinedir, entry)
            if os.path.isfile(entrypath):
                if not os.path.isfile(pristinepath) and not nofiles:
                    if empty:
                        open(pristinepath, "w").close()
                    else:
                        shutil.copy2(entrypath, pristinepath)
                    digest = filedigest(pristinepath)
                    digestfile.write("%s %s\n" % (entry, digest))
                    self.digests[entry] = digest
                    if fileisbinary(pristinepath):
                        ignorefile.write("%s\n" % entry)
                        self.ignores[entry] = 1
            elif os.path.isdir(entrypath):
                if entry not in self.submanagers:
                    manager = Manager(entrypath)
                    manager.start(empty, nofiles)
                    self.submanagers[entry] = manager
        ignorefile.close()
        digestfile.close()

    def stop(self):
        self.started(fail=True)
        shutil.rmtree(self.patcherdir)
        for manager in self.submanagers.values():
            manager.stop()
        self.submanagers = {}

    def add(self, entries=[], empty=False, nofiles=False):
        if not entries:
            if self.started():
                raise Error, "found existent pristine for '%s'" % self.dir
            self.start(empty, nofiles)
            return [self.dir]
        self.started(fail=True)
        digestfile = open(self.digestfilepath, "a")
        ignorefile = open(self.ignorefilepath, "a")
        passedpaths = []
        # First check every file
        for entry in entries:
            entrypath = os.path.join(self.dir, entry)
            pristinepath = os.path.join(self.pristinedir, entry)
            if entrypath.startswith("./"):
                entrypath = entrypath[2:]
            if pristinepath.startswith("./"):
                pristinepath = pristinepath[2:]
            if os.path.isfile(pristinepath):
                raise Error, "found existent pristine for '%s'" % entrypath
            if not os.path.isfile(entrypath):
                raise Error, "file not found: %s" % entrypath
            passedpaths.append((entry, entrypath, pristinepath))
        # Then add them
        for entry, entrypath, pristinepath in passedpaths:
            if empty:
                open(pristinepath, "w").close()
            else:
                shutil.copy2(entrypath, pristinepath)
            digest = filedigest(pristinepath)
            digestfile.write("%s %s\n" % (entry, digest))
            self.digests[entry] = digest
            if fileisbinary(pristinepath):
                ignorefile.write("%s\n" % entry)
                self.ignores[entry] = 1
        ignorefile.close()
        digestfile.close()
        return [x[0] for x in passedpaths]

    def remove(self, entries=[]):
        if not entries:
            if not self.started():
                raise Error, "pristine not found for '%s'" % self.dir
            self.stop()
            return [self.dir]
        self.started(fail=True)
        passedpaths = []
        # First check every file
        for entry in entries:
            entrypath = os.path.join(self.dir, entry)
            pristinepath = os.path.join(self.pristinedir, entry)
            if entrypath.startswith("./"):
                entrypath = entrypath[2:]
            if pristinepath.startswith("./"):
                pristinepath = pristinepath[2:]
            if not os.path.isfile(pristinepath):
                raise Error, "pristine not found for '%s'" % entrypath
            passedpaths.append((entry, entrypath, pristinepath))
        # Then remove them
        for entry, entrypath, pristinepath in passedpaths:
            os.unlink(pristinepath)
            if entry in self.ignores:
                del self.ignores[entry]
            if entry in self.digests: # Should always have
                del self.digests[entry]
        digestfile = open(self.digestfilepath, "w")
        for entry, digest in self.digests.items():
            digestfile.write("%s %s\n" % (entry, digest))
        digestfile.close()
        ignorefile = open(self.ignorefilepath, "w")
        ignorefile.write("\n".join(self.ignores.keys()))
        ignorefile.close()
        return [x[1] for x in passedpaths]

    def stop(self):
        self.started(fail=True)
        shutil.rmtree(self.patcherdir)
        for manager in self.submanagers.values():
            manager.stop()
        self.submanagers = {}

    def diff(self, entries=[], recursive=True):
        self.started(fail=True)
        recurse = False
        if not entries:
            recurse = True
            entries = os.listdir(self.pristinedir)
            entries.sort()
        for entry in entries:
            if entry in self.ignores:
                continue
            entrypath = os.path.join(self.dir, entry)
            pristinepath = os.path.join(self.pristinedir, entry)
            if entrypath.startswith("./"):
                entrypath = entrypath[2:]
            if pristinepath.startswith("./"):
                pristinepath = pristinepath[2:]
            if os.path.isfile(entrypath) and self.changed(entry):
                print "Index:", entrypath
                print "="*67
                sys.stdout.flush()
                execcmd("diff -u -L", entrypath, pristinepath, entrypath,
                        noerror=1, show=1)
        if recursive and recurse:
            for manager in self.submanagers.values():
                manager.diff()

    def revert(self, entries=[], recursive=True):
        self.started(fail=True)
        reverted = []
        recurse = False
        if not entries:
            recurse = True
            entries = os.listdir(self.pristinedir)
            entries.sort()
        for entry in entries:
            entrypath = os.path.join(self.dir, entry)
            pristinepath = os.path.join(self.pristinedir, entry)
            if entrypath.startswith("./"):
                entrypath = entrypath[2:]
            if pristinepath.startswith("./"):
                pristinepath = pristinepath[2:]
            if os.path.isfile(pristinepath):
                if self.changed(entry):
                    shutil.copy(pristinepath, entrypath)
                    reverted.append(entry)
            else:
                raise Error, "nothing known about '%s'" % entrypath
        if recursive and recurse:
            for manager in self.submanagers.values():
                reverted.extend(manager.revert())
        return reverted

    def status(self, entries=[], recursive=True):
        self.started(fail=True)
        status = []
        recurse = False
        if not entries:
            recurse = True
            entries = os.listdir(self.dir)
            entries.extend([x for x in os.listdir(self.pristinedir)
                               if x not in entries])
            entries.sort()
        for entry in entries:
            if entry == PATCHERDIR:
                continue
            entrypath = os.path.join(self.dir, entry)
            pristinepath = os.path.join(self.pristinedir, entry)
            if entrypath.startswith("./"):
                entrypath = entrypath[2:]
            if pristinepath.startswith("./"):
                pristinepath = pristinepath[2:]
            ignored = entry in self.ignores
            if not os.path.exists(entrypath) and \
               not os.path.exists(pristinepath):
                raise Error, "entry not found: %s" % entrypath
            elif os.path.isdir(entrypath):
                if not os.path.isdir(os.path.join(entrypath, PATCHERDIR)):
                    status.append(("?", entrypath))
            elif not ignored:
                if not os.path.isfile(pristinepath):
                    status.append(("?", entrypath))
                elif not os.path.isfile(entrypath):
                    status.append(("!", entrypath))
                elif self.changed(entry):
                    status.append(("M", entrypath))
                else:
                    status.append(("_", entrypath))
        if recursive and recurse:
            for manager in self.submanagers.values():
                status.extend(manager.status())
        return status

    def ignore(self, entries=[], recursive=True):
        self.started(fail=True)
        recurse = False
        if not entries:
            recurse = True
            entries = os.listdir(self.pristinedir)
        ignorefile = open(self.ignorefilepath, "a")
        for entry in entries:
            entrypath = os.path.join(self.dir, entry)
            pristinepath = os.path.join(self.pristinedir, entry)
            if entrypath.startswith("./"):
                entrypath = entrypath[2:]
            if pristinepath.startswith("./"):
                pristinepath = pristinepath[2:]
            if not os.path.isfile(pristinepath):
                raise Error, "nothing known about '%s'" % entrypath
            if entry not in self.ignores:
                ignorefile.write("%s\n" % entry)
                self.ignores[entry] = True
        if recursive and recurse:
            for manager in self.submanagers.values():
                manager.ignore()
        ignorefile.close()

    def unignore(self, entries=[], recursive=True):
        self.started(fail=True)
        recurse = False
        if not entries:
            recurse = True
            self.ignores = {}
        else:
            for entry in entries:
                try:
                    del self.ignores[entry]
                except KeyError:
                    pass
        ignorefile = open(self.ignorefilepath, "w")
        ignorefile.write("\n".join(self.ignores.keys()))
        ignorefile.close()
        if recursive and recurse:
            for manager in self.submanagers.values():
                manager.unignore()

    def started(self, fail=True):
        if not os.path.isdir(self.patcherdir):
            if fail:
                raise Error, "no control directory in '%s'" % self.dir
            return False
        return True

    def ignored(self):
        self.started(fail=True)
        return self.ignores

    def changed(self, entry):
        entrypath = os.path.join(self.dir, entry)
        if entry not in self.digests:
            return False
        if not os.path.isfile(entrypath):
            return True
        if self.digests[entry] != filedigest(entrypath):
            return True
        return False

# vim:et:ts=4:sw=4
