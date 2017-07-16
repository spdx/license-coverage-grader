#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render
from xml.dom.minidom import parse, parseString
import xml.dom.minidom
from xmlbuilder import XMLBuilder
from colorama import Fore, Back, Style
from colorama import init, deinit
init()

VALUES_TO_AVOID = ['NOASSERTION', 'NONE']
SCALE = [('A', 90, Fore.GREEN), ('B', 75, Fore.BLUE), ('C', 55,
         Fore.MAGENTA), ('D', 30, Fore.YELLOW)]

# Percentage value below which a link between an spdx document and a source package is deemed a fail

THRESHOLD_VALUE = 80
MSG = {True: 'Good! The spdx document and the source files match.',
       False: 'Could not proceed because the source files do not match with the spdx document provided.'}


def get_xml_item_count(
    collection,
    item,
    values_to_avoid,
    tag_to_get,
    ):

    # Takes the xml document element tree, the item to count and the values
    # that should not be included in the count

    item_count = 0
    attribute_value = 0
    for item_ in collection.getElementsByTagName(item):
        if item_.hasAttribute(tag_to_get):
            attribute_value = item_.getAttribute(tag_to_get)
            if attribute_value not in values_to_avoid:
                item_count += 1
    return item_count


def get_xml_item_value(collection, tag_to_get):
    attribute_value = 0
    elt_list = collection.getElementsByTagName(tag_to_get)
    if len(elt_list):
        attribute_value = elt_list[0].firstChild.nodeValue
    return attribute_value


def parse_xml_results(xml_string):
    results_dict = {
        'num_license_concluded': 0,
        'num_license_possible': 0,
        'total_num_source_files': 0,
        'total_num_files_with_license': 0,
        }

    # Open XML document

    DOMTree = xml.dom.minidom.parseString(xml_string)
    collection = DOMTree.documentElement
    if collection.hasAttribute('shelf'):
        print 'Root element : %s' % collection.getAttribute('shelf')

    # Get detail of each useful attribute.

    results_dict['num_license_concluded'] = \
        get_xml_item_count(collection, 'license_concluded',
                           VALUES_TO_AVOID, 'val')
    results_dict['num_license_possible'] = \
        get_xml_item_count(collection, 'license_info', VALUES_TO_AVOID,
                           'val')
    results_dict['total_num_source_files'] = \
        get_xml_item_value(collection, 'n_files')
    results_dict['total_num_files_with_license'] = \
        get_xml_item_count(collection, 'license_concluded',
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

    print color + '{0} {1} with {2} %  pass for {3}'.format('GRADE: ', grade, grade_num, additional_info)
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
    grade1 = 100 * (float(dict_of_values['total_num_files_with_license'
                    ]) / float(dict_of_values['total_num_source_files'
                    ]))
    grade2 = 100 * (float(dict_of_values['num_license_concluded'])
                    / float(dict_of_values['total_num_source_files']))
    return (grade_scale(grade1, 1), (grade_scale(grade2, 2)))


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
    grade = 100 * (float(results_dict['num_common_files'])
                   / float(results_dict['total_number_of_files']))
    return grade
