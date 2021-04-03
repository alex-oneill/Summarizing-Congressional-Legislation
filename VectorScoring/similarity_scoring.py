import gensim
import psycopg2
import smart_open
import logging
from configparser import ConfigParser


# SECTION: FUNCTIONS
def config(filename='../database.ini', section='postgres'):
    """Establishes connection to local postgres db with masked credentials"""
    parser = ConfigParser()
    parser.read(filename)
    db_conn = {}
    for param in parser.items(section):
        db_conn[param[0]] = param[1]
    return db_conn


# NOTE: NOT USED IF PULLING TEXT DIRECTLY FROM DB
def read_corpus(fname, tokens_only=False):
    """Reads in a text document formatted with each line as a single token and returns tagged documents"""
    with smart_open.open(fname, encoding='iso-8859-1') as f:
        for i, line in enumerate(f):
            tokens = gensim.utils.simple_preprocess(line, min_len=3)
            if tokens_only:
                yield tokens
            else:
                yield gensim.models.doc2vec.TaggedDocument(tokens, [i])


def fetch_from_db(short_name) -> list:
    """Fetches text rows from the cleaned table"""
    query = f"""SELECT blend_id, row_number, row_text, stnd_text_list, short_name, sum1, sum2, sum3
            FROM stnd_row_text 
            WHERE short_name = '{short_name}'
            ORDER BY row_number ASC"""
    cur.execute(query)
    rows = cur.fetchall()
    return rows


def make_corpus_DB(doc_tups: list) -> str:
    """Processes database yield, prepares into a corpus, and tags documents for model prep"""
    for blend_id, _, _, stnd_text, _, _, _, _ in doc_tups:
        tokens = gensim.utils.simple_preprocess(stnd_text, min_len=3)
        yield gensim.models.doc2vec.TaggedDocument(tokens, [blend_id])


def save_scores(score_tup: tuple) -> None:
    """Saves documents to the database with the corresponding tag and pos/neg score"""
    (blend_id, stnd_doc, pos, neg) = score_tup
    cur.execute("""INSERT INTO similarity_scores (blend_id, stnd_doc, pos, neg)
                VALUES (%s, %s, %s, %s)""",
                (blend_id[0], stnd_doc, pos, neg))
    conn.commit()


params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()

# SECTION: MODEL PREP
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# NOTE: picked test doc has 10k+ lines
doc_name = '116hr2500'
doc_attributes = fetch_from_db(doc_name)
train_corpus = list(make_corpus_DB(doc_attributes))

# SECTION: MODEL DESIGN
vec_size = 24
epoch = 100
model = gensim.models.doc2vec.Doc2Vec(vector_size=vec_size, min_count=5, epochs=epoch, dm=1, alpha=0.025,
                                      min_alpha=0.020)
model.build_vocab(train_corpus)

model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)

# SECTION: MODEL EVALUATION
doc_scores = []
for doc_id in train_corpus:
    # GETS VECTOR FOR DOC_ID WORDS
    inferred_vector = model.infer_vector(doc_id.words, epochs=epoch)
    # MAKES LIST OF MOST SIMILAR VECTORS TO DOC id TUPLES (DOC-ID, SCORE)
    sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))

    # NOTE: GET POS/NEG VECTOR COUNTS
    pos, neg = 0, 0
    for doc in sims:
        if doc[1] >= 0:
            pos += 1
        else:
            neg += 1
    doc_scores.append((doc_id.tags, pos, neg))

# NOTE: PRINTS/STORES POS/NEG DOC COUNTS
for doc in doc_scores:
    for item in train_corpus:
        if doc[0] == item.tags:
            scored_doc = (doc[0], ' '.join(item.words), doc[1], doc[2])
            save_scores(scored_doc)
            # print('\nDocument ({}): <<{}>>'.format(doc[0], ' '.join(item.words)))
            # print('POS: {}\tNEG: {}'.format(doc[1], doc[2]))

cur.close()
conn.close()
