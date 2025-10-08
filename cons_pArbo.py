# -*- coding: utf-8 -*-
import pandas as pd
from itertools import combinations, repeat
import threading
import multiprocess as mp
from multiprocess import Pool

max_complexity = 5
tree = [[]]
for depth in range(max_complexity + 1):
    tree.append([])
import math
sufficient = True
def queryPairs(pairs, df):
    r2 = []
    for i in range(len(df)):
        # if i % 10000 == 0:
        #     print("Processing: ", i)
        data = df.iloc[i]
        isThere = True
        for pair in pairs:
            if pair[-2] == "eq":
                if pair[0] != data[pair[-1]]:
                    isThere = False
            if pair[-2] == "within":
                if data[pair[-1]] <= pair[0] or data[pair[-1]] >= pair[1]:
                    isThere = False
        if isThere:
            r2.append(i)
            # print("**************     BELOW    ***************")
            # print(data)
            # #print(data.values)
            # print("*******************************************")
            
    return r2

def condIndeCheck(r1, r2, rc, df):
    inter_temp = list(set(r1).intersection(rc))
    c = len(inter_temp)
    bc = len(list(set(r2).intersection(inter_temp)))
    return bc, c
    
def corrCheckK(r1, r2, df_len):
    # ------------------------------part 1 ---------------------------
    # r2 = []
    # for i in range(len(df)):
    #     # if i % 10000 == 0:
    #     #     print("Processing: ", i)
    #     data = df.iloc[i]
    #     isThere = True
    #     for pair in pairs2:
    #         if pair[-2] == "eq":
    #             if pair[0] != data[pair[-1]]:
    #                 isThere =  False
    #         if pair[-2] == "within":
    #             if data[pair[-1]] < pair[0] or data[pair[-1]] >= pair[1]:
    #                 isThere = False
    #     if isThere:
    #         r2.append(i)
            # print("**************     BELOW    ***************")
            # print(data)
            # #print(data.values)
            # print("*******************************************")
    # ------------------------------part 1 ---------------------------        
    # r2_real = []
    # for r2_one in r2:
    #     if r2_one < len(df):
    #         r2_real.append(r2_one)
    # print(r2_real)
    if len(r1) == 0:
        return [0, 0]
    else:
        a = len(list(set(r1).intersection(r2)))
        b = len(r1) - a
        c = len(r2) - a
        d = df_len - len(r1) - len(r2) + a 
        s = a + b + c + d
        # print("-----------------------------------")
        # print(r2)
        # print(a, b, c, d)
        if s == 0.0:
            return [s, s]
        else:
            p1 = (a + d)/s
            p2_1 = (a + b)*(a + c)/(s*s)
            p2_2 = (c + d)*(b + d)/(s*s)
            p2 = p2_1 + p2_2
            if 1-p2 == 0.0:
                return [s, s]
            corrk = (p1 - p2)/(1 - p2)
            # if corrk < 0:
            #     print(p1, p2)
            #     print(a, b, c, d)
            sd = math.sqrt((p1*(1-p1))/(1-p2)**2)
            if sufficient:
                sd = 1
            return [corrk, sd]
def month_converter(utc):
    month_dict = {"Jan": "01", "Feb" : "02", "Mar" : "03", "Apr" : "04", 
                  "May" : "05", "June" : "06", "July" : "07", "Aug" : "08",
                  "Sep" : "09", "Oct" : "10", "Nov" : "11", "Dec" : "12"}
    utc_all = utc.split()
    return int(utc_all[-1] + month_dict[utc_all[1]] + utc_all[2] + utc_all[3].split(":")[0] + utc_all[3].split(":")[1])

def generateCategoricalPairs(values, attr):
    pairs = []
    for value in values:
        pairs.append([value, "eq", attr])
    return pairs

def generateNumericalPairs(minV, maxV, length, attr):
    pairs = []
    steps = int((maxV-minV)/length) + 1
    for i in range(steps):
        pairs.append([minV + i*length, minV + (i+1)*length, "within", attr])
    return pairs   

class Node:
    def __init__(self, pairs):
        self.q = None
        self.pairs = pairs
        self.child = None
        self.parent = None
    def setChild(self, child):
        self.child = child
    def setParent(self, parent):
        self.parent = parent
    def getPairs(self):
        return self.pairs
    def query(self, data_all):
        isThereIndex = []
        for i in range(len(data_all)):
            if i % 10000 == 0:
                print("Processing: ", i)
            data = data_all.iloc[i]
            isThere = True
            for pair in self.pairs:
                if pair[-2] == "eq":
                    if pair[0] != data[pair[-1]]:
                        isThere =  False
                if pair[-2] == "within":
                    if data[pair[-1]] < pair[0] or data[pair[-1]] > pair[1]:
                        isThere = False
            if isThere:
                isThereIndex.append(i)
                print("**************     BELOW    ***************")
                print(data)
                #print(data.values)
                print("*******************************************")
        return isThereIndex
    
class Tree:
    def __init__(self, root):
        self.root = root
        self.depth = 0
        self.nodes = [[root]]
        self.newDepth()
        
    def getNodes(self, depth):
        return self.nodes[depth]
    
    def getDepth(self):
        return self.depth
    
    def newNode(self, node):
        self.nodes[self.depth].append(node)
            
    def newDepth(self):
        self.nodes.append([])
        self.depth = self.depth + 1

def convertDataToPairs(data, attr, mins):
    categorical_columns = ["name", "venue", "brand", "country"]
    if attr in categorical_columns:
        return [data, "eq", attr]
    elif attr == "lati" or attr == "long":
        minv = mins[attr]
        length = 0.001
        minx = (float(data) - ((float(data) - minv)%length))
        maxx = minx + length 
        return [minx, maxx, "within", attr]
    else:
        minv = mins[attr]
        length = 1
        minx = (float(data) - ((float(data) - minv)%length))
        maxx = minx + length
        
        return [minx, maxx, "within", attr]

