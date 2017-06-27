# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from xml.dom.minidom import parse, parseString
import xml.dom.minidom

# Open XML document
DOMTree = xml.dom.minidom.parse("spdx_package_analysis_results.xml")
collection = DOMTree.documentElement
if collection.hasAttribute("shelf"):
   print "Root element : %s" % collection.getAttribute("shelf")

# Get all the values in the collection
sum = collection.getElementsByTagName("total")

# Get detail of each useful attribute.
for total in sum:
   if total.hasAttribute("sum_files"):
      num_source_files = total.getAttribute("sum_files")
      
#Counting all file tags from spdx scanned
num_total_files = len(collection.getElementsByTagName('item'))

num_license_concluded = 0
for license_conclude in collection.getElementsByTagName('license_concluded'):
	if license_conclude.hasAttribute('val'):
		attribute_value = license_conclude.getAttribute('val')
		if attribute_value not in ["NOASSERTION", "NONE"]:
			num_license_concluded += 1

num_license_possible = 0
for license_conclude in collection.getElementsByTagName('license_info'):
	if license_conclude.hasAttribute('val'):
		attribute_value = license_conclude.getAttribute('val')
		if attribute_value not in ["NOASSERTION", "NONE"]:
			num_license_possible += 1