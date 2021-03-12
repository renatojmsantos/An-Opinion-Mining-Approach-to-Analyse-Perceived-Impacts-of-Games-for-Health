import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import wordcloud
from wordcloud import STOPWORDS, WordCloud
import nltk
from collections import Counter
from itertools import groupby
from nltk.stem import WordNetLemmatizer
import re   # regular expression
from nltk.tokenize import RegexpTokenizer

path = '../CSV/YT_10_03_2021_v6 - cópia 2.csv'
data = pd.read_csv(path,lineterminator='\n',encoding='utf-8')
#print("-----> ",len(data))

#file = open(path)
#numline = len(file.readlines())
#print (numline)

#with open(path) as file:
#	n_rows = len(file.readlines())
#print (f'Exact number of rows: {n_rows}')


#yt = pd.read_csv(path,nrows=5)
#print(len(yt))
#print(data.head())
#print(data.info())



text = data['Comment']
text.dropna(inplace=True) # se nao tiver nenhum texto


#remove emojis
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

text = text.astype(str).apply(lambda x: demoji(x))

listaPalavras = ["@rui ola","best game #yolo","my best  friend from   germany !!!!!!!!!! lol ...... ","beautifulllll","OMG", "YOU are goooood", "issijjsij","laranja","orange","how","fix this"]

c=0
for t in listaPalavras:
	c+=1
	print(t)
	if c > 200:
		break
	"""
	pal = t.split()	
	if (pal == " "):
	    pal = ""
	if ("#" in pal or "@" in pal):
		pal = ""    
	print(pal)
	"""
	tokeniser = RegexpTokenizer(r'\w+')
	tokens = tokeniser.tokenize(t)
	print(tokens)

	print("\n")

	


#data['cleanText'] = data['Comment'].astype(str)
#data['cleanText'] = data['cleanText'].apply(lambda x: demoji(x))


# antes de detetar linguagem, é preciso tratar palavras...
# letras repetidas
# abreviaturas
# erros ortográficos
#hashtags, mencoes , commentID
# OMG, ahahah, @ddddd, #dijdij
# urls....

# tudo em minusculas
#text = yt['text'].str.lower()
#print(text)
#data['cleanText'].dropna(inplace=True) # se nao tiver nenhum texto


print("#################\n")
# ----------------------------------------------------------------------------------------
"""
del data['Comment']
#del data['Video Description']

data['language'] = 0
count = 0
for i in range(0,len(data)):
    temp = data['cleanText'].iloc[i]
    count += 1
    try:
        data['language'].iloc[i] = detect(temp)
    except:
        data['language'].iloc[i] = "error"

only_english = data[data['language'] == 'en']
#only_english.head()
# ver se é um comentario relevante...
# se só tiver uma palavra e for um nome ou pronome talvez n seja...




#tokeniser = RegexpTokenizer(r'\w+')
#tokens = tokeniser.tokenize(text)
#print(tokens)

regex = r"[^0-9A-Za-z'\t]"
comentarios = only_english.copy()

comentarios['reg'] = comentarios['cleanText'].apply(lambda x:re.findall(regex,x))
comentarios['reg_comentarios'] = comentarios['cleanText'].apply(lambda x:re.sub(regex," ",x))

#dataset = comentarios[['reg_comentarios','Likes','Video Title','Channel','Comment ID','Video ID']].copy()
dataset = comentarios[['Video Title','videoID','reg_comentarios','CommentID','Likes','TimeStampComment','Channel','ChannelID','VideoPublishedAt','ViewsVideo','likesVideo','dislikesVideo','totalCommentsVideo']].copy()
dataset = dataset.rename(columns={"reg_comentarios":"Comment"})
print(dataset.head())
"""

#pathExport = "../CSV/clean/YT_clean1.csv"
#only_english.to_csv('cleanYoutube.csv', index=False, encoding='utf-8')

#dataset.to_csv(pathExport,index = False, encoding='utf-8')




