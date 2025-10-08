# -*- coding: utf-8 -*-
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


if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    df = pd.read_csv('dataset.csv', sep = ",", nrows = 10000)

    threshold = 2 # Anything that occurs less than this will be removed.
    value_counts = df.stack().value_counts() # Entire DataFrame 
    to_remove = value_counts[value_counts <= threshold].index
    df.replace(to_remove, np.nan, inplace=True)
    df = df.dropna()
    
    df.to_csv('dataset_cleaned.csv', index=False) 

    names = pd.Categorical(df['name']).categories
    venus_names = pd.Categorical(df['venue']).categories
    #countries = pd.Categorical(df['country']).categories
    #weeks = pd.Categorical(df['week']).categories
    brands = pd.Categorical(df['brand']).categories
    
    all_pairs = []
    all_pairs = all_pairs + generateCategoricalPairs(names, "name")
    all_pairs = all_pairs + generateCategoricalPairs(venus_names, "venue")
    #all_pairs = all_pairs + generateCategoricalPairs(countries, "country")
    #all_pairs = all_pairs + generateCategoricalPairs(weeks, "week")
    all_pairs = all_pairs + generateCategoricalPairs(brands, "brand")
    
    mins = [mins_arc["time"], mins_arc["lati"], mins_arc["long"]]
    maxs = [maxs_arc["time"], maxs_arc["lati"], maxs_arc["long"]]
    
    all_pairs = all_pairs + generateNumericalPairs(mins[0], maxs[0], 1, "time")
    all_pairs = all_pairs + generateNumericalPairs(mins[1], maxs[1], 0.01, "lati")
    all_pairs = all_pairs + generateNumericalPairs(mins[2], maxs[2], 0.01, "long")

