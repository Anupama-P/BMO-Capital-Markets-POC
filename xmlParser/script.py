import os
import datetime
import random

# from django.template import Context, Template
from elasticsearch import Elasticsearch
from threading import Thread
from io import StringIO, BytesIO
# from blog.models import XMLData

from lxml import etree as ET


def xml_to_html_parser(xmlFileName, esObj, index):
    file_name = os.path.join(os.getcwd(), 'CC') + '.xml'

    tree = ET.parse(file_name)
    tree = tree.getroot()

    passage_heading = passage_parser(tree).get('heading')
    passage_bottom_line = passage_parser(tree).get('bottom_line')
    passage_key_points = passage_parser(tree).get('key_points')

    title_title = title_parser(tree).get('title')
    title_symbol = title_parser(tree).get('symbol')

    header_data_rating = header_parser(tree).get('rating')
    header_data_price = header_parser(tree).get('price')
    header_data_target = header_parser(tree).get('target')
    header_data_total_return = header_parser(tree).get('total_return')
    header_data_side_title = header_parser(tree).get('side_title')

    member1_name = member_parser(tree).get('member1').get('name')
    member1_position = member_parser(tree).get('member1').get('position')
    member1_email = member_parser(tree).get('member1').get('email')
    member1_role = member_parser(tree).get('member1').get('role')
    member1_phone = member_parser(tree).get('member1').get('phone')

    member2_name = member_parser(tree).get('member2').get('name')
    member2_position = member_parser(tree).get('member2').get('position')
    member2_email = member_parser(tree).get('member2').get('email')
    member2_role = member_parser(tree).get('member2').get('role')
    member2_phone = member_parser(tree).get('member2').get('phone')

    member3_name = member_parser(tree).get('member3').get('name')
    member3_position = member_parser(tree).get('member3').get('position')
    member3_email = member_parser(tree).get('member3').get('email')
    member3_role = member_parser(tree).get('member3').get('role')
    member3_phone = member_parser(tree).get('member3').get('phone')

    company_data_dividend = company_data_parser(tree).get('dividend')
    company_data_shares = company_data_parser(tree).get('shares')
    company_data_yield = company_data_parser(tree).get('yield')
    company_data_market_cap = company_data_parser(tree).get('market_cap')
    company_data_nav = company_data_parser(tree).get('nav')
    company_data_p_nav = company_data_parser(tree).get('p_nav')

    bmo_estimates = bmo_estimates_parser(tree)
    consensus_estimates = consensus_estimates_parser(tree)
    valuation = valuation_parser(tree)
    eps = eps_parser(tree)

    sidebar_stuff_our_thesis = sidebar_stuff_parser(tree).get('Our Thesis')
    sidebar_stuff_valuation = sidebar_stuff_parser(tree).get('Valuation')
    sidebar_stuff_upside_scenario = sidebar_stuff_parser(tree).get('Upside Scenario')
    sidebar_stuff_downside_scenario = sidebar_stuff_parser(tree).get('Downside Scenario')
    sidebar_stuff_company_description = sidebar_stuff_parser(tree).get('Company Description')

    income_statement = income_statement_parser(tree)
    cash_flow_statement = cash_flow_statement_parser(tree)
    balance_sheet = balance_sheet_parser(tree)
    key_metrics = key_metrics_parser(tree)

    footer_stuff_certification = footer_parser(tree).get('certification')
    footer_stuff_disclosures_1 = footer_parser(tree).get('disclosures')[0]
    footer_stuff_disclosures_2 = footer_parser(tree).get('disclosures')[1]
    footer_stuff_disclosures_3 = footer_parser(tree).get('disclosures')[2]
    footer_stuff_disclosures_4 = footer_parser(tree).get('disclosures')[3]
    footer_stuff_disclosures_5 = footer_parser(tree).get('disclosures')[4]
    footer_stuff_methodology = footer_parser(tree).get('methodology')
    footer_stuff_risks = footer_parser(tree).get('risks')

    footer_constant_stuff_actual_footer = footer_constant_stuff_parser(tree).get('actual_footer')
    footer_constant_stuff_ratings = footer_constant_stuff_parser(tree).get('ratings')
    footer_constant_stuff_ratings_key = footer_constant_stuff_parser(tree).get('ratings_key')
    footer_constant_stuff_other_important_disclosures = footer_constant_stuff_parser(tree).get('other_important_disclosures')

    context_dict = {
        'passage_heading': passage_heading,
        'passage_bottom_line': passage_bottom_line,
        'passage_key_points': passage_key_points,
        'title_title': title_title,
        'title_symbol': title_symbol,
        'header_data_rating': header_data_rating,
        'header_data_price': header_data_price,
        'header_data_target': header_data_target,
        'header_data_total_return': header_data_total_return,
        'header_data_side_title': header_data_side_title,
        'company_data_dividend': company_data_dividend,
        'company_data_shares': company_data_shares,
        'company_data_yield': company_data_yield,
        'company_data_market_cap': company_data_market_cap,
        'company_data_nav': company_data_nav,
        'company_data_p_nav': company_data_p_nav,
        'bmo_estimates': bmo_estimates,
        'consensus_estimates': consensus_estimates,
        'valuation': valuation,
        'eps': eps,
        "sidebar_stuff_our_thesis": sidebar_stuff_our_thesis,
        "sidebar_stuff_valuation": sidebar_stuff_valuation,
        "sidebar_stuff_upside_scenario": sidebar_stuff_upside_scenario,
        "sidebar_stuff_downside_scenario": sidebar_stuff_downside_scenario,
        "sidebar_stuff_company_description": sidebar_stuff_company_description,
        "member1_name": member1_name,
        "member1_position": member1_position,
        "member1_email": member1_email,
        "member1_role": member1_role,
        "member1_phone": member1_phone,
        "member2_name": member2_name,
        "member2_position": member2_position,
        "member2_email": member2_email,
        "member2_role": member2_role,
        "member2_phone": member2_phone,
        "member3_name": member3_name,
        "member3_position": member3_position,
        "member3_email": member3_email,
        "member3_role": member3_role,
        "member3_phone": member3_phone,
        'income_statement': income_statement,
        'cash_flow_statement': cash_flow_statement,
        'balance_sheet': balance_sheet,
        'key_metrics': key_metrics,
        'footer_stuff_certification': footer_stuff_certification,
        'footer_stuff_disclosures_1': footer_stuff_disclosures_1,
        'footer_stuff_disclosures_2': footer_stuff_disclosures_2,
        'footer_stuff_disclosures_3': footer_stuff_disclosures_3,
        'footer_stuff_disclosures_4': footer_stuff_disclosures_4,
        'footer_stuff_disclosures_5': footer_stuff_disclosures_5,
        'footer_stuff_methodology': footer_stuff_methodology,
        'footer_stuff_risks': footer_stuff_risks,
        'footer_constant_stuff_ratings': footer_constant_stuff_ratings,
        'footer_constant_stuff_ratings_key': footer_constant_stuff_ratings_key,
        'footer_constant_stuff_other_important_disclosures': footer_constant_stuff_other_important_disclosures,
        'footer_constant_stuff_actual_footer': footer_constant_stuff_actual_footer
    }

    # context = Context(context_dict)

    # # print ('Parsing {} done.'.format(file_name))
    #
    # template_text = open('xmlToHtml/templates/xmlToHtml/output.html', 'r').read()
    #
    # template = Template(template_text)
    #
    # final_template = template.render(context)
    # final_template = final_template.encode('utf-8')
    #
    # # print ('Starting generating html. {}'.format(file_name))
    #
    # f = open(xmlFileName + '.html', 'w+')
    # f.write(final_template)
    # f.close()

    countries = [
        'France',
        'Germany',
        'England'
    ]
    research_type = [
        'Reports', 'Periodical',
        'Videocast', 'Comments',
        'Flashes', 'Red Sheets',
        'Company Specific Only',
        'Member of Top 15 lists',
        'Derivatives', 'Charts',
        'NAVs'
    ]
    performance = [
        'To Underperform',
        'To Market Perform',
        'To Outperform'
    ]
    #
    context_dict['filename'] = xmlFileName
    context_dict['country'] = countries[random.randint(0, 2)]
    context_dict['research_type'] = research_type[random.randint(0, 10)]
    context_dict['performance'] = performance[random.randint(0, 2)]

    esObj.index(
        index="xml_data",
        doc_type="xml_body",
        id=xmlFileName,
        body=context_dict
    )

    # saveObjInModel(context_dict)

    # print 'Indexed the %s' % (xmlFilesName)
    # print ('Html generation done. {}'.format(file_name))

    return context_dict


