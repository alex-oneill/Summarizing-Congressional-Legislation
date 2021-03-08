import psycopg2
from configparser import ConfigParser
import re
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


def get_text():
    """Fetches text and data rows for cleaning and inserting back as single tuples"""
    query = """SELECT
            A.short_name ,A.name ,A.link ,A.bill_title AS "full_title" ,A.title_sum AS "short_title"
            ,B.title_sum AS "summary_1" ,B.sum_text AS "summary_2" ,A.header AS "summary_3"
            ,A.words AS "full_text"
            FROM bills_full_text A
            INNER JOIN sum_full_text B ON B.name = A.short_name
            ORDER BY A.short_name"""
    cur.execute(query)
    rows = cur.fetchall()
    return rows


def grab_xml(link):
    """Fetches xml text from the bulk data website. Returns BeautifulSoup text."""
    webpage = requests.get(link, headers={'Accept': 'application/xml'})
    raw_txt = bs(webpage.text, 'xml')
    return raw_txt


def parse_insert_row(data, db_info):
    """Parses BeautifulSoup text and inserts relevant rows into the sum_full_text table."""

    short_name = db_info[0]
    name = db_info[1]
    link = db_info[2]
    full_title = db_info[3]
    short_title = db_info[4]
    summary_1 = db_info[5]
    summary_2 = re.sub(r'<.+?>', '', db_info[6])
    summary_3 = db_info[7]
    word_list = data.find_all('text')

    for k, text_line in enumerate(word_list):
        # mod = re.sub(r'<.+?>', '', text_line)
        cur.execute("""INSERT INTO text_row (id, short_name, name, link, full_title, short_title, summary_1,
                    summary_2, summary_3, row_number, row_text)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (name+'-'+str(k), short_name, name, link, full_title, short_title, summary_1, summary_2,
                     summary_3, k, text_line.text))
        conn.commit()


params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()

rowdata = get_text()
# TEXT AND STUFF HERE
# 0 = {str} 'short_name'
# 1 = {str} 'name'
# 2 = {str} 'link'
# 3 = {str} 'full_title'
# 4 = {str} 'short_title'
# 5 = {str} 'summary_1'
# 6 = {str} 'summary_2'
# 7 = {str} 'summary_3'
# 8 = {str} 'full_text -- tuple list'
for row in rowdata:
    try:
        raw_text = grab_xml(row[2])
        parse_insert_row(raw_text, row)
        print('Inserted ', row[2], '. Sleeping peacefully until next fetch...')
        time.sleep(10)
    except Exception as e:
        print('Caught exception! Moving along\n', e)

cur.close()
conn.close()
print('Fetching and inserting is done. All connections closed')