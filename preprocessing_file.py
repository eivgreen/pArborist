# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
df = pd.read_csv('dataset.csv', sep = ",", nrows = 100000)

threshold = 2
value_counts = df.stack().value_counts()
to_remove = value_counts[value_counts <= threshold].index
df.replace(to_remove, np.nan, inplace=True)
df = df.dropna()

df.to_csv('original_dataset.csv', index = False) 