# def saveObjInModel(context):
#     try:
#         obj = XMLData(
#             file_name=context['filename'],
#             research_type=context['research_type'],
#             country=context['country'],
#             passage_heading=context['passage_heading'],
#             passage_bottom_line=context['passage_bottom_line'],
#             passage_key_points=context['passage_key_points'],
#             title_title=context['title_title'],
#             title_symbol=context['title_symbol'],
#             header_data_rating=context['header_data_rating'],
#             header_data_price=context['header_data_price'],
#             header_data_target=context['header_data_target'],
#             header_data_total_return=context['header_data_total_return'],
#             header_data_side_title=context['header_data_side_title'],
#             company_data_dividend=context['company_data_dividend'],
#             company_data_shares=context['company_data_shares'],
#             company_data_yield=context['company_data_yield'],
#             company_data_market_cap=context['company_data_market_cap'],
#             company_data_nav=context['company_data_nav'],
#             company_data_p_nav=context['company_data_p_nav'],
#             bmo_estimates=context['bmo_estimates'],
#             consensus_estimates=context['consensus_estimates'],
#             valuation=context['valuation'],
#             eps=context['eps'],
#             sidebar_stuff_our_thesis=context['sidebar_stuff_our_thesis'],
#             sidebar_stuff_valuation=context['sidebar_stuff_valuation'],
#             sidebar_stuff_upside_scenario=context['sidebar_stuff_upside_scenario'],
#             sidebar_stuff_downside_scenario=context['sidebar_stuff_downside_scenario'],
#             sidebar_stuff_company_description=context['sidebar_stuff_company_description'],
#             member1_name=context['member1_name'],
#             member1_position=context['member1_position'],
#             member1_email=context['member1_email'],
#             member1_role=context['member1_role'],
#             member1_phone=context['member1_phone'],
#             member2_name=context['member2_name'],
#             member2_position=context['member2_position'],
#             member2_email=context['member2_email'],
#             member2_role=context['member2_role'],
#             member2_phone=context['member2_phone'],
#             member3_name=context['member3_name'],
#             member3_position=context['member3_position'],
#             member3_email=context['member3_email'],
#             member3_role=context['member3_role'],
#             member3_phone=context['member3_phone'],
#             income_statement=context['income_statement'],
#             cash_flow_statement=context['cash_flow_statement'],
#             balance_sheet=context['balance_sheet'],
#             key_metrics=context['key_metrics'],
#             footer_stuff_certification=context['footer_stuff_certification'],
#             footer_stuff_disclosures_1=context['footer_stuff_disclosures_1'],
#             footer_stuff_disclosures_2=context['footer_stuff_disclosures_2'],
#             footer_stuff_disclosures_3=context['footer_stuff_disclosures_3'],
#             footer_stuff_disclosures_4=context['footer_stuff_disclosures_4'],
#             footer_stuff_disclosures_5=context['footer_stuff_disclosures_5'],
#             footer_stuff_methodology=context['footer_stuff_methodology'],
#             footer_stuff_risks=context['footer_stuff_risks'],
#             footer_constant_stuff_ratings=context['footer_constant_stuff_ratings'],
#             footer_constant_stuff_ratings_key=context['footer_constant_stuff_ratings_key'],
#             footer_constant_stuff_other_important_disclosures=context['footer_constant_stuff_other_important_disclosures'],
#             footer_constant_stuff_actual_footer=context['footer_constant_stuff_actual_footer']
#         )
#         obj.save()
#     except XMLData.DoesNotExist:
#         pass


