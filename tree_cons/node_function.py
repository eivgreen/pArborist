# -*- coding: utf-8 -*-
from calculations import corrCheckK
from calculations import queryPairs
from calculations import condIndeCheck
import pandas as pd
max_complexity = 5

def queryAllPairsInDf(tree, df, complexity):
    from calculations import queryPairs
    que_res_temp = []
    for i in range(len(tree[complexity])):
        if i % 100 == 0:
            print(i)
        que_res_temp.append(queryPairs(tree[j][i], df))
    que_res[complexity] = que_res_temp
    
def derive_pairs(seed_pairs, que_res, df, repeat = False):
    derived_pairs_list = []

    for seed_pair in seed_pairs:
        r1 = queryPairs(seed_pair, df)
        comp_list = [[]]
        derived_pairs = []
        thres = 0.5
        for j in range(1, max_complexity):
            comp_list.append([])
            for i in range(len(que_res[j])):
                corr_temp = corrCheckK(r1, que_res[j][i], df) 
                #print(corr_temp)
                if corr_temp[0] >= thres or corr_temp[0] <= -thres:
                    comp_list[j].append([i, corr_temp])
                    #derived_pairs.append([corr_temp[0], corr_temp[1]] + tree[j][i])
                    temp_pairs = [corr_temp[0], corr_temp[1]] + tree[j][i]
                    if temp_pairs not in derived_pairs:
                        if not repeat:
                            temp = 0
                            for p in seed_pair:
                                if p in tree[j][i]:
                                    temp = temp + 1
                            if temp != len(seed_pair):
                                derived_pairs.append(temp_pairs)
                        else:
                            derived_pairs.append(temp_pairs)
        # for j in range(1, max_complexity):
        #     for i in range(len(que_res[j])):
        #     for pairs in temp:
        #         derived_pairs.append(tree[j][pairs[0]])
        derived_pairs_list.append(derived_pairs)
    return derived_pairs_list

if __name__ == '__main__':
    import pickle
    import pandas as pd
    with open("que_res", "rb") as fp:   # Unpickling
       que_res = pickle.load(fp)
    with open("tree", "rb") as fp:   # Unpickling
       tree = pickle.load(fp)
    df = pd.read_csv('dataset_cleaned.csv', sep = ",", nrows = 10000)
    seed_pairs = [[["4693d828f964a520d3481fe3", "eq", "venue"]],
                  [['123234', 'eq', 'name']]]
    derived_pairs_list = derive_pairs(seed_pairs, que_res, df, repeat = False)
    
    for derived_pairs in derived_pairs_list:
        for result in derived_pairs:
            print(result)
