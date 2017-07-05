# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from xml.dom.minidom import parse, parseString
import xml.dom.minidom

VALUES_TO_AVOID = ["NOASSERTION", "NONE"]

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
    results_dict['total_num_files_with_license'] = get_xml_item_count(collection, 'file', VALUES_TO_AVOID)
    print(results_dict)


#  print “%s: %c -> %c  %n source file in %n total “ file, 
#  grade_scale(100 *num_license_concluded / num_source_files), 
#  grade_scale (num_license_possible / num_source_files ) num_source_files, num_total_files;

