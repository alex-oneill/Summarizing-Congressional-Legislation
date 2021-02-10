import requests
from bs4 import BeautifulSoup as bs

bill_stub = 'https://www.govinfo.gov/bulkdata/xml/BILLS/116'
billsum_stub = 'https://www.govinfo.gov/bulkdata/xml/BILLSUM/116'
# session = input('Enter congressional session: ')

# todo LIVE REQUESTS
# session_page = requests.get(f'{bill_stub}', headers={"Accept": "application/xml"})
# text = bs(session_page.text, 'xml')

# todo DUMMY REQUEST
text = bs(open('1_sessionpage.xml'), 'xml')

# SESSION DATA
session_dict = {}
for file in text.findAll('file'):
    session = file.find('displayLabel').text
    session_dict[session] = {'Session': session,
                             'Modified': file.find('formattedLastModifiedTime').text,
                             'Link': file.find('link').text}
# print(session_dict)

# TYPES OF BILLS PER SESSION
type_dict = {}
for session_data in session_dict.values():
    # todo LIVE REQUEST
    # type_page = requests.get(session_data['Link'], headers={"Accept": "application/xml"})
    # type_text = bs(type_page.text, 'xml')

    # todo DUMMY REQUEST
    type_text = bs(open('2_typespage.xml'), 'xml')

    for file in type_text.findAll('file'):
        section, congress, session, bill_type = file.find('fullFilePath').text[1:].split('/')
        type_title = f'{congress}-{session}-{bill_type}'
        type_dict[type_title] = {'Bill_Type': bill_type,
                                 'Session': session,
                                 'Modified': file.find('formattedLastModifiedTime').text,
                                 'Link': file.find('link').text}
    # print(type_dict)

# todo next loop will need to grab all bill_type links to collect links for actual documents
