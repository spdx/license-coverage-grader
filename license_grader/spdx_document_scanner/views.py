# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from __future__ import print_function
from argparse import ArgumentParser

import Levenshtein as lev
import copy
import sys
import csv

class spdxdata(object):
    def __init__(self, fname):
        self.fname = fname
        self.parser = ""
        self.filerefs = {}
        self.files = set()

class filedata(object):
    def __init__(self, fname, info=None):
        self.fname = fname
        self.licinfo = []
        self.concluded = ""
        if info:
            self.licinfo.append(info)

# Trivial SPDX scan
def read_spdx(filename, spdx):
    with open(filename) as f:
        fname = None
        for line in f.readlines():

            parts = line.split(":", 1)
            key = parts[0].strip()

            if key == 'Creator':
                parts = line.split(":", 2)
                if parts[1].strip() == 'Tool':
                    spdx.parser = parts[2].strip()

            if key == 'FileName':
                if (fname):
                    spdx.filerefs[fname] = fdata

                fname = parts[1].strip().split('/', 1)[1].strip().replace(",", "%2C")
                fdata = filedata(fname)

            if key == 'LicenseConcluded':
                lic = parts[1].strip()
                if lic == 'NONE':
                    lic = 'NOASSERTION'
                fdata.concluced = lic

            if key == 'LicenseInfoInFile':
                lic = parts[1].strip()
                if lic == 'NONE':
                    lic = 'NOASSERTION'
                if lic not in fdata.licinfo:
                    fdata.licinfo.append(lic)

        if fname:
            spdx.filerefs[fname] = fdata

# LID CSV scan
def read_csv(filename, spdx):

    spdx.parser = 'LID'

    with open(filename) as f:
        rdr = csv.reader(f)
        i = 0

        for row in rdr:
            i += 1
            if i == 1:
                continue

            fn = row[0].split('/', 1)[1].strip().replace(",", "%2C")
            lic = row[1]

            fd = spdx.filerefs.pop(fn, filedata(fn))
            if lic not in fd.licinfo:
                fd.licinfo.append(lic)
            spdx.filerefs[fn] = fd

def diff_spdx(spdxfiles, totfiles, windcrap):

    spdx = {}
    files = set()

    t = "Tool %d" %totfiles
    for spf in spdxfiles:
        s = spdxdata(spf)

        if spf.endswith(".spdx"):
            read_spdx(spf, s)
        else:
            read_csv(spf, s)

        s.files = set(sorted(s.filerefs.keys()))
        files = files | s.files
        spdx[spf] = s
        t += "," + s.parser + ":%d" %(len(s.files))

    t += ",Match"

    print(t)

    if windcrap:
        # Sanitize windrivel output which drops '/'
        # from the middle of the file path
        #
        # Are there any functional tools out there?
        #
        # This certainly can be done smarter, but WTF
        sanitize = { }
        for src in sorted(files):
            if src in sanitize:
                continue
            for crap in sorted(files):
                if crap in sanitize:
                    continue

                if len(src) - len(crap) != 1:
                    continue

                ops = lev.opcodes(src, crap)
                if len(ops) != 3:
                    continue

                #arch/arc/cpu/arc700/u-boot.lds -> arch/arc/cpu/arc700u-boot.lds
                #[('equal', 0, 19, 0, 19), ('delete', 19, 20, 19, 19), ('equal', 20, 30, 19, 29)]
                if ops[0][0] != 'equal' or ops[1][0] != 'delete' or ops[2][0] != 'equal':
                    continue
                if ops[1][1] != ops[1][3] or ops[1][1] != ops[1][4]:
                    continue
                if ops[1][2] - ops[1][1] != 1:
                    continue
                if src[ops[1][1]] != '/':
                    continue

                sanitize[crap] = src

            files = set()
            sanset = set(sanitize.keys())
            for spf in spdxfiles:
                s = spdx[spf]
                for crap in sanset & s.files:
                    ref = s.filerefs.pop(crap)
                    src = sanitize[crap]
                    ref.fname = src
                    s.filerefs[src] = ref
                s.files = set(sorted(s.filerefs.keys()))
                files = files | s.files

    for src in sorted(files):
        info = src
        lics = None
        match = "Y"
        for spf in spdxfiles:
            li = spdx[spf].filerefs.get(src, filedata(src, 'NOTSCANNED')).licinfo
            if not lics:
                lics = copy.copy(li)
            elif set(lics) != set(li):
                match = "N"

            info += "," + li.pop()
            for l in li:
                info += " " + l

        print(info + "," + match)

if __name__ == '__main__':
    parser = ArgumentParser(description = 'Diff of two or more SPDX files')
    parser.add_argument('filenames', metavar = 'file', nargs = '+',
                        help = 'list of source URIs, minimum 2')
    parser.add_argument("-s", "--sourcefiles", type=int, default=0,
                    help="Number of files in the source")
    parser.add_argument("-w", "--windcrap", action='store_true',
                    help="Sanitize windrivel filenames")

    args = parser.parse_args()

    if len(args.filenames) < 1:
        print("Not enough SPDX files\n")
        sys.exit(1)

    diff_spdx(args.filenames, args.sourcefiles, args.windcrap)
