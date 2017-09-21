# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response

import xml.etree.cElementTree as ET


def xml_to_html_parser(request):
    tree = ET.ElementTree(file='CC.xml')

    passage = passage_parser(tree)
    title = title_parser(tree)
    header_data = header_parser(tree)
    team_members = member_parser(tree)

    company_data = company_data_parser(tree)
    bmo_estimates = bmo_estimates_parser(tree)
    consensus_estimates = consensus_estimates_parser(tree)
    valuation = valuation_parser(tree)
    eps = eps_parser(tree)
    sidebar_stuff = sidebar_stuff_parser(tree)

    income_statement = income_statement_parser(tree)
    cash_flow_statement = cash_flow_statement_parser(tree)
    balance_sheet = balance_sheet_parser(tree)
    key_metrics = key_metrics_parser(tree)

    footer_stuff = footer_parser(tree)

    footer_constant_stuff = footer_constant_stuff_parser(tree)

    return render_to_response(
        'xmlToHtml/output.html',
        {
            'passage': passage,
            'title': title,
            'header_data': header_data,
            'company_data': company_data,
            'bmo_estimates' : bmo_estimates,
            'consensus_estimates' : consensus_estimates,
            'valuation' : valuation,
            'eps' : eps,
            'sidebar_stuff' : sidebar_stuff,
            'team_members': team_members,
            'income_statement' : income_statement,
            'cash_flow_statement' : cash_flow_statement,
            'balance_sheet' : balance_sheet,
            'key_metrics' : key_metrics,
            'footer_stuff': footer_stuff,
            'footer_constant_stuff' : footer_constant_stuff
        })


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


def company_data_parser(tree):
    data_dict = {}

    try:
        for elem in tree.iter(tag='FinancialValue'):
            if elem.attrib['name'] == 'DIVIDEND':
                data_dict['dividend'] = elem[0].attrib['displayValue']
            if elem.attrib['name'] == 'YIELD_CALC':
                data_dict['yield'] = elem[0].attrib['displayValue']
            if elem.attrib['name'] == 'NAV':
                data_dict['nav'] = elem[0].attrib['displayValue']
            if elem.attrib['name'] == 'SHARES_OUT':
                data_dict['shares'] = elem[0].attrib['displayValue']
            if elem.attrib['name'] == 'MKT_CAP_CALC':
                data_dict['market_cap'] = elem[0].attrib['displayValue']
            if elem.attrib['name'] == 'P_NAV':
                data_dict['p_nav'] = elem[0].attrib['displayValue']
    except:
        print 'Key not found'

    return data_dict


def footer_parser(tree):
    data_dict = {}

    for elem in tree.iter(tag='Disclaimer'):
        if elem.attrib['code'] == 'REG_AC':
            data_dict['certification'] = elem.text.strip()

    data_dict['disclosures'] = []

    for elem in tree.iter(tag='Disclosure'):
        data_dict['disclosures'].append(elem.text.strip())

    for elem in tree.iter(tag='BoilerPlate'):
        if elem.attrib['name'] == 'Methodology':
            data_dict['methodology'] = elem.text.strip()
        if elem.attrib['name'] == 'Risks':
            data_dict['risks'] = elem.text.strip()

    return data_dict


def bmo_estimates_parser(tree):
	data_dict = {}

	for elem in tree.iter(tag='FinancialModel'):
		if elem.attrib['name'].find('BMO Estimates') > -1:
			for values in elem:
				data_dict[values.attrib['name']] = {}
				for value in values:
					if value.attrib['year'] == '2016' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2016'] = value.attrib['displayValue']
					if value.attrib['year'] == '2017' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2017'] = value.attrib['displayValue']
					if value.attrib['year'] == '2018' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2018'] = value.attrib['displayValue']

	return data_dict


def consensus_estimates_parser(tree):
	data_dict = {}

	for elem in tree.iter(tag='FinancialModel'):
		if elem.attrib['name'].find('Consensus Estimates') > -1:
			for values in elem:
				data_dict[values.attrib['name']] = {}
				for value in values:
					if value.attrib['year'] == '2016' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2016'] = value.attrib['displayValue']
					if value.attrib['year'] == '2017' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2017'] = value.attrib['displayValue']
					if value.attrib['year'] == '2018' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2018'] = value.attrib['displayValue']

	return data_dict

def valuation_parser(tree):
	data_dict = {}

	for elem in tree.iter(tag='FinancialModel'):
		if elem.attrib['name'].find('Valuation') > -1:
			for values in elem:
				data_dict[values.attrib['name']] = {}
				for value in values:
					if value.attrib['year'] == '2016' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2016'] = value.attrib['displayValue']
					if value.attrib['year'] == '2017' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2017'] = value.attrib['displayValue']
					if value.attrib['year'] == '2018' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2018'] = value.attrib['displayValue']

	return data_dict

