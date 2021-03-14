import psycopg2
from configparser import ConfigParser


def config(filename='database.ini', section='postgres'):
    """Establishes connection to local postgres db with masked credentials."""
    parser = ConfigParser()
    parser.read(filename)
    db_conn = {}
    for param in parser.items(section):
        db_conn[param[0]] = param[1]
    return db_conn


def execute_sql(sql_file):
    """Executes a the sql query in an external file."""
    file_in = open(sql_file, 'r')
    sql = file_in.read()
    file_in.close()
    return sql


params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()

# MAKE TEXT ROW TABLE
# cur.execute(execute_sql(r'DataScraper\makeTextRowTable.sql'))

# MAKE FULL TEXT BILL TABLE
# cur.execute(execute_sql(r'DataScraper\makeBillsFullTxtTable.sql'))

# MAKE FULL TEXT SUMMARY TABLE
# cur.execute(execute_sql(r'DataScraper\makeSummaryFullTxtTable.sql'))

# MAKE BILL INFO TABLE
# cur.execute(execute_sql(r'DataScraper\makeInfoTable.sql'))

# MAKE FINANCIAL ALLOCATION HIT TABLE
# cur.execute(execute_sql(r'FinancialAllocations\makeMoneyHitTable.sql'))

cur.close()
conn.commit()
conn.close()
