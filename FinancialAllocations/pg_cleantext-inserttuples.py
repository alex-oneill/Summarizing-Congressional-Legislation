import psycopg2
from configparser import ConfigParser


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
    rows = cur.fetchmany(15)
    return rows


def make_txt_tuples(row):
    for line in row[8][2:-2].split('), ('):
        line_num, text = line.split(', ', 1)
        row_tup = (line_num, text)
        print(row_tup)


params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()

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

rowdata = get_text()
for row in rowdata:
    make_txt_tuples(row)


cur.close()
conn.close()
