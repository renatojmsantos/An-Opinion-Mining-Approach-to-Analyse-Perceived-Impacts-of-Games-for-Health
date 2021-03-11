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


path = '../CSV/YT_10_03_2021_v6 - cópia 2.csv'
yt = pd.read_csv(path)
print(len(yt))

with open(path) as file:
	n_rows = len(file.readlines())
print (f'Exact number of rows: {n_rows}')


yt = pd.read_csv(path,nrows=5)
print(len(yt))
print(yt.head())
print(yt.info())


def demoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U00010000-\U0010ffff"
                               "]+", flags=re.UNICODE)
    return (emoji_pattern.sub(r'', text))



"""
newyear20=0
for i in range (-1,12): #(-1,12)
    change = 0 
    #text = '201'+str(i)+'ss'
    #before = '2010-01-01T00:00:00Z'
    #after = '2011-01-01T00:00:00Z'
    #print(j)
    if(i==-1): #jd lancado em nov de 2009
        #before = '2009-06-01T00:00:00Z'
        #after = '2010-01-01T00:00:00Z'
        before = '2014-06-01T00:00:00Z'
        after = '2015-01-01T00:00:00Z'

    for j in range(2):
        #time.sleep(60*4) #86400 = 1 dia sleep, 3600s = 1h
        print(" .... NOVO INTERVALO DE TEMPO")
        if(j%2==0):
	        #mes 1
	        j=1
        else: 
            #mes 6
            j=6
        if(i<10 and i>=5 or i<=-1):
            if (i == -1):
                if (j%2==0): # ir buscar os ultimos 6 meses de 2009
                    pass
                else:
                    continue
            else:
                #time.sleep(60*4) #86400 = 1 dia sleep, 3600s = 1h
                if(j==1):
                    a = 6
                else:
                    a = 1
                #print("$ ",change)
                before = '201'+str(i)+'-0'+str(j)+'-01T00:00:00Z'
                if((i+1) == 10): #2020
                    if(change==1):
                        #after = '2020-0'+str(a)+'-01T00:00:00Z'
                        after = '2020-0'+str(a)+'-01T00:00:00Z'
                    else:
                        after = '2019-0'+str(a)+'-01T00:00:00Z'
                else: #2010 - 2019
                    print(change)
                    if(change==1):
                        after = '201'+str(i+1)+'-0'+str(a)+'-01T00:00:00Z'
                    else:
                        after = '201'+str(i)+'-0'+str(a)+'-01T00:00:00Z' 
        elif(i>=10): #2021
            #time.sleep(60*5) #86400 = 1 dia sleep, 3600s = 1h
            i=20
            #ano=[20,20,21,21]
            if(j==1):
                a = 6
            else:
                a = 1
            #print("#",change)
            #print(i)
            #print(ano[change])

            newyear20+=1
            if(newyear20 <= 2):
                print("False")
                before = '20'+str(i)+'-0'+str(j)+'-01T00:00:00Z'
                #before = '20'+str(ano[change])+'-0'+str(j)+'-01T00:00:00Z'
                if(change==1):
                    after = '20'+str(i+1)+'-0'+str(a)+'-01T00:00:00Z'
                    
                else:
                    after = '20'+str(i)+'-0'+str(a)+'-01T00:00:00Z'

            if(newyear20 > 2):
                print("True")
                y=21
                before = '20'+str(y)+'-0'+str(j)+'-01T00:00:00Z'
                #before = '20'+str(ano[change])+'-0'+str(j)+'-01T00:00:00Z'
                if(change==1):
                    newyear20+=1
                    after = '20'+str(y+1)+'-0'+str(a)+'-01T00:00:00Z'
                else:
                    after = '20'+str(y)+'-0'+str(a)+'-01T00:00:00Z'
        else:
        	continue
            
        change+=1

        print(before)
        print(after)
"""