def passage_parser(tree):
    data_dict = {}

    data_dict['bottom_line'] = tree.findall('Content/Resource/Data/TextElement[@name="bottom_line"]')[0].text.strip()
    data_dict['key_points'] = tree.findall('Content/Resource/Data/TextElement[@name="key_points"]')[0].text.strip()
    data_dict['heading'] = tree.findall('Content/Title')[0].text.strip()

    return data_dict


def title_parser(tree):
    data_dict = {}

    data_dict['symbol'] = tree.findall('Context/IssuerDetails/Issuer')[0].get('symbol')
    data_dict['title'] = tree.findall('Context/IssuerDetails/Issuer')[0].get('companyName')

    return data_dict


def header_parser(tree):
    data_dict = {}

    data_dict['rating'] = tree.findall('Context/IssuerDetails/Issuer/SecurityDetails/Security/Clusters[@rank="1"]/FinancialValue[@name="RATING"]/CurrentValue')[0].get('displayValue')
    data_dict['price'] = tree.findall('Context/IssuerDetails/Issuer/SecurityDetails/Security/Clusters[@rank="1"]/FinancialValue[@name="PRICE"]/CurrentValue')[0].get('displayValue')
    data_dict['target'] = tree.findall('Context/IssuerDetails/Issuer/SecurityDetails/Security/Clusters[@rank="1"]/FinancialValue[@name="PRICE_TARGET"]/CurrentValue')[0].get('displayValue')
    data_dict['total_return'] = tree.findall('Context/IssuerDetails/Issuer/SecurityDetails/Security/Clusters[@rank="1"]/FinancialValue[@name="TOTAL_RETURN"]/CurrentValue')[0].get('displayValue')
    data_dict['side_title'] = tree.findall('Content/Resource/Data/TextElement[@name="sector_name_override"]')[0].text.strip()

    return data_dict


