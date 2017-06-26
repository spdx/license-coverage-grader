
"""
Fabric file to standardize our dev process.
1. Run the dev setup with: $ fab debug. For postgres. fab debug:psql
2. Run the prod setup with: $ fab prod. For postgres. fab prod:psql
3. Remember to stop the servers, with $ fab stop

All Rights Reserved. Hadron Tech LLC 2016.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from contextlib import contextmanager, nested
import os
import platform
import sys
import time
from fabric.api import env, local, task, warn_only
from colorama import Back, Fore, Style, init
from xmlbuilder import XMLBuilder
from xml.etree import ElementTree as et
# Launch tasks here.

IS_WIN = platform.system().lower().startswith("win")

IS_TTY = sys.stdout.isatty()

STATUS_MARK = u'\u2712' * IS_TTY
X_MARK = u'\u2718' * IS_TTY
CHECK_MARK = u'\u2714' * IS_TTY
WARNING_MARK = u"\u26A0" * IS_TTY
NOTE_MARK = u'\u2710' * IS_TTY

def W(string, prefix=" "):
    """Returns "" if this platform is WIN."""
    return "" if IS_WIN else prefix + string

def _fprint(bg, status, message):
    print(Fore.WHITE + Style.BRIGHT + bg + " " + status + " ", end="")
    print(Fore.WHITE + Style.BRIGHT + " " + message)


def warn(message):
    _fprint(Back.BLACK, "WARNING", message + W(Fore.YELLOW + WARNING_MARK))


def success(message):
    _fprint(Back.BLACK, "SUCCESS", message + W(Fore.GREEN + CHECK_MARK))


def note(message):
    _fprint(Back.BLACK, " NOTE  ", message + W(Fore.CYAN + NOTE_MARK))


def error(message):
    _fprint(Back.BLACK, " ERROR ", message + W(Fore.RED + X_MARK))


@contextmanager
def introduce(what):
    """Status decorate an event."""
    start_time = time.time()
    introducer_dict = {}

    def timer():
        return str(time.time() - start_time) + " seconds"

    print(Fore.WHITE + Back.BLACK + Style.BRIGHT + "  START  ", end="")
    print(Fore.WHITE + Style.BRIGHT + W(STATUS_MARK) + " " + what)
    try:
        yield introducer_dict
    except:
        error(what + timer())
        raise
    else:
        if not introducer_dict:
            success(what + timer())
        else:
            warn(what + timer())

@task
def setup():
    # Sets up the project, installs the necessary utilities so that commands do not fail
    """Setup the project"""
    with introduce("Checking Cloc installation: "):
        local('sudo apt-get install cloc')
    with introduce("Checking and installing requriements: "):
        local('pip install -r requirements.txt')
    with introduce("Check for libxml installation"):
        local('pip install xmlbuilder')


@task
def analyse(package=""):
    """Analyse a source file package USAGE: fab analyse:<source_file_or_package>"""
    with introduce("Analysing the source package: "):
        cloc_command_result = local('cloc --xml {package}'.format(package=package), capture=True)
        print(cloc_command_result)

@task
def scan(spdx_file=""):
    """Scan an spdx document USAGE: fab scan:<spdx_source_file_or_link> """
    with introduce("Scanning the spdx file: "):
        spdx_scan_result = local('python -s spdx_scanner.py -s 10571 -w {spdx_file}'.format(spdx_file=spdx_file), capture=True)
        x = XMLBuilder('spdx_file')
        with x.data:
            for line in spdx_scan_result.splitlines():
                single_line = line.split(',')
                with x.item:
                    x.file(val=single_line[0])
                    x.license_info(val=single_line[1])
                    x.license_concluded(val=single_line[2])
                etree_node = ~x
        print(str(x))

def combine_xml(files):
    first = None
    for filename in files:
        # data = et.parse(filename).getroot()
        data = filename
        if first is None:
            first = data
        else:
            first.extend(data)
        print(data)
    if first is not None:
        return et.tostring(first)

@task
def cover(spdx_file="", package=""):
    """Analyse package and scan an spdx document"""
    with introduce("Analyse and scan"):
        setup()
        spdx_scan_results = scan(spdx_file=spdx_file)
        package_analysis_results = analyse(package=package)
        # Merge the two results
        # combined_results = combine_xml([spdx_scan_results, package_analysis_results])
        # print(combined_results)
        print(type(spdx_scan_results), type(package_analysis_results))
