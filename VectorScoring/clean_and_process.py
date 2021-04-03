import psycopg2
from configparser import ConfigParser
import re
import logging
from gensim import corpora
from Document import Document


def config(filename='../database.ini', section='postgres'):
    """Establishes connection to local postgres db with masked credentials."""
    parser = ConfigParser()
    parser.read(filename)
    db_conn = {}
    for param in parser.items(section):
        db_conn[param[0]] = param[1]
    return db_conn


# SECTION: CLEAN AND MAKE CORPUS
def get_rows() -> list:
    """Fetches text rows to be searched for matches from the text_row table"""
    query = """SELECT DISTINCT ON(short_name, row_number) id, concat(short_name, '-', row_number) AS blend_id, 
            short_name, name, full_title, short_title, summary_1, summary_2, summary_3, row_number, row_text
            FROM text_row
            ORDER BY short_name, row_number"""
    cur.execute(query)
    # TODO: ADJUST FETCH FOR FINAL
    rows = cur.fetchall()
    # rows = cur.fetchmany(100)
    return rows


def standardize(row_tup: tuple) -> tuple:
    word_list = [word.lower() for word in row_tup[10].split()]
    stnd_word_list = []
    for word in word_list:
        en_str = word.encode('ascii', 'ignore')
        de_str = en_str.decode()
        # FIXME: TOO MANY WORDS WITH - INCLUDE UNICODE ERRORS
        # if '-' in word:
        #     sym_word = word
        # else:
        sym_word = re.sub(r'[^a-z]+', '', de_str)
        stnd_word_list.append(sym_word)
    stnd_word_str = ' '.join(stnd_word_list)
    stnd_word_list = stnd_word_str.split()
    return row_tup + (stnd_word_list,)


# TODO: remove stop-words
# TODO: stemming and lemmatization


def make_corpus(all_docs: list) -> list:
    documents = []
    doc = (doc_tup for doc_tup in all_docs)
    for document in all_docs:
        this_doc = next(doc)
        if this_doc[2] in [dc.short_name for dc in documents]:
            for dc in documents:
                if dc.short_name == this_doc[2]:
                    dc.add_text_row(document)
        else:
            documents.append(Document(this_doc))
    return documents


def write_corpus(docs: list) -> None:
    """Writes documents to individual .cor files"""
    for bill in docs:
        title = bill.short_name
        texts = [doc['stnd_row_text'] for doc in bill.texts]
        file_name = title + '.cor'
        with open('corpus_docs\\' + file_name, 'w') as file:
            for sent in texts:
                try:
                    sent_line = ' '.join(sent)
                    file.write(sent_line + '\n')
                except UnicodeEncodeError as e:
                    print('Unicode Error:\n', file_name, e)
                    print(sent_line)


def db_load(docs: list) -> None:
    """Loads document items into Postgres database"""
    for bill in docs:
        title = bill.short_name
        sum1, sum2, sum3 = bill.summary_1, bill.summary_2, bill.summary_3
        for text in bill.texts:
            blend_id = text['blend_id']
            row_num = text['row_number']
            row_text = text['row_text']
            stnd_text = ' '.join(text['stnd_row_text'])

            cur.execute("""INSERT INTO stnd_row_text (blend_id, row_number, row_text, stnd_text_list, short_name, 
                        sum1, sum2, sum3) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (blend_id, row_num, row_text, stnd_text, title, sum1, sum2, sum3))
            conn.commit()


# SECTION: MAIN()
params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()

# NOTE: text_rows tuple format...
# 00 = {str} id # 01 = {str} blend_id # 02 = {str} short_name # 03 = {str} name # 04 = {str} full_title
# 05 = {str} short_title # 06 = {str} summary_1 # 07 = {str} summary_2 # 08 = {str} summary_3
# 09 = {int} row_number # 10 = {str} row_text

text_rows = get_rows()

stnd_rows = []
for row in text_rows:
    # NOTE: adds tup[11] = {list} stnd_row_text
    stnd_rows.append(standardize(row))

doc_list = make_corpus(stnd_rows)

db_load(doc_list)

# NOTE: INSPECT DOCUMENT OBJECT
# for bill in doc_list[:1]:
#     texts = [doc['stnd_row_text'] for doc in bill.texts]
#     corp_dictionary = corpora.Dictionary(texts)
#     print(corp_dictionary)
#     print(corp_dictionary.token2id)
#     corpus = [corp_dictionary.doc2bow(text) for text in texts]
#     print(corpus)

# NOTE: GET BILLS OVER 500 ROWS
# for bill in doc_list:
#     size = len(bill.texts)
#     if size >= 500:
#         print(size)

# NOTE: RECLAIM MEMORY
# del text_rows

cur.close()
conn.close()
