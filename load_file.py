# -*- coding: utf-8 -*-

import pandas as pd

if __name__ == '__main__':
    df_p1 = pd.read_csv('dataset_WWW_Checkins_anonymized.txt', sep = "\t", header = None, nrows = 100000, 
                        names = ['name', 'venue', 'UTC', 'offset'])
    
    df_p2 = pd.read_csv('raw_POIs.txt', sep = '\t', header = None, 
                        names = ['venue', 'lati', 'long', 'brand', 'country'])
