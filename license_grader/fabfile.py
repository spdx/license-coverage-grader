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
from lxml import etree

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


@task
def analyse(package="", run_setup=True):
    """Analyse a source file package USAGE: fab analyse:<source_file_or_package>"""
    with introduce("Analysing the source package: "):
        if run_setup:
            setup()
        # to print ignored files to a file, add --ignored=ignore.txt
        cloc_command_result = local('cloc --xml {package}'.format(package=package), capture=True)
        if run_setup:
            print(cloc_command_result)
        else:
            return cloc_command_result


@task
def scan(spdx_file="", run_setup=True):
    """Scan an spdx document USAGE: fab scan:<spdx_source_file_or_link> """
    with introduce("Scanning the spdx file: "):
        if run_setup:
            setup()
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
        if run_setup:
            print(str(x))
        else:
            return str(x)


@task
def grade(spdx_file="", package=""):
    """Analyse package and scan an spdx document"""
    with introduce("Analyse and scan"):
        setup()
        # No need to run setup again in each of the methods below
        spdx_scan_results = scan(spdx_file=spdx_file, run_setup=False)
        package_analysis_results = analyse(package=package, run_setup=False)
        # XML strings to etree
        spdx_scan_results_root = etree.fromstring(spdx_scan_results)
        package_analysis_results_root = etree.fromstring(package_analysis_results.split("\n",4)[4])
        spdx_scan_results_root.append(package_analysis_results_root)
        print(etree.tostring(spdx_scan_results_root))
