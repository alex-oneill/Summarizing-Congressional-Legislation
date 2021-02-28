import psycopg2
from configparser import ConfigParser
import json


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


def read_bill_info(file):
    file_in = open(file, 'r')
    info_dict = json.load(file_in)
    file_in.close()
    return info_dict


params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()


# INSERT SUMMARY INTO TABLE
# todo adjust the input file
# data = read_bill_info('SummaryBillData_117thCongress.json')
# for k, v in data.items():
#
#     cur.execute("""INSERT INTO bill_info (full_title, name, section, link, congress, modified)
#                 VALUES (%s, %s, %s, %s, %s, %s)""",
#                 (v['Title'][:-4],
#                  v['Title'].split('-')[1][:-4],
#                  v['Section'],
#                  v['Link'],
#                  v['Congress'],
#                  v['Modified']))

    # full_title = v['Title'][:-4]
    # name = v['Title'].split('-')[1][:-4]
    # section = v['Section']
    # link = v['Link']
    # congress = v['Congress']
    # modified = v['Modified']

# INSERT FULL TEXT INFO INTO TABLE
# todo adjust sql for full text input
data = read_bill_info('FullBillData_116thCongress.json')
for k, v in data.items():

    cur.execute("""INSERT INTO bill_info (full_title, name, section, link, congress, modified)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (v['Title'][:-4],
                 v['Title'].split('-')[1][:-4],
                 v['Section'],
                 v['Link'],
                 v['Congress'],
                 v['Modified']))

    # full_title = v['Title'][:-4]
    # name = v['Title'].split('-')[1][:-4]
    # section = v['Section']
    # link = v['Link']
    # congress = v['Congress']
    # modified = v['Modified']

cur.close()
conn.commit()
conn.close()