def eps_parser(tree):
	data_dict = {}

	for elem in tree.iter(tag='TimesSeriesList'):
		if elem.attrib['description'] == 'EPS':

			data_dict['2016'] = {}
			data_dict['2017'] = {}
			data_dict['2018'] = {}

			for fv in elem:
				if fv.attrib['period'] == 'Q1' and fv.attrib['periodEnd'].split('-')[0] == '2016':
					data_dict['2016']['Q1'] = fv[0].attrib['displayValue']
				if fv.attrib['period'] == 'Q2' and fv.attrib['periodEnd'].split('-')[0] == '2016':
					data_dict['2016']['Q2'] = fv[0].attrib['displayValue']
				if fv.attrib['period'] == 'Q3' and fv.attrib['periodEnd'].split('-')[0] == '2016':
					data_dict['2016']['Q3'] = fv[0].attrib['displayValue']
				if fv.attrib['period'] == 'Q4' and fv.attrib['periodEnd'].split('-')[0] == '2016':
					data_dict['2016']['Q4'] = fv[0].attrib['displayValue']

				if fv.attrib['period'] == 'Q1' and fv.attrib['periodEnd'].split('-')[0] == '2017':
					data_dict['2017']['Q1'] = fv[0].attrib['displayValue']
				if fv.attrib['period'] == 'Q2' and fv.attrib['periodEnd'].split('-')[0] == '2017':
					data_dict['2017']['Q2'] = fv[0].attrib['displayValue']
				if fv.attrib['period'] == 'Q3' and fv.attrib['periodEnd'].split('-')[0] == '2017':
					data_dict['2017']['Q3'] = fv[0].attrib['displayValue']
				if fv.attrib['period'] == 'Q4' and fv.attrib['periodEnd'].split('-')[0] == '2017':
					data_dict['2017']['Q4'] = fv[0].attrib['displayValue']

				if fv.attrib['period'] == 'Q1' and fv.attrib['periodEnd'].split('-')[0] == '2018':
					data_dict['2018']['Q1'] = fv[0].attrib['displayValue']
				if fv.attrib['period'] == 'Q2' and fv.attrib['periodEnd'].split('-')[0] == '2018':
					data_dict['2018']['Q2'] = fv[0].attrib['displayValue']
				if fv.attrib['period'] == 'Q3' and fv.attrib['periodEnd'].split('-')[0] == '2018':
					data_dict['2018']['Q3'] = fv[0].attrib['displayValue']
				if fv.attrib['period'] == 'Q4' and fv.attrib['periodEnd'].split('-')[0] == '2018':
					data_dict['2018']['Q4'] = fv[0].attrib['displayValue']

	return data_dict

def sidebar_stuff_parser(tree):
	data_dict = {}

	for elem in tree.iter(tag='BoilerPlate'):
		if elem.attrib['name'] == 'Our Thesis':
			data_dict['Our Thesis'] = elem.text.strip()
		if elem.attrib['name'] == 'Valuation':
			data_dict['Valuation'] = elem.text.strip()
		if elem.attrib['name'] == 'Upside Scenario':
			data_dict['Upside Scenario'] = elem.text.strip()
		if elem.attrib['name'] == 'Downside Scenario':
			data_dict['Downside Scenario'] = elem.text.strip()
		if elem.attrib['name'] == 'Company Description':
			data_dict['Company Description'] = elem.text.strip()
			
	return data_dict

def income_statement_parser(tree):
	data_dict = {}

	for elem in tree.iter(tag='FinancialModel'):
		if elem.attrib['name'].find('Income Statement') > -1:
			for values in elem:
				data_dict[values.attrib['name']] = {}
				for value in values:
					if value.attrib['year'] == '2016' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2016'] = value.attrib['displayValue']
					if value.attrib['year'] == '2017' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2017'] = value.attrib['displayValue']
					if value.attrib['year'] == '2018' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2018'] = value.attrib['displayValue']

	return data_dict

def cash_flow_statement_parser(tree):
	data_dict = {}

	for elem in tree.iter(tag='FinancialModel'):
		if elem.attrib['name'].find('Cash Flow Statement') > -1:
			for values in elem:
				data_dict[values.attrib['name']] = {}
				for value in values:
					if value.attrib['year'] == '2016' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2016'] = value.attrib['displayValue']
					if value.attrib['year'] == '2017' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2017'] = value.attrib['displayValue']
					if value.attrib['year'] == '2018' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2018'] = value.attrib['displayValue']

	return data_dict

def balance_sheet_parser(tree):
	data_dict = {}

	for elem in tree.iter(tag='FinancialModel'):
		if elem.attrib['name'].find('Balance Sheet') > -1:
			for values in elem:
				data_dict[values.attrib['name']] = {}
				for value in values:
					if value.attrib['year'] == '2016' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2016'] = value.attrib['displayValue']
					if value.attrib['year'] == '2017' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2017'] = value.attrib['displayValue']
					if value.attrib['year'] == '2018' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2018'] = value.attrib['displayValue']

	return data_dict

def key_metrics_parser(tree):
	data_dict = {}

	for elem in tree.iter(tag='FinancialModel'):
		if elem.attrib['name'].find('Key Metrics') > -1:
			for values in elem:
				data_dict[values.attrib['name']] = {}
				for value in values:
					if value.attrib['year'] == '2016' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2016'] = value.attrib['displayValue']
					if value.attrib['year'] == '2017' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2017'] = value.attrib['displayValue']
					if value.attrib['year'] == '2018' and value.tag == 'Value':
						data_dict[values.attrib['name']]['2018'] = value.attrib['displayValue']

	return data_dict

def footer_constant_stuff_parser(tree):
	data_dict = {}

	for elem in tree.iter(tag='Disclaimer'):
		if elem.attrib['code'] == 'DOR_LEGEND':
			data_dict['ratings'] = elem.text.strip()

	for elem in tree.iter(tag='Disclaimer'):
		if elem.attrib['code'] == 'RATINGS':
			data_dict['ratings_key'] = elem.text.strip()

	for elem in tree.iter(tag='Disclaimer'):
		if elem.attrib['code'] == 'OTHER_DIS':
			data_dict['other_important_disclosures'] = elem.text.strip()

	for elem in tree.iter(tag='Disclaimer'):
		if elem.attrib['code'] == 'ADDL_INFO':
			data_dict['actual_footer'] = elem.text.strip()

	return data_dict