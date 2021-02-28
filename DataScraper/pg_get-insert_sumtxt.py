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
    """Fetches 1000 random bill summary rows from the bill_info table. These are returned as a list."""
    query = """SELECT * FROM bill_info
            WHERE section = 'BILLSUM'
            ORDER BY RANDOM()
            LIMIT 1000"""
    cur.execute(query)
    rows = cur.fetchmany(1000)
    return rows


def fetch_xml(link):
    """Fetches xml text from the bulk data website. Returns BeautifulSoup text."""
    webpage = requests.get(link, headers={'Accept': 'application/xml'})
    raw_txt = bs(webpage.text, 'xml')
    return raw_txt


def parse_insert_row(data, url):
    """Parses BeautifulSoup text and inserts relevant roles into the sum_full_text table."""

    full_title = url.split('/')[-1][:-4]
    name = full_title.split('-')[-1]
    section = full_title.split('-')[0]
    congress = data.find('item').get('congress')
    title_sum = data.find('title').text
    sum_text = data.find('summary-text').text
    measure_type = data.find('item').get('measure-type')
    measure_number = data.find('item').get('measure-number')
    origin_chamber = data.find('item').get('originChamber')
    orig_publish = data.find('item').get('orig-publish-date')

    cur.execute("""INSERT INTO sum_full_text (full_title, name, section, congress, title_sum, sum_text,
                measure_type, measure_number, origin_chamber, orig_publish)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (full_title, name, section, congress, title_sum, sum_text, measure_type, measure_number,
                 origin_chamber, orig_publish))
    conn.commit()


params = config()
conn = psycopg2.connect(**params)

cur = conn.cursor()

result_list = get_billsum_rows()

# RESULT LIST TUPLE STRUCTURE
# [0] = full_title, [1] = name, [2] = section, [3] = link, [4] = congress, [5] = session, [6] = modified_data
for db_row in result_list:
    try:
        raw_text = fetch_xml(db_row[3])
        parse_insert_row(raw_text, db_row[3])
        print('Inserted ', db_row[3], '. Sleeping peacefully until next fetch...')
        time.sleep(10)
    except Exception as e:
        print('Caught exception! Moving along\n', e)

cur.close()
conn.close()
print('Fetching and inserting is done. All connections closed')
