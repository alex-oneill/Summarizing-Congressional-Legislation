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
    # rows = cur.fetchall()
    rows = cur.fetchmany(2)
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
    summary_2 = db_info[6]
    summary_3 = db_info[7]
    # bill_title = data.find('dc:title').text
    # title = data.find('dc:title').text
    # publisher = data.find('dc:publisher').text
    # if data.find('dc:date').text == '':
    #     date = None
    # else:
    #     date = data.find('dc:date').text
    # header = ' '.join(data.find('official-title').text.split())
    word_list = data.find_all('text')
    # words = str([(k, v) for k, v in enumerate(word_list)])

    for k, text_line in enumerate(word_list):
        # mod = re.sub(r'<.+?>', '', text_line)
        print(k, text_line.text)

# def make_txt_tuples(str_text):
#     """Ingests full words string, removes xml tags, and splits into tuples of (row #, section). Returns a list of
#     these tuples"""
#     word_list = []
#     for words in str_text[8][2:-2].split('), ('):
#         if '<text' in words:
#             mod = re.sub(r'<.+?>', '', words)
#             line_num, text = mod.split(', ', 1)
#             row_tup = (line_num, text)
#             word_list.append(row_tup)
#     for word in word_list:
#         print(word)
#     return word_list


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

    # make_txt_tuples(row)


cur.close()
conn.close()
print('Fetching and inserting is done. All connections closed')

# r"\([^<>]*\)",