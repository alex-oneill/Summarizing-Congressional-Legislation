import psycopg2
from configparser import ConfigParser
import re


def config(filename='../database.ini', section='postgres'):
    """Establishes connection to local postgres db with masked credentials."""
    parser = ConfigParser()
    parser.read(filename)
    db_conn = {}
    for param in parser.items(section):
        db_conn[param[0]] = param[1]
    return db_conn


def get_rows() -> list:
    """Fetches text rows to be searched for matches from the text_row table"""
    query = """SELECT id, row_number, row_text FROM text_row"""
    cur.execute(query)
    # rows = cur.fetchmany(10000)
    rows = cur.fetchall()
    return rows


def search(text_row: tuple):
    """Scans input text row for symbol, phrase, or keyword matches, then returns matches to the money_hits table"""
    text = text_row[2]

    # NOTE: ds = dollar sign match
    # NOTE: re_phrase = regexp phrase match
    # NOTE: kw = key word match
    ds = re.compile(r'\$')
    perc_of_fund = re.compile(r'percent of fund')
    not_more_perc = re.compile(r'not more than [\w.,]+ percent')
    phrase_list = [not_more_perc, perc_of_fund]
    kw = ['fund', 'funds', 'funded', 'dollar']

    if ds.search(text):
        row_out = (text_row[0], 'ds', text_row[1], text_row[2])
        insert_to_hit_tbl(row_out)

    elif any(phrase.search(text) for phrase in phrase_list):
        row_out = (text_row[0], 're_phrase', text_row[1], text_row[2])
        insert_to_hit_tbl(row_out)

    # NOTE: partial word match option instead of whole world above
    # elif any(key_w in text for key_w in kw):
    elif any(key_w in text.lower().split() for key_w in kw):
        row_out = (text_row[0], 'kw', text_row[1], text_row[2])
        insert_to_hit_tbl(row_out)

    # NOTE: there may be discrepancies between the sql and python matching
    #   this can be evidenced with the following sql query:
    """ SELECT * FROM text_row
        WHERE id NOT IN (SELECT id FROM money_hits) AND (
        row_text LIKE '%$%'
        OR row_text LIKE '%not more than%percent%'
        OR row_text LIKE '%percent of funds%'
        OR row_text LIKE '%dollar%'
        OR row_text LIKE '%fund%'
        );
    """


def insert_to_hit_tbl(row_tup: tuple):
    """Inserts matched string info into the money hits table"""
    (row_id, hit_type, row_number, row_text) = row_tup
    cur.execute("""INSERT INTO money_hits (id, hit_type, row_number, row_text)
                VALUES (%s, %s, %s, %s)""",
                (row_id, hit_type, row_number, row_text))
    conn.commit()


# SECTION: MAIN()
params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()

db_info = get_rows()

# TODO: purge old files from money_hits table if starting fresh
cur.execute("""DELETE FROM money_hits""")
conn.commit()

for row in db_info:
    search(row)

cur.close()
conn.close()
