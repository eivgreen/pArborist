# -*- coding: utf-8 -*-

def month_converter(utc):
    utc_all = utc.split()
    return int(utc_all[-1] + month_dict[utc_all[1]] + utc_all[2])


df = df_p1.set_index('venue').join(df_p2.set_index('venue'))
df['week'] = df['UTC'].str.split(' ', n=1, expand=True)[0]
month_dict = {"Jan": "01", "Feb" : "02", "Mar" : "03", "Apr" : "04", 
              "May" : "05", "June" : "06", "July" : "07", "Aug" : "08",
              "Sep" : "09", "Oct" : "10", "Nov" : "11", "Dec" : "12"}
df['time'] = df['UTC'].apply(month_converter)
df = df.drop(columns=['UTC'])
df = df.drop(columns=['country'])
df = df.drop(columns=['week'])
df = df.drop(columns=['offset'])
#df = df.drop(columns=['index'])
columns = df.columns.values
categorical_columns = ["name", "venue", "country", "brand", "week"]
mins_arc, maxs_arc = df.min(), df.max()
df = df.reset_index()
df_arc = df

df.to_csv('dataset.csv', index=False) 

#df = df.sort_values(by = 'time')
