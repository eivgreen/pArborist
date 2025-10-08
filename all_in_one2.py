# -*- coding: utf-8 -*-
from calculations import corrCheckK
from calculations import queryPairs
from calculations import condIndeCheck
import pandas as pd

def queryAllPairsInDf(tree, df, complexity):
    from calculations import queryPairs
    que_res_temp = []
    for i in range(len(tree[complexity])):
        if i % 100 == 0:
            print(i)
        que_res_temp.append(queryPairs(tree[j][i], df))
    que_res[complexity] = que_res_temp
    
df = pd.read_csv('dataset_cleaned.csv', sep = ",", nrows = 10000)
max_complexity = 5
que_res = [[]]


# from itertools import repeat
# from multiprocessing import Pool
# for j in range(1, max_complexity + 1):
#     que_res.append([])
#     comp_list.append(j)
# with Pool(20) as p:
#     p.map(queryAllPairsInDf, repeat(tree), repeat(df), comp_list))

for j in range(1, max_complexity + 1):
    que_res.append([])
    for i in range(len(tree[j])):
        if i % 100 == 0:
            print(i)
        que_res[j].append(queryPairs(tree[j][i], df))
        
import pickle
with open("que_res", "wb") as fp:
   pickle.dump(que_res, fp)
with open("tree", "wb") as fp:
   pickle.dump(tree, fp)
 