def member_parser(tree):
    data_dict = {}
    data_dict['member1'] = {
        'name': tree.findall('Source/Publisher/Team/TeamMember[@sequence="1"]')[0][2].text + ' ' + tree.findall('Source/Publisher/Team/TeamMember[@sequence="1"]')[0][1].text,
        'role': tree.findall('Source/Publisher/Team/TeamMember[@sequence="1"]')[0][0].text,
        'position': tree.findall('Source/Publisher/Team/TeamMember[@sequence="1"]')[0][4].text,
        'email': tree.findall('Source/Publisher/Team/TeamMember[@sequence="1"]')[0][10].text,
        'phone': tree.findall('Source/Publisher/Team/TeamMember[@sequence="1"]')[0][9].text,
    }
    data_dict['member2'] = {
        'name': tree.findall('Source/Publisher/Team/TeamMember[@sequence="2"]')[0][2].text + ' ' + tree.findall('Source/Publisher/Team/TeamMember[@sequence="2"]')[0][1].text,
        'role': tree.findall('Source/Publisher/Team/TeamMember[@sequence="2"]')[0][0].text,
        'position': tree.findall('Source/Publisher/Team/TeamMember[@sequence="2"]')[0][4].text,
        'email': tree.findall('Source/Publisher/Team/TeamMember[@sequence="2"]')[0][10].text,
        'phone': tree.findall('Source/Publisher/Team/TeamMember[@sequence="2"]')[0][9].text,
    }
    data_dict['member3'] = {
        'name': tree.findall('Source/Publisher/Team/TeamMember[@sequence="3"]')[0][2].text + ' ' + tree.findall('Source/Publisher/Team/TeamMember[@sequence="3"]')[0][1].text,
        'role': tree.findall('Source/Publisher/Team/TeamMember[@sequence="3"]')[0][0].text,
        'position': tree.findall('Source/Publisher/Team/TeamMember[@sequence="3"]')[0][4].text,
        'email': tree.findall('Source/Publisher/Team/TeamMember[@sequence="3"]')[0][10].text,
        'phone': tree.findall('Source/Publisher/Team/TeamMember[@sequence="3"]')[0][9].text,
    }

    return data_dict


def company_data_parser(tree):
    data_dict = {}

    data_dict['dividend'] = tree.findall('Context/IssuerDetails/Issuer/SecurityDetails/Security/Clusters[@rank="9"]/FinancialValue[@name="DIVIDEND"]/CurrentValue')[0].get('displayValue')
    data_dict['yield'] = tree.findall('Context/IssuerDetails/Issuer/SecurityDetails/Security/Clusters[@rank="9"]/FinancialValue[@name="YIELD_CALC"]/CurrentValue')[0].get('displayValue')
    data_dict['nav'] = tree.findall('Context/IssuerDetails/Issuer/SecurityDetails/Security/Clusters[@rank="9"]/FinancialValue[@name="NAV"]/CurrentValue')[0].get('displayValue')
    data_dict['shares'] = tree.findall('Context/IssuerDetails/Issuer/SecurityDetails/Security/Clusters[@rank="9"]/FinancialValue[@name="SHARES_OUT"]/CurrentValue')[0].get('displayValue')
    data_dict['market_cap'] = tree.findall('Context/IssuerDetails/Issuer/SecurityDetails/Security/Clusters[@rank="9"]/FinancialValue[@name="MKT_CAP_CALC"]/CurrentValue')[0].get('displayValue')
    data_dict['p_nav'] = tree.findall('Context/IssuerDetails/Issuer/SecurityDetails/Security/Clusters[@rank="9"]/FinancialValue[@name="P_NAV"]/CurrentValue')[0].get('displayValue')

    return data_dict


