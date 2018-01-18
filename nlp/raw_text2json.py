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


def read_files():
    asd = {}
    directory = 'data'
    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]

    for file in onlyfiles:
        f = open(join(directory, file), "r")
        name = file.split('.')[0]
        cafename = name.split('-')[0]
        date = name.split('-')[1] + '-' + name.split('-')[2]
        content = f.read().replace('\n', ' ')[:10]

        if date in asd:
            asd[date].append(content)
        else:
            asd[date] = []

        f.close()
    return asd


def check_nltk_resources(path):
    for res in RESOURCES:
        try:
            nltk.data.find(res)
        except LookupError:
            nltk.download(res.split('/')[1], path)

def get_stopwords():
    lines = [line.rstrip('\n') for line in open('our_stopwords.txt')]
    return nltk.corpus.stopwords.words('dutch') + lines

check_nltk_resources(NLTK_DATA_PATH)
stopwords = get_stopwords()

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


def dump_keywords(lst):
    topic_keywords = []
    for item in lst:
        date = item[0]
        topics = item[1]
        dictionary = {"date": date, "topics": []}
        for topic in topics:
            topic_keywords1 = []
            for keyword in topic[1]:
                d={"keyword":keyword[0], "weight":keyword[1]}
                topic_keywords1.append(d)
            dictionary["topics"].append(topic_keywords1)
        topic_keywords.append(dictionary)

    import json
    with open('keywords.json', 'w') as f:
        json.dump(topic_keywords, f, ensure_ascii=False)


if __name__ == "__main__":
    files = read_files()
    lst = []
    for time_period, texts in files.items():
        tokenized = [tokenize(text) for text in texts]
        dictionary = corpora.Dictionary(tokenized)
        corpus = [dictionary.doc2bow(text) for text in tokenized]

        tfidf = models.TfidfModel(corpus)   # train model
        corpus_tfidf = tfidf[corpus]        # transform documents

        # initialize an LSI transformation
        lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
        # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
        corpus_lsi = lsi[corpus_tfidf] 
        topics = lsi.show_topics(formatted=False)

        lst.append((time_period, topics))

    dump_keywords(lst)
