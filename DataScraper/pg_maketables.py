import psycopg2
from configparser import ConfigParser


def config(filename='../database.ini', section='postgres'):
    parser = ConfigParser()
    parser.read(filename)
    db_conn = {}
    for param in parser.items(section):
        db_conn[param[0]] = param[1]
    return db_conn


def execute_sql(sql_file):
    file_in = open(sql_file, 'r')
    sql = file_in.read()
    file_in.close()
    return sql


params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()

# MAKE FULL TEXT SUMMARY TABLE
# cur.execute(execute_sql('makeSummaryFullTxtTable.sql'))

# MAKE BILL INFO TABLE
# cur.execute(execute_sql('makeInfoTable.sql'))

cur.close()
conn.commit()
conn.close()
