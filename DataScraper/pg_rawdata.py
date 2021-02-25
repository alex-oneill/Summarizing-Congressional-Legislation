import psycopg2
from configparser import ConfigParser


def config(filename='../database.ini', section='postgres'):
    parser = ConfigParser()
    parser.read(filename)
    db_conn = {}
    for param in parser.items(section):
        db_conn[param[0]] = param[1]
    return db_conn


params = config()
conn = psycopg2.connect(**params)

cur = conn.cursor()

query = "SELECT * FROM test_table WHERE firstname LIKE '%a%'"
cur.execute(query)
print(cur.fetchall())

conn.close()
