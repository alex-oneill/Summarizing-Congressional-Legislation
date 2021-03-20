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
    query = """SELECT DISTINCT ON(short_name, row_number) id, concat(short_name, '-', row_number) AS blend_id, 
            short_name, name, full_title, short_title, summary_1, summary_2, summary_3, row_number, row_text
            FROM text_row
            ORDER BY short_name, row_number"""
    cur.execute(query)
    # rows = cur.fetchmany(100)
    rows = cur.fetchall()
    return rows


def standardize(row_tup: tuple) -> tuple:
    word_list = [word.lower() for word in row_tup[10].split()]
    stnd_word_list = []
    for word in word_list:
        en_str = word.encode('ascii', 'ignore')
        de_str = en_str.decode()
        if '-' in word:
            sym_word = word
        else:
            sym_word = re.sub(r'[^a-z]+', '', de_str)
        stnd_word_list.append(sym_word)
    stnd_word_str = ' '.join(stnd_word_list)
    stnd_word_list = stnd_word_str.split()
    return row_tup + (stnd_word_list,)

# TODO: remove stop-words
# TODO: stemming and lemmatization


params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()

# SECTION: MAIN()
text_rows = get_rows()
# NOTE: text_rows tuple format...
# 00 = {str} id
# 01 = {str} blend_id
# 02 = {str} short_name
# 03 = {str} name
# 04 = {str} full_title
# 05 = {str} short_title
# 06 = {str} summary_1
# 07 = {str} summary_2
# 08 = {str} summary_3
# 09 = {int} row_number
# 10 = {str} row_text

stnd_rows = []
for row in text_rows:
    # NOTE: adds tup[11] = {list} stnd_row_text
    stnd_rows.append(standardize(row))

# NOTE: reclaim memory
# del text_rows

cur.close()
conn.close()

