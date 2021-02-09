import requests
from bs4 import BeautifulSoup as bs

bill_stub = 'https://www.govinfo.gov/bulkdata/xml/BILLS/116'
billsum_stub = 'https://www.govinfo.gov/bulkdata/xml/BILLSUM/116'
# session = input('Enter congressional session: ')

# LIVE REQUESTS
# page = requests.get(f'{bill_stub}', headers={"Accept": "application/xml"})
# text = bs(page.text, 'lxml')

# DUMMY REQUEST
text = bs(open('sessionpage.xml'), 'xml')
# print(text.prettify())

# SESSION DATA
session_dict = {}
for file in text.findAll('file'):
    session = file.find('displayLabel').text
    modified_date = file.find('formattedLastModifiedTime').text
    link = file.find('link').text
    session_dict[session] = {'Session': session,
                             'Modified': modified_date,
                             'Link': link}
print(session_dict)

# todo scan for session urls
# todo parse sub-urls


