import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import wordcloud
from wordcloud import STOPWORDS, WordCloud
import nltk
from collections import Counter
from itertools import groupby
from nltk.stem import WordNetLemmatizer
import re

path = '../CSV/YT_10_03_2021_v3.csv'
yt = pd.read_csv(path)
print(len(yt))

with open(path) as file:
	n_rows = len(file.readlines())
print (f'Exact number of rows: {n_rows}')


yt = pd.read_csv(path,nrows=5)
#print(len(yt))
print(yt.head())
print(yt.info())