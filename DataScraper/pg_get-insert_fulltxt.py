import psycopg2
from configparser import ConfigParser
import requests
from bs4 import BeautifulSoup as bs
import time


def config(filename='../database.ini', section='postgres'):
    """Establishes connection to local postgres db with masked credentials."""
    parser = ConfigParser()
    parser.read(filename)
    db_conn = {}
    for param in parser.items(section):
        db_conn[param[0]] = param[1]
    return db_conn


def get_billsum_rows():
    """Fetches all full-text data rows from the bill_info table that have corresponding summaries previously scraped
     into the sum_full_text table. These are returned as a list."""
    query = """SELECT B.*
            FROM BILL_INFO B
            INNER JOIN SUM_FULL_TEXT S ON S.NAME = B.SHORT_NAME
            WHERE B.SECTION = 'BILLS'
            ORDER BY B.SHORT_NAME"""
    cur.execute(query)
    rows = cur.fetchall()
    return rows


def fetch_xml(link):
    """Fetches xml text from the bulk data website. Returns BeautifulSoup text."""
    webpage = requests.get(link, headers={'Accept': 'application/xml'})
    raw_txt = bs(webpage.text, 'xml')
    return raw_txt


def parse_insert_row(data, db_info):
    """Parses BeautifulSoup text and inserts relevant rows into the sum_full_text table."""

    full_title = db_info[0]
    short_name = db_info[1]
    name = db_info[2]
    section = db_info[3]
    link = db_info[4]
    congress = db_info[5]
    session = db_info[6]
    bill_title = data.find('dc:title').text
    title = data.find('dc:title').text
    publisher = data.find('dc:publisher').text
    if data.find('dc:date').text == '':
        date = None
    else:
        date = data.find('dc:date').text
    header = ' '.join(data.find('official-title').text.split())
    word_list = data.find_all('text')
    words = str([(k, v) for k, v in enumerate(word_list)])

    cur.execute("""INSERT INTO bills_full_text (full_title, short_name, name, section, link, congress, session,
                bill_title, title_sum, publisher, date, header, words)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (full_title, short_name, name, section, link, congress, session, bill_title, title,
                 publisher, date, header, words))
    conn.commit()


params = config()
conn = psycopg2.connect(**params)

cur = conn.cursor()

result_list = get_billsum_rows()

# RESULT LIST TUPLE STRUCTURE
# 0 = {str} 'BILLS-116hconres19eh'
# 1 = {str} '116hconres19'
# 2 = {str} '116hconres19eh'
# 3 = {str} 'BILLS'
# 4 = {str} 'https://www.govinfo.gov/bulkdata/BILLS/116/1/hconres/BILLS-116hconres19eh.xml'
# 5 = {str} '116'
# 6 = {str} '1'
# 7 = {datetime} 2019-04-10 06: 27:00
for db_row in result_list:
    try:
        raw_text = fetch_xml(db_row[4])
        parse_insert_row(raw_text, db_row)
        print('Inserted ', db_row[4], '. Sleeping peacefully until next fetch...')
        time.sleep(10)
    except Exception as e:
        print('Caught exception! Moving along\n', e)

cur.close()
conn.close()
print('Fetching and inserting is done. All connections closed')
