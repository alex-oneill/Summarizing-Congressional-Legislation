import requests
from bs4 import BeautifulSoup as bs
import time
import json


# todo input congress number to the stub
congress_input = '117'
bill_stub = f'https://www.govinfo.gov/bulkdata/xml/BILLSUM/{congress_input}'

session_page = requests.get(f'{bill_stub}', headers={'Accept': 'application/xml'})

text = bs(session_page.text, 'xml')
print(f'Getting sub-directories from stub {bill_stub} ...\n')
time.sleep(10)

type_dict = {}
for file in text.findAll('file'):
    section, congress, bill_type = file.find('fullFilePath').text[1:].split('/')
    type_title = f'{congress}-{bill_type}'
    type_dict[type_title] = {'Bill_Type': bill_type,
                             'Modified': file.find('formattedLastModifiedTime').text,
                             'Link': file.find('link').text}
    print(f'Getting bill type {bill_type}...')
print()

# SUMS FROM BILLSUM PAGE
bills_dict = {}
for type_url in type_dict.values():
    bill_page = requests.get(type_url['Link'], headers={"Accept": "application/xml"})
    bill_page_txt = bs(bill_page.text, 'xml')
    time.sleep(10)

    for file in bill_page_txt.findAll('file'):
        section, congress, bill_type, title = file.find('fullFilePath').text[1:].split('/')
        bills_dict[title] = {'Link': file.find('link').text,
                             'Section': section,
                             'Congress': congress,
                             'Bill_Type': bill_type,
                             'Title': title,
                             'Modified': file.find('formattedLastModifiedTime').text,
                             'Size': file.find('formattedSize').text}
        print(f'Creating bill dictionary for {title}\t{congress}-{bill_type} ...')
    print()

# OUTPUT DICTIONARIES AS JSON
file_name = f'SummaryBillData_{congress_input}thCongress.json'

with open(file_name, 'w') as out_file:
    json.dump(bills_dict, out_file, indent=4)

print('Files scraped. Done...')
