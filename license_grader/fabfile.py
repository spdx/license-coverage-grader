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
from xml_result_parser.views import parse_xml_results, build_xml, establish_link, THRESHOLD_VALUE, grade_scale, MSG

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
def analyse(package="", run_setup=True):
    """Analyse a source file package USAGE: fab analyse:<source_file_or_package>"""
    with introduce("Analysing the source package: "):
        if run_setup:
            setup()
        # to print ignored files to a file, add --ignored=ignore.txt
        cloc_command_result = local('cloc --xml --by-file {package}'.format(package=package), capture=True)
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
        spdx_scan_result = local('python -s spdx_scanner.py -s 10571 {spdx_file}'.format(spdx_file=spdx_file), capture=True)
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
    with introduce("Analyse and scan: "):
        setup()
        check_results = check(spdx_file=spdx_file, package=package, run_setup=False)
        print(MSG[check_results[0]])
        if check_results[0]:
            # XML strings to etree
            spdx_scan_results_root = check_results[1]
            package_analysis_results_root = check_results[2]
            spdx_scan_results_root.append(package_analysis_results_root)
            results_string = etree.tostring(spdx_scan_results_root)
            parse_xml_results(results_string)



@task
def check(spdx_file="", package="", run_setup=True):
    """Check whether an spdx document points to the real Source package; USAGE: fab check:<spdx_document>,<source_file_or_package>"""
    with introduce("Checking the link between spdx file and package: "):
        if run_setup:
            setup()
        # No need to run setup again in each of the methods below
        spdx_scan_results = scan(spdx_file=spdx_file, run_setup=False)
        package_analysis_results = analyse(package=package, run_setup=False)
        # XML strings to etree
        spdx_scan_results_root = etree.fromstring(spdx_scan_results)
        package_analysis_results_root = etree.fromstring(package_analysis_results.split("\n",4)[4])
        grade = establish_link(etree.tostring(spdx_scan_results_root), etree.tostring(package_analysis_results_root))
        is_valid = grade >= THRESHOLD_VALUE
        if run_setup:
            grade_scale(grade, 1)
        else:
            return [is_valid, spdx_scan_results_root, package_analysis_results_root]
