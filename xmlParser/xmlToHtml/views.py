# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render_to_response

import xml.etree.cElementTree as ET

def xml_to_html_parser(request):
	tree = ET.ElementTree(file='CC.xml')

	passage = passage_parser(tree)
	title = title_parser(tree)
	header_data = header_parser(tree)
	team_members = member_parser(tree)

	# company_data = company_data_parser(tree)

	return render_to_response('xmlToHtml/output.html', {'passage' : passage, 'title' : title, 'header_data' : header_data, 'team_members' : team_members})

def passage_parser(tree):
	data_dict = {}

	for elem in tree.iter(tag='TextElement'):
		if elem.attrib['name'] == 'bottom_line':
			data_dict['bottom_line'] = elem.text.strip()
		if elem.attrib['name'] == 'key_points':
			data_dict['key_points'] = elem.text.strip()

	for elem in tree.iter(tag='Title'):
		data_dict['heading'] = elem.text.strip()

	return data_dict

def title_parser(tree):
	data_dict = {}

	for elem in tree.iter(tag='Issuer'):
		data_dict['symbol'] = elem.attrib['symbol']
		data_dict['title'] = elem.attrib['companyName']

	return data_dict

def header_parser(tree):
	data_dict = {}

	try:
		for elem in tree.iter(tag='FinancialValue'):
			if elem.attrib['name'] == 'RATING':
				for child in elem:
					data_dict['rating'] = child.attrib['displayValue']
					break
			if elem.attrib['name'] == 'PRICE':
				for child in elem:
					data_dict['price'] = child.attrib['displayValue']
					break
			if elem.attrib['name'] == 'PRICE_TARGET':
				for child in elem:
					data_dict['target'] = child.attrib['displayValue']
					break
			if elem.attrib['name'] == 'TOTAL_RETURN':
				for child in elem:
					data_dict['total_return'] = child.attrib['displayValue']
					break
	except:
		print 'Key not found'

	for elem in tree.iter(tag='TextElement'):
		if elem.attrib['name'] == 'sector_name_override':
			data_dict['side_title'] = elem.text.strip()

	return data_dict

def member_parser(tree):
	data_dict = {}
	data_dict['members'] = []

	inner_dict = {}

	for elem in tree.iter(tag='TeamMember'):
		inner_dict['name'] = elem[2].text + ' ' + elem[1].text
		inner_dict['role'] = elem[0].text
		inner_dict['position'] = elem[4].text
		inner_dict['email'] = elem[10].text
		inner_dict['phone'] = elem[9].text

		data_dict['members'].append(inner_dict)
		inner_dict = {}

	return data_dict

# def company_data_parser(tree):
	# data_dict = {}

	# try:
	# 	for elem in tree.iter(tag='FinancialValue'):
	# 		if elem.attrib['name'] == 'DIVIDEND':
	# 			data_dict['dividend'] = elem[0].attrib['displayValue']
	# 		if elem.attrib['name'] == 'YIELD_CALC':
	# 			data_dict['yield'] = elem[0].attrib['displayValue']
	# 		if elem.attrib['name'] == 'NAV':
	# 			data_dict['nav'] = elem[0].attrib['displayValue']
	# 		if elem.attrib['name'] == 'SHARES_OUT':
	# 			data_dict['shares'] = elem[0].attrib['displayValue']
	# 		if elem.attrib['name'] == 'MKT_CAP_CALC':
	# 			data_dict['market_cap'] = elem[0].attrib['displayValue']
	# 		if elem.attrib['name'] == 'P_NAV':
	# 			data_dict['p_nav'] = elem[0].attrib['displayValue']
	# except:
	# 	print 'Key not found'

	# return data_dict
