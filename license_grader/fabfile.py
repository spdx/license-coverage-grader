from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from contextlib import contextmanager, nested
import os
import platform
import sys
import time
from fabric.api import env, local, task, warn_only
from xmlbuilder import XMLBuilder
from xml.etree import ElementTree as et
from lxml import etree
from django.shortcuts import render
from xml.dom.minidom import parse, parseString
import xml.dom.minidom
from xmlbuilder import XMLBuilder
from colorama import Fore, Back, Style
from colorama import init, deinit
from xml_result_parser.utils import AnalysePackage, ScanSpdx, CheckPackage, GradePackage

DEFAULT_CODE_LINES = 0

@contextmanager
def introduce(intro_comment):
    """Status decorate an event."""
    start_time = time.time()
    introducer_dict = {}

    def timer():
        return str(time.time() - start_time) + " seconds"
    try:
        yield introducer_dict
    except:
        print(intro_comment + timer())
        raise
    else:
        if not introducer_dict:
            print(intro_comment + timer())
        else:
            print(intro_comment + timer())


@task
def setup():
    # Sets up the project, installs the necessary utilities so that commands do not fail
    """Setup the project"""
    with introduce("Checking Cloc installation: "):
        local('sudo apt-get install cloc')
    with introduce("Checking and installing requriements: "):
        local('pip install -r requirements.txt')


@task
def analyse(package="", min_code_lines=DEFAULT_CODE_LINES):
    """Analyse a source file package USAGE: fab analyse:<source_file_or_package>"""
    with introduce("Analysing the source package: "):
        analyse_obj = AnalysePackage(package, min_code_lines)
        analyse_obj.analyse()


@task
def scan(spdx_file=""):
    """Scan an spdx document USAGE: fab scan:<spdx_source_file_or_link> """
    with introduce("Scanning the spdx file: "):
        scan_obj = ScanSpdx(spdx_file)
        scan_obj.scan()


@task
def grade(spdx_file="", package="", min_code_lines=DEFAULT_CODE_LINES):
    """Analyse package and scan an spdx document"""
    with introduce("Analyse and scan: "):
        grade_obj = GradePackage(spdx_file, package, min_code_lines)
        grade_results = grade_obj.grade()


@task
def check(spdx_file="", package="", min_code_lines=DEFAULT_CODE_LINES):
    """Check whether an spdx document points to the real Source package; USAGE: fab check:<spdx_document>,<source_file_or_package>"""
    with introduce("Checking the link between spdx file and package: "):
        check_obj = CheckPackage(spdx_file, package, min_code_lines)
        check_obj.check()