def convertTupleToPairsSet(data, mins):
    pairsSet = []
    for index in data.index.values:
        
        pairsSet.append(convertDataToPairs(data[index], index, mins))
    return pairsSet


def growAtDepth(df, depth, df_min):
    import pandas as pd
    from cons_pArbo import corrCheckK
    from itertools import combinations, repeat
    from cons_pArbo import convertTupleToPairsSet
    tree_at_depth = []
    combs = combinations(df.columns.values, depth)
    attr_combs = [list(comb) for comb in combs]
    for attr in attr_combs:
        #print(attr)
        df_attr = df[attr]
        data_collected = []
        for i in range(len(df_attr)):
            data = df_attr.iloc[i]
            if list(data.values) not in data_collected:
                data_collected.append(list(data.values))
                # if i%1000 == 0:
                #     print(i)
                tree_at_depth.append(convertTupleToPairsSet(data, df_min))
    #tree.append(tree_at_depth)
    return tree_at_depth

if __name__ == '__main__':
    df = pd.read_csv('original_dataset.csv', sep = ",", nrows = 1000)
    
    names = pd.Categorical(df['name']).categories
    venus_names = pd.Categorical(df['venue']).categories
    countries = pd.Categorical(df['country']).categories
    #weeks = pd.Categorical(df['week']).categories
    brands = pd.Categorical(df['brand']).categories
    
    all_pairs = []
    all_pairs = all_pairs + generateCategoricalPairs(names, "name")
    all_pairs = all_pairs + generateCategoricalPairs(venus_names, "venue")
    all_pairs = all_pairs + generateCategoricalPairs(venus_names, "brand")
    all_pairs = all_pairs + generateCategoricalPairs(countries, "country")
    #all_pairs = all_pairs + generateCategoricalPairs(weeks, "week")
    
    
    mins_arc, maxs_arc = df.min(), df.max()
    mins = [mins_arc["time"], mins_arc["lati"], mins_arc["long"]]
    maxs = [maxs_arc["time"], maxs_arc["lati"], maxs_arc["long"]]
    
    all_pairs = all_pairs + generateNumericalPairs(mins[0], maxs[0], 1, "time")
    all_pairs = all_pairs + generateNumericalPairs(mins[1], maxs[1], 0.01, "lati")
    all_pairs = all_pairs + generateNumericalPairs(mins[2], maxs[2], 0.01, "long")

    
    from multiprocessing import Process
    from multiprocess import Pool
    import pandas as pd
    from cons_pArbo import corrCheckK
    from itertools import combinations, repeat
    import threading
    import multiprocess as mp
    from multiprocess import Pool
    #p = Pool(processes = 5)
    
    tree = [[]]
    max_complexity = 5
    for depth in range(1, max_complexity + 1):
        tree.append(growAtDepth(df, depth, mins_arc))
    
    import pickle
    with open("tree", "wb") as fp:
       pickle.dump(tree, fp)
       
       
    #----------------preprocessing back up--------------------------#
    # tree_unique = [[]]
    # for i in range(len(tree)):
    #     tree_at_i = []
    #     for pairs in tree[i]:
    #         if pairs not in tree_at_i:
    #             tree_at_i.append(pairs)
    #     tree_unique.append(tree_at_i)
    #----------------------------back up-----------------------------#
    
    
    #-------------------multithread process: disabled----------------------#
    # from multiprocessing import Process
    
    # for depth in range(1, max_depth + 1):
    #     growAtDepth(df, depth, mins_arc)
        #p.start()
        
    # max_depth = 3
    # for depth in range(1, max_depth):
    #     tree_at_depth = []
    #     combs = combinations(df.columns.values, depth)
    #     attr_combs = [list(comb) for comb in combs]
    #     print("attttttttttttr_______________combs")
    #     for attr in attr_combs:
    #         print(attr)
    #         df_attr = df[attr]
    #         for i in range(len(df_attr)):
    #             if i%100 == 0:
    #                 print(i)
    #                 tree_at_depth.append(convertTupleToPairsSet(df_attr.iloc[i], df.min()))

    # from itertools import repeat
    # with Pool(5) as p:
    #     print(p.map(growAtDepth, repeat(df), [1, 2]))
        
    # q = mp.Queue()
    # p = mp.Process(target = growAtDepth, args=(df, 1, mins_arc))
    # p.start()
    # print(q.get())
    # p.join()
    
    # pool = mp.Pool(2)
    # res = growAtDepth(df, 1)
    # res = pool.apply_async(growAtDepth, (df, 1, ))
    # test = res.get()

    # with Pool(20) as p:
    #     tree = [[],[],[],[]]
    #     p.map(growAtDepth, [1])
    
    # t1 = threading.Thread(target = growAtDepth, args=(df, 1))
    # t2 = threading.Thread(target = growAtDepth, args=(df, 2))
    
    # t1.start()
    # t2.start()
    
    # t1.join()
    # t2.join()
    
    # for d in range(max_depth):
    #     comb = combinations(df.columns.values, d)
    #     for i in comb:
    #         df_temp = df[list(i)]
    #         temp = df_temp.iloc(1)
    #         print(df_temp.iloc(1))
        
    # print(comb)
    # #root = Node([])
    # #tree = Tree(root)
    # root = []
    # tree = [[root], []]
    # for pair in all_pairs:
    #     new_node = Node(pair)
    #     new_node.query(df)
    #     new_node.append(all_pairs[i])
    #     tree[1].append(new_node)