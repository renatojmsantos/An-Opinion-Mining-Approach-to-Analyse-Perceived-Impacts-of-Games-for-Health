
import numpy as np
import pandas as pd


path='../csv/dataset.csv'
#path='../csv/data1.csv'

#path = 'YT_repliesDif-Descript-ALL'
#path = '../CSV/YT_10_03_2021_v6.csv'
data = pd.read_csv(path,lineterminator='\n',encoding='utf-8')

#print(data.info())
#print(len(data))
#print(data.head(10))
#print((len(data))
sorted_csv = data.sort_values(by=['Likes'], ascending=False)
#print(sorted_csv.head(20))
s = sorted_csv.head(1000)
s.to_csv("../csv/YT_dataset_top1000.csv",index = False)
#data.dropna(inplace=True)

#df = data.set_index("Comment", drop = False)
#data = pd.DataFrame(index=comments)

#csv_file = pandas.read_csv('JustDance.csv') # you can implement options as you want here)
#sorted_csv = data.sort_values(by=['Likes'], ascending=False)

#print(sorted_csv(25).to_csv("YT_dataset_top500.csv",index = False)
#sorted_csv.to_csv("Twitter_JD_sorted.csv",index = False)