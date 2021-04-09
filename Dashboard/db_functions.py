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


def get_bill_titles() -> list:
    """Establishes Connection to DB"""
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT (concat(short_name, ' - ', header)) as bill FROM bills_full_text
                        GROUP BY bill ORDER BY bill""")
            rows = cur.fetchall()
            return rows


def get_money_hits() -> list:
    """Retrieves all text rows from the DB with sample bill ID 116hr2500"""
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT hit_type, row_number, row_text FROM money_hits
                        WHERE id LIKE '%116hr2500%' ORDER BY row_number""")
            rows = cur.fetchall()
            return rows


def get_drill_rows(row_num) -> list:
    """Retrieves 5 rows prior and 3 rows after a selected money-hit row from sample bill 116hr2500"""
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            prior = row_num - 5
            after = row_num + 3
            query = f"""SELECT s.row_number, s.row_text FROM 
                            (SELECT * FROM text_row
                                WHERE name = (SELECT name FROM text_row
                                    WHERE short_name = '116hr2500'
                                    AND name NOT IN ('116hr2500ih', '116hr2500rh')
                                    GROUP BY name ORDER BY RANDOM() LIMIT 1)
                                ORDER BY row_number) s
                        WHERE row_number BETWEEN {prior} AND {after}"""
            cur.execute(query)
            dirty_rows = cur.fetchall()
            clean_rows = []
            for i, text in dirty_rows:
                clean_str = clean_db_text(text)
                clean_rows.append((i, clean_str))
            return clean_rows


def clean_db_text(text: str) -> str:
    """Removes lingering encoding text from uncleaned raw text rows"""
    en_str = text.encode('ascii', 'ignore')
    de_str = en_str.decode()
    return de_str


params = config()

