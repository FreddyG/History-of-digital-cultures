import numpy as np
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
from gensim import corpora, models, similarities
from os import listdir
from os.path import isfile, join
from six import iteritems


NLTK_DATA_PATH = '../venv/nltk_data'
RESOURCES = ['corpora/stopwords',
             'tokenizers/punkt']


def yield_file_contents():
    directory = 'data'
    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
    for filename in listdir(directory):
        if not isfile(join(directory, filename)):
            continue

        with open(join(directory, filename), "r") as f:
            for line in f:
                yield tokenize(f.read())



def read_files2():
    res = []
    directory = 'data'
    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]

    for filename in onlyfiles:
        name = filename.split('.')[0]
        cafename = name.split('-')[0]
        date = name.split('-')[1] + '-' + name.split('-')[2]
        with open(join(directory, filename), "r") as f:
            content = f.read().replace('\n', ' ')
            content = tokenize(content)

        res.append((cafename, date, content))
        f.close()

    return res


def check_nltk_resources(path):
    for res in RESOURCES:
        try:
            nltk.data.find(res)
        except LookupError:
            nltk.download(res.split('/')[1], path)


def get_stopwords():
    stopwords = {line.lower().rstrip('\n') for line in open('our_stopwords.txt')}
    username_stopwords = {line.lower().rstrip('\n') for line in open('username_stopwords.txt')}
    return stopwords | username_stopwords | set(nltk.corpus.stopwords.words('dutch'))


def tokenize(text):
    # first tokenize by sentence, then by word to ensure that punctuation
        # is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text)
                               for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        token = token.lower()
        if token in stopwords or len(token) > 15:
            continue
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


check_nltk_resources(NLTK_DATA_PATH)
stopwords = get_stopwords()


if __name__ == "__main__":
    # in_memory_files = read_files2()

    # tokenized = [tokenize(x[2]) for x in in_memory_files]
    dictionary = corpora.Dictionary(yield_file_contents())
    once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
    dictionary.filter_tokens(once_ids)
    dictionary.compactify()
    corpus = [dictionary.doc2bow(text) for text in yield_file_contents()]

    tfidf = models.TfidfModel(corpus)   # train model
    corpus_tfidf = tfidf[corpus]        # transform documents

    # # initialize an LSI transformation
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=1000, onepass=False, power_iters=5)
    print(*lsi.show_topics(num_topics=-1), sep='\n')

    # text = "Hallo meiden van TEchnika 10 Zijn er meisjes van de vierwindstreken in het cafe Ik Pia zit nu ook in het cafe en wil graag aan jullie vragen hoe het vandaag gaat met de Meisjes Internet Club."
    # bow_vector = dictionary.doc2bow(tokenize(text))
    # print([(dictionary[id], count) for id, count in bow_vector])

    # lsi_vector = lsi[bow_vector]
    # print(lsi_vector)
    # print(lsi.print_topic(max(lsi_vector, key=lambda item: item[1])[0]))

    # dic = {}
    # for f in in_memory_files:
    #     if not f[0] in dic:
    #         dic[f[0]] = []

    # for f in in_memory_files:
    #     bow_vector = dictionary.doc2bow(tokenize(f[2]))
    #     lsi_vector = lsi[bow_vector]
    #     if not lsi_vector:
    #         continue
    #     keywords = lsi.show_topic(max(lsi_vector, key=lambda item: item[1])[0])

    #     lst = []
    #     for word_weight in keywords:
    #         lst.append({"keyword":word_weight[0], "weight":word_weight[1]})

    #     dic[f[0]].append({f[1]: lst})

    # import json
    # with open('keywords1.json', 'w') as f:
    #     json.dump(dic, f, ensure_ascii=False)
