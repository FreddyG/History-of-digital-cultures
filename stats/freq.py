from os import listdir
from os.path import isfile, join
import collections

directory = 'data'

onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
group_by_cafe = {}

for filename in onlyfiles:
    name = filename.split('.')[0]
    cafename = name.split('-')[0]
    with open(join(directory, filename), "r") as file:
        if not cafename in group_by_cafe:
            group_by_cafe[cafename] = []
        
        for line in file:
            group_by_cafe[cafename].append(list(set(line.split())))

def count_word_freq():
    for k,v in group_by_cafe.items():
        wordcount = collections.Counter()
        for vv in v:
            wordcount.update(vv)

        print('>>> '+k)
        for w in wordcount.most_common()[:100]:
            print(w)


# count_word_freq()


stopwords = ["hallo", "hi", "hoi", "hey", "hai", "gegroet", "doei", "de mazzel", "hooi", "is er iemand", "iemand hier", "CU", "tot zo", "dag", "yo", "goedenavond", "goedemiddag", "goedenmiddag", "goedemorgen", "goede morgen", "goede avond", "goede middag"]

def count_stopword_messages():
    for k,v in group_by_cafe.items():
        wordcount = collections.Counter()
        for vv in v:
            wordcount.update(list(set(stopwords).intersection(vv)))

        print('>>> '+k)
        for w in wordcount.most_common()[:100]:
            print(w)


count_stopword_messages()