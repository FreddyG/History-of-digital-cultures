from os import listdir
from os.path import isfile, join

directory = 'data'

# def read_files():
#     res = []
#     onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]

#     for file in onlyfiles:
#         with open(join(directory, file), "r") as f:
#             content = f.readlines()
#         content = [x.strip('\n') for x in content] 
#         res.append((file, content))

#     return res

import collections

onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
group_by_cafe = {}

for filename in onlyfiles:
    name = filename.split('.')[0]
    cafename = name.split('-')[0]
    with open(join(directory, filename), "r") as file:
        if not cafename in group_by_cafe:
            group_by_cafe[cafename] = []
        
        for line in file:
            group_by_cafe[cafename].extend(list(set(line.split())))

for k,v in group_by_cafe.items():
    wordcount = collections.Counter()
    wordcount.update(v)

    print('>>> '+k)
    for w in wordcount.most_common()[:100]:
        print(w)
