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

init()

VALUES_TO_AVOID = ['NOASSERTION', 'NONE', 'Match']
SCALE = [('A', 90, Fore.GREEN), ('B', 75, Fore.BLUE), ('C', 55,
         Fore.MAGENTA), ('D', 30, Fore.YELLOW)]
DEFAULT_CODE_LINES = 10
# Percentage value below which a link between an spdx document and a source package is deemed a fail

THRESHOLD_VALUE = 80
MSG = {True: Fore.BLUE + 'Good! The spdx document and the source files match.',
       False: Fore.RED + 'Could not proceed because the source files do not match with the spdx document provided.'}

DEFAULT_CLOC_COMMAND_RESULT = """<?xml version="1.0"?>
<results>
<header>
  <cloc_url>http://cloc.sourceforge.net</cloc_url>
  <cloc_version>1.60</cloc_version>
  <elapsed_seconds>0</elapsed_seconds>
  <n_files>0</n_files>
  <n_lines>0</n_lines>
  <files_per_second>0</files_per_second>
  <lines_per_second>0</lines_per_second>
</header>
<files>
<file name="no/name" blank="0" comment="0" code="0"  language="Python" />
<total blank="0" comment="0" code="0" />
</files>
</results>"""

def progress_bar():
    bar = progressbar.ProgressBar(maxval=20, \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for i in xrange(20):
        bar.update(i+1)
        sleep(0.1)
    bar.finish()

def file_exists(packageCollection, filename):
    item_tags = packageCollection.getElementsByTagName('file')
    file_existence = False
    for item_ in item_tags:
        if item_.hasAttribute('name'):
            item_value = item_.getAttribute('name')
            if filename in item_value:
                file_existence = True
    return file_existence

def get_xml_item_count(
    spdxCollection,
    packageCollection,
    item,
    values_to_avoid,
    tag_to_get,
    ):

    # Takes the xml document element tree, the item to count and the values
    # that should not be included in the count

    item_count = 0
    attribute_value = 0
    sub_item_value = ''
    sub_item_name_value = ''
    item_tags = spdxCollection.getElementsByTagName('item')
    for item_ in item_tags:
        sub_item = item_.getElementsByTagName(item)
        sub_item_name = item_.getElementsByTagName('file')
        if sub_item[0].hasAttribute(tag_to_get):
            sub_item_value = sub_item[0].getAttribute(tag_to_get)
        if sub_item_name[0].hasAttribute(tag_to_get):
            sub_item_name_value = sub_item_name[0].getAttribute(tag_to_get)
        if file_exists(packageCollection, sub_item_name_value):
            if sub_item_value not in values_to_avoid:
                item_count += 1
    return item_count


def get_xml_item_value(collection, tag_to_get):
    attribute_value = 0
    elt_list = collection.getElementsByTagName(tag_to_get)
    if len(elt_list):
        attribute_value = elt_list[0].firstChild.nodeValue
    return attribute_value


def code_line_validator(xml_string, min_code_lines):
    DOMTree = xml.dom.minidom.parseString(xml_string)
    collection = DOMTree.documentElement
    num_source_file = 0
    for file_ in collection.getElementsByTagName('file'):
        if file_.hasAttribute('code'):
            attribute_value = file_.getAttribute('code')
            if int(attribute_value) >= int(min_code_lines):
                num_source_file += 1
    return [xml_string, num_source_file]


def parse_xml_results(spdx_results, package_analysis_results, num_source_files):
    results_dict = {
        'num_license_concluded': 0,
        'num_license_possible': 0,
        'total_num_source_files': 0,
        'total_num_files_with_license': 0,
        }
    # Open XML document

    spdxDOMTree = xml.dom.minidom.parseString(spdx_results)
    spdxcollection = spdxDOMTree.documentElement
    packageDOMTree = xml.dom.minidom.parseString(package_analysis_results)
    packageCollection = packageDOMTree.documentElement

    # Get detail of each useful attribute.

    results_dict['num_license_concluded'] = \
        get_xml_item_count(spdxDOMTree, packageCollection, 'license_concluded',
                           VALUES_TO_AVOID, 'val')
    results_dict['num_license_possible'] = \
        get_xml_item_count(spdxDOMTree, packageCollection, 'license_info', VALUES_TO_AVOID,
                           'val')
    results_dict['total_num_source_files'] = num_source_files

    results_dict['total_num_files_with_license'] = \
        get_xml_item_count(spdxDOMTree, packageCollection, 'license_concluded',
                           VALUES_TO_AVOID, 'val')
    return compute_grade(results_dict)


def grade_string(grade, grade_num, gtype):
    """Dispays the grade with a color following its value; Red for F, Green for A, etc"""
    additional_info = ''
    if grade_num > SCALE[0][1]:
        color = SCALE[0][2]
    elif grade_num > SCALE[1][1]:
        color = SCALE[1][2]
    elif grade_num > SCALE[2][1]:
        color = SCALE[2][2]
    elif grade_num > SCALE[3][1]:
        color = SCALE[3][2]
    else:
        color = Fore.RED
    if gtype == 1:
        additional_info = 'files_with_any_kind_of_license_infos'
    if gtype == 2:
        additional_info = 'files_with_license_concluded'

    print(color + '{0} {1} with {2} %  pass for {3}'.format('GRADE: ', grade, grade_num, additional_info))
    deinit()


def grade_scale(grade_num, gtype):
    if grade_num > SCALE[0][1]:
        return grade_string(SCALE[0][0], grade_num, gtype)
    if grade_num > SCALE[1][1]:
        return grade_string(SCALE[1][0], grade_num, gtype)
    if grade_num > SCALE[2][1]:
        return grade_string(SCALE[2][0], grade_num, gtype)
    if grade_num > SCALE[3][1]:
        return grade_string(SCALE[3][0], grade_num, gtype)
    else:
        return grade_string('F', grade_num, gtype)


def compute_grade(dict_of_values):
    grade1 = "0 %"
    grade2 = "0 %"
    if dict_of_values['total_num_source_files'] > 0:
        grade1 = 100 * (float(dict_of_values['num_license_possible'
                        ]) / float(dict_of_values['total_num_source_files'
                        ]))
        grade2 = 100 * (float(dict_of_values['num_license_concluded'])
                        / float(dict_of_values['total_num_source_files']))
    return (grade_scale(grade2, 2))


def build_xml(spdx_scan_result):
    x = XMLBuilder('spdx_file')
    with x.data:
        for line in spdx_scan_result.splitlines():
            single_line = line.split(',')
            with x.item:
                x.file(val=single_line[0])
                x.license_info(val=single_line[1])
                x.license_concluded(val=single_line[2])
            etree_node = ~x
    return x


def get_number_of_common_files(spdx_scan_results, source_collection):
    item_count = 0
    for item_ in source_collection.getElementsByTagName('file'):
        if item_.hasAttribute('name'):
            attribute_value = item_.getAttribute('name')

            file_link = '/'.join(attribute_value.split('/')[-2:])
            if file_link in spdx_scan_results:
                item_count += 1

    return item_count


def establish_link(spdx_scan_results, source_package_results):
    results_dict = {'total_number_of_files': 0, 'num_common_files': 0}

    # Open XML document

    spdxDOMTree = xml.dom.minidom.parseString(spdx_scan_results)
    sourceDOMTree = xml.dom.minidom.parseString(source_package_results)
    spdx_collection = spdxDOMTree.documentElement
    source_collection = sourceDOMTree.documentElement

    # Get detail of each useful attribute.
    results_dict['num_common_files'] = \
        get_number_of_common_files(spdx_scan_results, source_collection)
    results_dict['total_number_of_files'] = \
        get_xml_item_value(source_collection, 'n_files')
    grade = "0 %"
    if results_dict['total_number_of_files'] != '0':
        grade = 100 * (float(results_dict['num_common_files'])
                       / float(results_dict['total_number_of_files']))
    return grade

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
    # with introduce("Checking Cloc installation: "):
    #     local('sudo apt-get install cloc')
    # with introduce("Checking and installing requriements: "):
    #     local('pip install -r requirements.txt')


@task
def analyse(package="", min_code_lines=DEFAULT_CODE_LINES, run_setup=True):
    """Analyse a source file package USAGE: fab analyse:<source_file_or_package>"""
    with introduce("Analysing the source package: "):
        if run_setup:
            setup()
        # to print ignored files to a file, add --ignored=ignore.txt
        cloc_command_result = local('cloc --xml --force-lang="PHP",in --force-lang="PHP",conf --force-lang="PHP",twig --force-lang="PHP",json --by-file {package}'.format(package=package), capture=True)
        formatted_command_result = ""
        if len(cloc_command_result.split('\n')) < 4:
            formatted_command_result = DEFAULT_CLOC_COMMAND_RESULT
        else:
            formatted_command_result = cloc_command_result.split("\n",4)[4]
        valid_code_lines = code_line_validator(etree.tostring(etree.fromstring(formatted_command_result)), min_code_lines)
        if run_setup:
            print(cloc_command_result)
        else:
            return [cloc_command_result, valid_code_lines[1]]


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
def grade(spdx_file="", package="", min_code_lines=DEFAULT_CODE_LINES):
    """Analyse package and scan an spdx document"""
    with introduce("Analyse and scan: "):
        setup()
        check_results = check(spdx_file=spdx_file, package=package, min_code_lines=min_code_lines, run_setup=False)
        print(MSG[check_results[0]])
        if check_results[0]:
            # XML strings to etree
            spdx_scan_results_root = check_results[1]
            package_analysis_results_root = check_results[2]
            parse_xml_results(etree.tostring(spdx_scan_results_root), etree.tostring(package_analysis_results_root), check_results[3])



@task
def check(spdx_file="", package="", min_code_lines=DEFAULT_CODE_LINES, run_setup=True):
    """Check whether an spdx document points to the real Source package; USAGE: fab check:<spdx_document>,<source_file_or_package>"""
    with introduce("Checking the link between spdx file and package: "):
        if run_setup:
            setup()
        # No need to run setup again in each of the methods below
        spdx_scan_results = scan(spdx_file=spdx_file, run_setup=False)
        package_analysis_results = analyse(package=package, min_code_lines=min_code_lines, run_setup=False)
        # XML strings to etree
        spdx_scan_results_root = etree.fromstring(spdx_scan_results)
        formatted_package_analysis_result = ""
        if len(package_analysis_results[0].split('\n')) < 4:
            formatted_package_analysis_result = DEFAULT_CLOC_COMMAND_RESULT
        else:
            formatted_package_analysis_result = package_analysis_results[0].split("\n",4)[4]
        package_analysis_results_root = etree.fromstring(formatted_package_analysis_result)
        grade = establish_link(etree.tostring(spdx_scan_results_root), etree.tostring(package_analysis_results_root))
        is_valid = grade >= THRESHOLD_VALUE
        if run_setup:
            grade_scale(grade, 1)
        else:
            return [is_valid, spdx_scan_results_root, package_analysis_results_root, package_analysis_results[1]]
