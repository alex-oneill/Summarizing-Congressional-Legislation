import random
import gensim
import smart_open
import collections

# import os
# test_data_dir = os.path.join(gensim.__path__[0], 'test', 'test_data')
# lee_train_file = os.path.join(test_data_dir, 'lee_background.cor')
# lee_test_file = os.path.join(test_data_dir, 'lee.cor')


# SECTION: FUNCTIONS
def read_corpus(fname, tokens_only=False):
    with smart_open.open(fname, encoding='iso-8859-1') as f:
        for i, line in enumerate(f):
            tokens = gensim.utils.simple_preprocess(line)
            if tokens_only:
                yield tokens
            else:
                yield gensim.models.doc2vec.TaggedDocument(tokens, [i])


# SECTION: MODEL
# NOTE: picked test doc has 10k+ lines
train_corpus = list(read_corpus('corpus_docs\\116hr2500.cor'))
# train_corpus = list(read_corpus(lee_train_file))

# TODO: test and adjust model used for smaller docs
model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count=2, epochs=20)
model.build_vocab(train_corpus)

model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)


# SECTION: MODEL EVALUATION
ranks = []
second_ranks = []
# for doc_id in range(len(train_corpus)):
for num in range(15):
    doc_id = random.randint(0, len(train_corpus) - 1)
    inferred_vector = model.infer_vector(train_corpus[doc_id].words)
    sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
    rank = [docid for docid, sim in sims].index(doc_id)
    ranks.append(rank)
    second_ranks.append(sims[1])

    # NOTE: check random docs for similar and least-similar rows
    print('\nDocument ({}): «{}»'.format(doc_id, ' '.join(train_corpus[doc_id].words)))
    for label, index in [('MOST SIMILAR', 0), ('SECOND-MOST SIMILAR', 1)]:
        print(u'%s %s: «%s»' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))
    for i in range(1, 6)[::-1]:
        for label, index in [('LEAST-{} SIMILAR'.format(i), len(sims) - i)]:
            print(u'%s %s: «%s»' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))

    # NOTE: can use to see how many documents are most similar to themself. Will need to infer model for all
    #   documents above then evaluate the counter output against the actual corpus size
    # counter = collections.Counter(ranks)
    # print(counter)

# NOTE: default printing from doc2vec demo
# print('Second-Most Similar Document {}: «{}»\n'.format(sim_id, ' '.join(train_corpus[sim_id[1][0]].words)))
# print('Least Similar Document {}: «{}»\n'.format(sim_id, ' '.join(train_corpus[sim_id[-1][0]].words)))
# print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
# for label, index in [('MOST', 0), ('SECOND-MOST', 1), ('MEDIAN', len(sims)//2), ('LEAST', len(sims) - 1)]:
#     print(u'%s %s: «%s»' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))
