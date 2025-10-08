# -*- coding: utf-8 -*-
from cons_pArbo import corrCheckK
from cons_pArbo import queryPairs
from cons_pArbo import condIndeCheck
import pandas as pd
max_complexity = 5

def queryAllPairsInDf(tree, df, complexity):
    from cons_pArbo import queryPairs
    que_res = []
    que_res_temp = []
    for i in range(len(tree[complexity])):
        if i % 100 == 0:
            print(i)
        que_res_temp.append(queryPairs(tree[complexity][i], df))
    que_res[complexity] = que_res_temp
    return que_res
    
def derive_pairs(seed_pairs, que_res, df, repeat = False):
    max_complexity = 5
    import pickle
    with open("cache/tree", "rb") as fp:   # Unpickling
       tree = pickle.load(fp)
    derived_pairs_list = []

    for i in range(len(seed_pairs)):
        # if i%100 == 0:
        #     print(i)
        seed_pair = seed_pairs[i]
        r1 = queryPairs(seed_pair, df)
        #print(r1)
        comp_list = [[]]
        derived_pairs = []
        thres = 0.5
        for j in range(1, max_complexity):
            comp_list.append([])
            for i in range(len(que_res[j])):
                #print(r1, que_res[j][i], len(df))
                corr_temp = corrCheckK(r1, que_res[j][i], len(df)) 
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

def translate_results(queries):
    if queries == []:
        return ["There is NO other privacy revealing data that exceeds " + "50%" + " probability."] 
    translate_results = []
    for query in queries:
        translate_results.append(translate_query(query))
    return translate_results
    
def translate_query(query):
    translated_query = "with " + str(abs(query[0])*100) + "% probability, activities"
    for i in range(2, len(query)):
        if i == 2:
            translated_query = translated_query + translate_pair(query[i])
        elif i == len(query) - 1:
            translated_query = translated_query + ", and" + translate_pair(query[i])
        elif i >= 3:
            translated_query = translated_query + "," + translate_pair(query[i])
        else:
            translated_query = translated_query + translate_pair(query[2])
    return translated_query + " are also privacy-revealing."
    
def translate_seed(seed):
    translated_seed = "the individual claims that the activities"
    for i in range(len(seed)):
        if i == 0:
            translated_seed = translated_seed + translate_pair(seed[i])
        elif i == len(seed) - 1:
            translated_seed = translated_seed + ", and" + translate_pair(seed[i])
        elif i >= 1:
            translated_seed = translated_seed + "," + translate_pair(seed[i])
        else:
            translated_seed = translated_seed + translate_pair(seed[i])
            
    return translated_seed + " are privacy-revealing"

def translate_pair(pair):
    if pair[-1] == 'name':
        return " under the name " + str(pair[0])
    elif pair[-1] == 'long':
        return " around Longitude: " + str(pair[0])
    elif pair[-1] == 'country':
        return " in country: " + str(pair[0])
    elif pair[-1] == 'lati':
        return " around Latitude: " + str(pair[0])
    elif pair[-1] == 'venue':
        return " in Hotel: " + str(pair[0])
    elif pair[-1] == 'brand':
        return " in brand: " + str(pair[0])
    elif pair[-1] == 'time':
        return " within time: (" + str(int(pair[0])) + ", " + str(int(pair[1])) + ")"
    else:
        return ""
    
def select_a_pair(data, index, attrs, isAny = 0):
    seed = []
    data_row = data.iloc[index-2]
    for attr in attrs:
        if attr == "name":
            if isAny == 1:
                seed.append(["any", "eq", "name"])
            else:
                seed.append([int(data_row[attr]), "eq", "name"])
        elif attr == "venue":
            if isAny == 2:
                seed.append(["any", "eq", "venue"])
            else:
                seed.append([data_row[attr], "eq", "venue"])
        elif attr == "brand":
            if isAny == 3:
                seed.append(["any", "eq", "brand"])
            else:
                seed.append([data_row[attr], "eq", "brand"])
        elif attr == "time":
            seed.append([data_row[attr] - 0.5, data_row[attr] + 0.5, "within", "time"])
        elif attr == "long":
            seed.append([round(data_row[attr] - 0.0005, 6), round(data_row[attr] + 0.0005, 6), "within", "long"])
        elif attr == "lati":
            seed.append([round(data_row[attr] - 0.0005, 6), round(data_row[attr] + 0.0005, 6), "within", "lati"])
    return seed

