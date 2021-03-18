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


def get_rows():
    """Fetches text rows to be searched for matches from the text_row table"""
    query = """SELECT id, row_number, row_text FROM text_row"""
    cur.execute(query)
    rows = cur.fetchmany(200)
    return rows


def search(row):
    text = row[2]
    ds = re.compile('\$')

    if ds.search(text):
        row_out = (row[0], "ds", row[1], row[2])
        insert_to_hit_tbl(row_out)
    # todo elif kw match
        # todo insert_to_hit_tbl
    # todo nothing
    # print(text)


def insert_to_hit_tbl(row_tup):
    """Inserts matched string info into the money hits table"""
    (row_id, hit_type, row_number, row_text) = row_tup
    cur.execute("""INSERT INTO money_hits (id, hit_type, row_number, row_text)
                VALUES (%s, %s, %s, %s)""",
                (row_id, hit_type, row_number, row_text))
    conn.commit()


params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()

db_info = get_rows()

# todo PURGE OLD
cur.execute("""DELETE FROM money_hits""")
conn.commit()

for row in db_info:
    search(row)

cur.close()
conn.close()
