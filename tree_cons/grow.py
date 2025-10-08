# -*- coding: utf-8 -*-
from calculations import corrCheckK
from itertools import combinations, repeat
import threading

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

def convertDataToPairs(data, attr):
    if attr in categorical_columns:
        return [data, "eq", attr]
    elif attr == "lati" or attr == "long":
        minv, maxv = mins_arc[attr], maxs_arc[attr]
        length = 0.001
        minx = (data - ((data - minv)%length))
        maxx = minx + length
        return [minx, maxx, "within", attr]
    else:
        minv, maxv = mins[attr], maxs[attr]
        length = 2400
        minx = (data - ((data - minv)%length))
        maxx = minx + length
        return [minx, maxx, "within", attr]

def convertTupleToPairsSet(data):
    pairsSet = []
    for index in data.index.values:
        pairsSet.append(convertDataToPairs(data[index], index))
    return pairsSet

# max_depth = 4
# root_node = Node([])
# tree = Tree(root_node)
# for d in range(1, max_depth):
#     combs = combinations(df.columns.values, d)
#     attr_combs = [list(comb) for comb in combs]
#     for attr in attr_combs:
#         print(attr)
#         df_attr = df[attr]
#         for i in range(len(df_attr)):
#             new_node = Node(convertTupleToPairsSet(df_attr.iloc[i]))
#             tree.newNode(new_node)
#     tree.newDepth()

def growAtDepth(df, depth):
    tree_at_depth = []
    combs = combinations(df.columns.values, depth)
    attr_combs = [list(comb) for comb in combs]
    for attr in attr_combs:
        print(attr)
        df_attr = df[attr]
        for i in range(len(df_attr)):
            tree_at_depth.append(convertTupleToPairsSet(df_attr.iloc[i]))
    return tree_at_depth

import multiprocessing as mp

if __name__ == '__main__':
    df_temp = df
    categorical_columns = ["name", "venue", "brand"]
    mins_arc, maxs_arc = df_temp.min(), df_temp.max()
    #mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=growAtDepth, args=(df_temp, 1, ))
    p.start()
    print(q.get())
    p.join()
    
    
# (back up) Different Methods for MultiThread Processing:
    # pool = mp.Pool(1)
    # #res = growAtDepth(df, 1)
    # res = pool.apply_async(growAtDepth, (df, 1))

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
    