import random
import gensim
import smart_open
import collections
import logging


# SECTION: FUNCTIONS
def read_corpus(fname, tokens_only=False):
    with smart_open.open(fname, encoding='iso-8859-1') as f:
        for i, line in enumerate(f):
            # if len(line.strip().split()) == 1:
            #     logging.info('Line Dropped: {}'.format(line))
            #     continue
            # else:
            #     tokens = gensim.utils.simple_preprocess(line, min_len=3)
            #     if tokens_only:
            #         yield tokens
            #     else:
            #         yield gensim.models.doc2vec.TaggedDocument(tokens, [i])
            tokens = gensim.utils.simple_preprocess(line, min_len=3)
            if tokens_only:
                yield tokens
            else:
                yield gensim.models.doc2vec.TaggedDocument(tokens, [i])

# SECTION: MODEL PREP
# FIXME: LOGGING IS OFF
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# NOTE: picked test doc has 10k+ lines
train_corpus = list(read_corpus('corpus_docs\\116hr2500.cor'))

# TODO: test and adjust model used for smaller docs
# SECTION: EPOCH TESTING
for epoch in range(40, 120, 20):
    for vec_size in range(24, 60, 12):
        model = gensim.models.doc2vec.Doc2Vec(vector_size=vec_size, min_count=5, epochs=epoch, dm=1, alpha=0.025,
                                              min_alpha=0.020)
        model.build_vocab(train_corpus)

        model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)

        # SECTION: MODEL EVALUATION
        ranks = []
        second_ranks = []
        sim_hits = []
        last_rank = []
        # rand_docs = [random.randrange(0, len(train_corpus) - 1) for i in range(15)]
        # rand_docs = [random.randrange(0, 100) for i in range(5)]
        doc_scores = []
        for doc_id in range(len(train_corpus)):
        # for num in range(15):
        #     doc_id = random.randint(0, len(train_corpus) - 1)
            # NOTE: GETS VECTOR FOR DOC_ID WORDS
            inferred_vector = model.infer_vector(train_corpus[doc_id].words, epochs=epoch)
            # NOTE: MAKES LIST OF MOST SIMILAR VECTORS TO DOC id TUPLES (DOC-ID, SCORE)
            sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
            # NOTE: STORES RANK OF ITSELF
            rank = [docid for docid, sim in sims].index(doc_id)
            ranks.append(rank)
            second_ranks.append(sims[1])
            last_rank.append(sims[-1])

            # NOTE: GET POS/NEG VECTOR COUNTS
            pos, neg = 0, 0
            for doc in sims:
                if doc[1] >= 0:
                    pos += 1
                else:
                    neg += 1

            doc_scores.append((doc_id, pos, neg))

        # NOTE: PRINTS POS/NEG DOC COUNTS
        # for doc in doc_scores:
        #     print('\nDocument ({}): <<{}>>'.format(doc[0], ' '.join(train_corpus[doc[0]].words)))
        #     print('POS: {}\tNEG: {}'.format(doc[1], doc[2]))

        counter = collections.Counter(ranks)
        v_lt_five, v_lt_ten, v_lt_twenty = 0, 0, 0
        total_docs = sum(counter.values())
        for k, v in counter.items():
            if k < 5:
                v_lt_five += counter[k]
            if k < 10:
                v_lt_ten += counter[k]
            if k < 20:
                v_lt_twenty += counter[k]
        print(f'\nModel: {model}')
        print('\nTop 5 Count: {}/{}: {}%'.format(v_lt_five, total_docs, (v_lt_five / total_docs) * 100))
        print('\nTop 10 Count: {}/{}: {}%'.format(v_lt_ten, total_docs, (v_lt_ten / total_docs) * 100))
        print('\nTop 20 Count: {}/{}: {}%'.format(v_lt_twenty, total_docs, (v_lt_twenty / total_docs) * 100))
        print(f'\nEpochs: {epoch}\tVector_Size: {vec_size}')
        # print(list(counter.items()))
        print('\n'*2)
        with open('epoch_vec_test.txt', 'a') as outfile:
            outfile.write(f'\nModel: {model}')
            outfile.write('\nTop 5 Count: {}/{}: {}%'.format(v_lt_five, total_docs, (v_lt_five / total_docs) * 100))
            outfile.write('\nTop 10 Count: {}/{}: {}%'.format(v_lt_ten, total_docs, (v_lt_ten / total_docs) * 100))
            outfile.write('\nTop 20 Count: {}/{}: {}%'.format(v_lt_twenty, total_docs, (v_lt_twenty / total_docs) * 100))
            outfile.write(f'\nEpochs: {epoch}\tVector-Size: {vec_size}\n\n')
            # outfile.write('\n'+str(list(counter.items())))
            outfile.write('\n'*2)
# SECTION: RANDOM PRINTING FORMATS
# NOTE: check random docs for similar and least-similar rows
# if doc_id in rand_docs:
#     sim_hits.append(sims)
    # print('\nDocument ({}): «{}»'.format(doc_id, ' '.join(train_corpus[doc_id].words)))
    # print(u'\nSIMILAR/DISSIMILAR DOCS PER MODEL %s:' % model)
    # for label, index in [('MOST SIMILAR', 0), ('SECOND-MOST SIMILAR', 1)]:
    #     print(u'%s %s: «%s»' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))
    # for i in range(0, 4)[::-1]:
    #     # for label, index in [('LEAST-{} SIMILAR'.format(i), len(sims) - i)]:
    #     label, index = ('LEAST-{} SIMILAR'.format(i), len(sims) - i)
    #     print(u'%s %s: «%s»' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))

# print('\nDocument ({}): «{}»'.format(doc_id, ' '.join(train_corpus[doc_id].words)))
# print(u'\nSIMILAR/DISSIMILAR DOCS PER MODEL %s:' % model)
# for label, index in [('MOST SIMILAR', 0), ('SECOND-MOST SIMILAR', 1)]:
#     print(u'%s %s: «%s»' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))
# NOTE: can use to see how many documents are most similar to themself. Will need to infer model for all
#   documents above then evaluate the counter output against the actual corpus size

# NOTE: default printing from doc2vec demo
# print('Second-Most Similar Document {}: «{}»\n'.format(sim_id, ' '.join(train_corpus[sim_id[1][0]].words)))
# print('Least Similar Document {}: «{}»\n'.format(sim_id, ' '.join(train_corpus[sim_id[-1][0]].words)))
# print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
# for label, index in [('MOST', 0), ('SECOND-MOST', 1), ('MEDIAN', len(sims)//2), ('LEAST', len(sims) - 1)]:
#     print(u'%s %s: «%s»' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))
