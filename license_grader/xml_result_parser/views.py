# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from xml.dom.minidom import parse, parseString
import xml.dom.minidom
from xmlbuilder import XMLBuilder
from colorama import Fore, Back, Style
from colorama import init, deinit
init()

VALUES_TO_AVOID = ["NOASSERTION", "NONE"]
SCALE = [('A', 90, Fore.GREEN), ('B', 75, Fore.BLUE), ('C', 55, Fore.MAGENTA), ('D', 30, Fore.YELLOW)]


def get_xml_item_count(collection, item, values_to_avoid):
    # Takes the xml document element tree, the item to count and the values
    # that should not be included in the count
    item_count = 0
    for item_ in collection.getElementsByTagName(item):
    	if item_.hasAttribute('val'):
    		attribute_value = item_.getAttribute('val')
    		if attribute_value not in values_to_avoid:
    			item_count += 1
    return item_count

def parse_xml_results(xml_string):
    results_dict = {
    'num_license_concluded': 0,
    'num_license_possible': 0,
    'total_num_files': 0,
    'total_num_files_with_license': 0
    }
    # Open XML document
    DOMTree = xml.dom.minidom.parseString(xml_string)
    collection = DOMTree.documentElement
    if collection.hasAttribute("shelf"):
       print "Root element : %s" % collection.getAttribute("shelf")

    # Get detail of each useful attribute.
    results_dict['num_license_concluded'] = get_xml_item_count(collection, 'license_concluded', VALUES_TO_AVOID)
    results_dict['num_license_possible'] = get_xml_item_count(collection, 'license_info', VALUES_TO_AVOID)
    results_dict['total_num_files'] = get_xml_item_count(collection, 'file', [])
    results_dict['total_num_files_with_license'] = get_xml_item_count(collection, 'license_concluded', VALUES_TO_AVOID)
    return compute_grade(results_dict)

def grade_string(grade, grade_num):
    """Dispays the grade with a color following its value; Red for F, Green for A, etc"""
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
    print(color + '{0} {1}; ({2} %)'.format('GRADE: ', grade, grade_num))
    deinit()

def grade_scale(grade_num):
    if grade_num > SCALE[0][1]:
        return grade_string(SCALE[0][0], grade_num)
    if grade_num > SCALE[1][1]:
        return grade_string(SCALE[1][0], grade_num)
    if grade_num > SCALE[2][1]:
        return grade_string(SCALE[2][0], grade_num)
    if grade_num > SCALE[3][1]:
        return grade_string(SCALE[3][0], grade_num)
    else:
        return grade_string('F', grade_num)

def compute_grade(dict_of_values):
    grade = 100 * (float(dict_of_values['total_num_files_with_license']) / float(dict_of_values['total_num_files']))
    return grade_scale(grade)

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