def footer_parser(tree):
    data_dict = {}
    data_dict['disclosures'] = []

    data_dict['certification'] = tree.findall('Legal/Disclaimer[@code="REG_AC"]')[0].text.strip()
    data_dict['methodology'] = tree.findall('Content/Resource/Data/BoilerPlate[@name="Methodology"]')[0].text.strip()
    data_dict['risks'] = tree.findall('Content/Resource/Data/BoilerPlate[@name="Risks"]')[0].text.strip()

    for elem in tree.findall('Legal/Disclosure'):
        data_dict['disclosures'].append(elem.text.strip())

    return data_dict


def bmo_estimates_parser(tree):
    data_dict = {}

    for values in tree.findall('Context/IssuerDetails/Issuer/SecurityDetails/Security/FinancialModels/FinancialModel[@rank="1"]/Values'):
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

    data_dict['EPS'] = {}
    for value in tree.findall('Context/IssuerDetails/Issuer/SecurityDetails/Security/FinancialModels/FinancialModel[@rank="2"]/Values/Value'):
        if value.attrib['year'] == '2016' and value.tag == 'Value':
            data_dict['EPS']['2016'] = value.attrib['displayValue']
        if value.attrib['year'] == '2017' and value.tag == 'Value':
            data_dict['EPS']['2017'] = value.attrib['displayValue']
        if value.attrib['year'] == '2018' and value.tag == 'Value':
            data_dict['EPS']['2018'] = value.attrib['displayValue']

    return data_dict


def valuation_parser(tree):
    data_dict = {}

    for values in tree.findall('Context/IssuerDetails/Issuer/SecurityDetails/Security/FinancialModels/FinancialModel[@rank="3"]/Values'):
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
    data_dict['2016'] = {}
    data_dict['2017'] = {}
    data_dict['2018'] = {}

    for fv in tree.findall('Extended/Security/TimesSeriesList[@description="EPS"]/FinancialValue'):
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

    data_dict['Our Thesis'] = tree.findall('Content/Resource/Data/BoilerPlate[@name="Our Thesis"]')[0].text.strip()
    data_dict['Valuation'] = tree.findall('Content/Resource/Data/BoilerPlate[@name="Valuation"]')[0].text.strip()
    data_dict['Upside Scenario'] = tree.findall('Content/Resource/Data/BoilerPlate[@name="Upside Scenario"]')[0].text.strip()
    data_dict['Downside Scenario'] = tree.findall('Content/Resource/Data/BoilerPlate[@name="Downside Scenario"]')[0].text.strip()
    data_dict['Company Description'] = tree.findall('Content/Resource/Data/BoilerPlate[@name="Company Description"]')[0].text.strip()

    return data_dict


def income_statement_parser(tree):
    data_dict = {}

    for values in tree.findall('Context/IssuerDetails/Issuer/SecurityDetails/Security/FinancialModels/FinancialModel[@rank="4"]/Values'):
        key = values.attrib['name'].replace(" ", "_")
        data_dict[key] = {}
        for value in values:
            if value.attrib['year'] == '2016' and value.tag == 'Value':
                data_dict[key]['2016'] = value.attrib['displayValue']
            if value.attrib['year'] == '2017' and value.tag == 'Value':
                data_dict[key]['2017'] = value.attrib['displayValue']
            if value.attrib['year'] == '2018' and value.tag == 'Value':
                data_dict[key]['2018'] = value.attrib['displayValue']

    return data_dict


