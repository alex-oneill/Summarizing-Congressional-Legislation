import requests
from bs4 import BeautifulSoup as bs
import time

bill_stub = 'https://www.govinfo.gov/bulkdata/xml/BILLS/116'
billsum_stub = 'https://www.govinfo.gov/bulkdata/xml/BILLSUM/116'
# session = input('Enter congressional session: ')

# todo LIVE REQUESTS
session_page = requests.get(f'{bill_stub}', headers={'Accept': 'application/xml'})
text = bs(session_page.text, 'xml')
print(f'Getting sub-directories from stub {bill_stub} ...\n')
time.sleep(10)

# DUMMY REQUEST
# text = bs(open('1_sessionpage.xml'), 'xml')

# Level 1 - SESSION DATA
session_dict = {}
for file in text.findAll('file'):
    section_type, congress, session = file.find('fullFilePath').text[1:].split('/')
    print(f'Getting session {session} for Congress {congress} ...\n')
    # session = file.find('displayLabel').text
    session_dict[session] = {'Session': session,
                             'Modified': file.find('formattedLastModifiedTime').text,
                             'Link': file.find('link').text}

# Level 2 - TYPES OF BILLS PER SESSION
type_dict = {}
for session_data in session_dict.values():
    # todo LIVE REQUEST
    type_page = requests.get(session_data['Link'], headers={"Accept": "application/xml"})
    type_text = bs(type_page.text, 'xml')
    time.sleep(10)

    # DUMMY REQUEST
    # type_text = bs(open('2_typespage.xml'), 'xml')

    for file in type_text.findAll('file'):
        section, congress, session, bill_type = file.find('fullFilePath').text[1:].split('/')
        type_title = f'{congress}-{session}-{bill_type}'
        type_dict[type_title] = {'Bill_Type': bill_type,
                                 'Session': session,
                                 'Modified': file.find('formattedLastModifiedTime').text,
                                 'Link': file.find('link').text}
        print(f'Getting bill type {bill_type} for session {session} ...')
    print()

# Level 3 - BILLS FROM BILL PAGE
bills_dict = {}
for type_url in type_dict.values():
    # todo LIVE REQUEST
    bill_page = requests.get(type_url['Link'], headers={"Accept": "application/xml"})
    bill_page_txt = bs(bill_page.text, 'xml')
    time.sleep(10)

    # DUMMY REQUEST
    # bill_page_txt = bs(open('3_bills.xml'), 'xml')

    for file in bill_page_txt.findAll('file'):
        section, congress, session, bill_type, title = file.find('fullFilePath').text[1:].split('/')
        bills_dict[title] = {'File_Path': file.find('fullFilePath').text,
                             'Section': section,
                             'Congress': congress,
                             'Session': session,
                             'Bill_Type': bill_type,
                             'Title': title,
                             'Modified': file.find('formattedLastModifiedTime').text,
                             'Size': file.find('formattedSize').text}
        print(f'Creating bill dictionary for {title}\t{congress}-{session}-{bill_type} ...')
    print()

# todo PULL ALL XML FILES FROM BILLS_DICT