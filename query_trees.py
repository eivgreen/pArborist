# -*- coding: utf-8 -*-
from cons_pArbo import corrCheckK
from cons_pArbo import queryPairs
from cons_pArbo import condIndeCheck
import pandas as pd

def queryAllPairsInDf(tree, df, complexity):
    from cons_pArbo import queryPairs
    que_res = []
    que_res_temp = []
    for i in range(len(tree[complexity])):
        if i % 100 == 0:
            print("query all pairs")
            print(i)
        que_res_temp.append(queryPairs(tree[complexity][i], df))
    que_res[complexity] = que_res_temp
    return que_res

df = pd.read_csv('original_dataset.csv', sep = ",", nrows = 1000)
max_complexity = 5
que_res = [[]]

#-------------------------------------------------------------------------#
# from itertools import repeat
# from multiprocessing import Pool
# for j in range(1, max_complexity + 1):
#     que_res.append([])
#     comp_list.append(j)
# with Pool(20) as p:
#     p.map(queryAllPairsInDf, repeat(tree), repeat(df), comp_list))
#-------------------------------------------------------------------------#

if __name__ == '__main__':
    import pickle
    
    with open("tree", "rb") as fp:   # Unpickling
       tree = pickle.load(fp)
       
    for j in range(1, max_complexity + 1):
        que_res.append([])
        for i in range(len(tree[j])):
            if i % 100 == 0:
                print(i)
            que_res[j].append(queryPairs(tree[j][i], df))
            
    with open("que_res", "wb") as fp:
       pickle.dump(que_res, fp)

 
