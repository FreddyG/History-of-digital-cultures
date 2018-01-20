import numpy as np
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
from gensim import corpora, models, similarities
from os import listdir
from os.path import isfile, join


NLTK_DATA_PATH = '../venv/nltk_data'
RESOURCES = ['corpora/stopwords',
             'tokenizers/punkt']


def read_files2():
    res = []
    directory = 'data'
    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]

    for file in onlyfiles:
        f = open(join(directory, file), "r")
        name = file.split('.')[0]
        cafename = name.split('-')[0]
        date = name.split('-')[1] + '-' + name.split('-')[2]
        content = f.read().replace('\n', ' ')

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
    lines = [line.rstrip('\n') for line in open('our_stopwords.txt')]
    return nltk.corpus.stopwords.words('dutch') + lines


def tokenize(text):
    # first tokenize by sentence, then by word to ensure that punctuation
        # is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text)
                               for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if token in stopwords:
            continue
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


check_nltk_resources(NLTK_DATA_PATH)
stopwords = get_stopwords()


if __name__ == "__main__":
    in_memory_files = read_files2()

    tokenized = [tokenize(x[2]) for x in in_memory_files]
    dictionary = corpora.Dictionary(tokenized)
    corpus = [dictionary.doc2bow(text) for text in tokenized]

    tfidf = models.TfidfModel(corpus)   # train model
    corpus_tfidf = tfidf[corpus]        # transform documents

    # initialize an LSI transformation
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=300)

    # text = "Hallo meiden van TEchnika 10 Zijn er meisjes van de vierwindstreken in het cafe Ik Pia zit nu ook in het cafe en wil graag aan jullie vragen hoe het vandaag gaat met de Meisjes Internet Club."
    # bow_vector = dictionary.doc2bow(tokenize(text))
    # print([(dictionary[id], count) for id, count in bow_vector])

    # lsi_vector = lsi[bow_vector]
    # print(lsi_vector)
    # print(lsi.print_topic(max(lsi_vector, key=lambda item: item[1])[0]))

    dic = {}
    for f in in_memory_files:
        if not f[0] in dic:
            dic[f[0]] = []

    for f in in_memory_files:
        bow_vector = dictionary.doc2bow(tokenize(f[2]))
        lsi_vector = lsi[bow_vector]
        if not lsi_vector:
            continue
        keywords = lsi.show_topic(max(lsi_vector, key=lambda item: item[1])[0])

        lst = []
        for word_weight in keywords:
            lst.append({"keyword":word_weight[0], "weight":word_weight[1]})

        dic[f[0]].append({f[1]: lst})

    import json
    with open('keywords1.json', 'w') as f:
        json.dump(dic, f, ensure_ascii=False)