def cash_flow_statement_parser(tree):
    data_dict = {}

    for values in tree.findall('Context/IssuerDetails/Issuer/SecurityDetails/Security/FinancialModels/FinancialModel[@rank="5"]/Values'):
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

    for values in tree.findall('Context/IssuerDetails/Issuer/SecurityDetails/Security/FinancialModels/FinancialModel[@rank="6"]/Values'):
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

    for values in tree.findall('Context/IssuerDetails/Issuer/SecurityDetails/Security/FinancialModels/FinancialModel[@rank="7"]/Values'):
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

    data_dict['ratings'] = tree.findall('Legal/Disclaimer[@code="DOR_LEGEND"]')[0].text.strip()
    data_dict['ratings_key'] = tree.findall('Legal/Disclaimer[@code="RATINGS"]')[0].text.strip()
    data_dict['other_important_disclosures'] = tree.findall('Legal/Disclaimer[@code="OTHER_DIS"]')[0].text.strip()
    data_dict['actual_footer'] = tree.findall('Legal/Disclaimer[@code="ADDL_INFO"]')[0].text.strip()

    return data_dict


# instantiate elastic search
context_dict = {
    "passage": "passage",
    "title": "title",
    "header_data": "header_data",
    "company_data": "company_data",
    "bmo_estimates": "bmo_estimates",
    "consensus_estimates": "consensus_estimates",
    "valuation": "valuation",
    "eps": "eps",
    "sidebar_stuff": "sidebar_stuff",
    "team_members": "team_members",
    "income_statement": "income_statement",
    "cash_flow_statement": "cash_flow_statement",
    "balance_sheet": "balance_sheet",
    "key_metrics": "key_metrics",
    "footer_stuff": "footer_stuff",
    "footer_constant_stuff": "footer_constant_stuff",
}

es_settings = {
    "settings": {
        "analysis": {
            "filter": {
                "edge_nGram_filter": {
                    "type": "edge_ngram",
                    "min_gram": 2,
                    "max_gram": 20,
                    "token_chars": [
                        "letter",
                        "digit"
                    ]
                }
            },
            "analyzer": {
                "edge_nGram_analyzer": {
                    "type": "custom",
                    "tokenizer": "whitespace",
                    "filter": [
                        "lowercase",
                        "asciifolding",
                        "edge_nGram_filter"
                    ]
                },
                "whitespace_analyzer": {
                    "type": "custom",
                    "tokenizer": "whitespace",
                    "filter": [
                        "lowercase",
                        "asciifolding"
                    ]
                }
            }
        }
    },
    "mappings": {
        "xml_body": {
            "properties": {
                "title_symbol": {
                    "type": "string",
                    "analyzer": "edge_nGram_analyzer",
                    "search_analyzer": "whitespace_analyzer"
                },
                "member1_name": {
                    "type": "string",
                    "analyzer": "edge_nGram_analyzer",
                    "search_analyzer": "whitespace_analyzer"
                },
                "member2_name": {
                    "type": "string",
                    "analyzer": "edge_nGram_analyzer",
                    "search_analyzer": "whitespace_analyzer"
                },
                "member3_name": {
                    "type": "string",
                    "analyzer": "edge_nGram_analyzer",
                    "search_analyzer": "whitespace_analyzer"
                },
                "performance": {
                    "type": "string",
                    "analyzer": "keyword"
                },
                "research_type": {
                    "type": "string",
                    "analyzer": "keyword"
                },
                "country": {
                    "type": "string",
                    "analyzer": "keyword"
                },
            }
        }
    }
}


def new_thread(name, start, es, s_time):
    print name + " started"
    for i in range(start, start + 25001):
        filename = 'newCC' + str(i)
        xml_to_html_parser(filename, es, i)
    print name + " ended"
    e_time = datetime.datetime.now() - s_time
    print str(e_time.seconds) + ' seconds'


def Main():
    start = datetime.datetime.now()
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    try:
        es.indices.delete(index='xml_data')
        es.indices.create(index='xml_data', body=es_settings)
        # XMLData.objects.all().delete()
    except Exception:
        es.indices.create(index='xml_data', body=es_settings)

    # With Threading

    num_of_threads = 4
    threads = list()
    for i in range(num_of_threads):
        t = Thread(target=new_thread, args=("Thread-" + str(i), i * 25000, es, start))
        print 'created thread ' + str(i)
        threads.append(t)

    for t in threads:
        t.start()

    # Without threading

    # for i in range(10000):
    #     filename = 'newCC' + str(i)
    #     xml_to_html_parser(os.path.join(os.getcwd(), 'HTML', filename), es, i)

    end = datetime.datetime.now() - start
    print str(end.seconds) + ' seconds'


Main()