def compare_queries(query1, query2):
    if len(query1) != len(query2):
        return False
    else:
        for pair in query1:
            if pair not in query2:
                return False
        return True

if __name__ == '__main__':
    print("derive queries")
    print("debug")
    # import pickle
    # import pandas as pd
    # with open("que_res", "rb") as fp:   # Unpickling
    #    que_res = pickle.load(fp)
    # with open("tree", "rb") as fp:   # Unpickling
    #    tree = pickle.load(fp)
    # df = pd.read_csv('dataset_cleaned.csv', sep = ",", nrows = 10000)
    
    # df_oblig = pd.read_csv('original_dataset_oblig.csv', sep = ",", nrows = 2000)
    
    # seed_pairs = []
    
    # #seed_pairs = [[["3fd66200f964a52032f01ee3", "eq", "venue"], [951582, 'eq', 'name']]]
    
    # seed81 = select_a_pair(df_oblig, 418, ["name", "long", "lati"])
    # #seed82 = select_a_pair(df_oblig, 623, ["name", "venue", "brand", "long", "lati", "time", "country"])
    # #seed6_2 = select_a_pair(df_oblig, 6, ["brand", "long", "lati"])
    # # column_names = ["name", "venue", "time", "brand", "country", "long", "lati"]
    # # for i in range(5):
    # #     print(i)
    # #     for j in range(len(tree[i])):
    # #         print(j)
    # #         seed_pairs.append(tree[i][j])
    # #seed_pairs.append(seed81)
    # seed_pairs.append(seed81)

    # # seed_pairs.append(seed4_1)
    # # seed_pairs.append(seed4_2)
    # # seed_pairs.append(seed4_3)
    # # seed_pairs.append(seed4_4)
    # # seed_pairs.append(seed4_5)
    # # seed_pairs.append(seed4_6)
    # # seed_pairs.append(seed4_7)
    # # seed_pairs.append(seed4_8)
    # # seed_pairs.append(seed4_9)
    # # seed_pairs.append(seed4_10)
    
    # #print(seed_temp1)
    
    # derived_pairs_list = derive_pairs(seed_pairs, que_res, df_oblig, repeat = False)
    # all_shown_derived_pairs = []
    
    # from collections import Counter
    # for derived_pairs in derived_pairs_list:
    #     for result in derived_pairs:
    #         show_results = []
    #         for counter in range(len(result)):
    #             if counter >=2:
    #                 if result[counter][-1] == 'name':
    #                     result[counter][0] = str(int(result[counter][0]))
    #                 if result[counter][-1] == 'long':
    #                     result[counter][0] = str(round(float(result[counter][0]), 6))
    #                     result[counter][1] = str(round(float(result[counter][1]), 6))
    #                 if result[counter][-1] == 'lati':
    #                     result[counter][0] = str(round(float(result[counter][0]), 6))
    #                     result[counter][1] = str(round(float(result[counter][1]), 6))
    #                 if result[counter][-1] == 'time':
    #                     result[counter][0] = str(int(result[counter][0]))
    #                     result[counter][1] = str(int(result[counter][1]))
    #                 show_results.append((result[counter]))
    #             else:
    #                 show_results.append((result[counter]))
    #         #if compare_queries(show_results[2:], seed_pairs[0]):
    #         all_shown_derived_pairs.append(show_results)
    
    # for seed in seed_pairs:
    #     print(translate_seed(seed))
            
    # translated_results = translate_results(all_shown_derived_pairs)
    
    # for i in range(len(translated_results)):
    #     print("___________________________________________")
    #     print("(" + str(i+1) + ") " + translated_results[i])
    #     #print(" · " + translated_results[i])
