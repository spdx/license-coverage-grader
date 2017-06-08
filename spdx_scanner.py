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