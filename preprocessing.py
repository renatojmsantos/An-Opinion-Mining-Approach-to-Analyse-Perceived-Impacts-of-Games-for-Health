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
import demoji

import numpy as np
from nltk.corpus import wordnet

import regex

from langdetect import detect
from langdetect import DetectorFactory



from textblob import TextBlob

import time


#from abbr import expandall

DetectorFactory.seed = 0


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
#print(data)


#comments = data['Comment']
#comments.dropna(inplace=True) # se nao tiver nenhum texto

#print(data.shape)
data.dropna(inplace=True)

#df = data.set_index("Comment", drop = False)
#data = pd.DataFrame(index=comments)

comments = data['Comment']
commentID = data['CommentID']
videoTitle = data['Video Title']
videoID = data['videoID']
likes = data['Likes']
timestampComment = data['TimeStampComment']
channel = data['Channel']
channelID = data['ChannelID']
videoPublishedAt = data['VideoPublishedAt']
views = data['ViewsVideo']
likesVideo = data['likesVideo']
dislikesVideo = data['dislikesVideo']
totalCommentsVideo = data['totalCommentsVideo']


#print(comments[0])
#print(videoTitle[2])
#print(videoTitle[comments[4]])


#print(df)
#df.info()
#print("---")
#print(df.loc[: ,"Video Title"])
#print(data)

"""
 0   Video Title         208727 non-null  object
 1   videoID             208727 non-null  object
 2   Comment             208158 non-null  object
 3   CommentID           208727 non-null  object
 4   Likes               208727 non-null  int64 
 5   TimeStampComment    208727 non-null  object
 6   Channel             208727 non-null  object
 7   ChannelID           208727 non-null  object
 8   VideoPublishedAt    208727 non-null  object
 9   ViewsVideo          208727 non-null  int64 
 10  likesVideo          208727 non-null  int64 
 11  dislikesVideo       208727 non-null  int64 
 12  totalCommentsVideo  208727 non-null  int64 
 """

#demoji.download_codes()
#demoji.last_downloaded_timestamp()

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

#comment = comment.astype(str).apply(lambda x: demoji(x))

def isEnglish(text):

	time.sleep(0.10)
	#lang = TextBlob(text)
	#print(lang.detect_language())
	#language = lang.detect_language()

	#print(detect(text))
	language = detect(text)
	# procurar outro com maior accuracy ...
	
	if (language == "en"):
		return True
	else:
		return False
	

listaPalavras = ["🤗","l","I’d like to know how I’d done that!","I'd like to play!", "abc","sex","stop","this game/ is! great!","this is great", "isto é bom","i love thiq gam ","u know","hi","a","aaa","big https://wwww.uc.pt THE BEST url: http://blah.com/path/to/here?p=1&q=abc,def#posn2 #ahashtag http://t.co/FNkPfmii-","@rui ola 🙀🤗🤗🤗🤗","best game #yolo :)","my best  friend from   germany !!!!!!!!!! lol ...... ","beautifulllll","OMG 🤯", "YOU 🤯🤯🤯🤯are goooood ", "issijjsij","laranja","orange","how","fix this"]

def clearText(text):
	# remove emojis
	text = demoji(text)
	# remove URLs
	text = re.sub('https?://[A-Za-z0-9./?&=_]+','',text)
	# hashtags
	text = re.sub('#[A-Za-z0-9]+','',text)
	# mencoes
	text = re.sub('@[A-Za-z0-9._-]+','',text)
	# to lower
	text = text.lower()

	#https://pypi.org/project/pycontractions/
	# expand abreviaturas ...
	# remover pontuacao
	text = re.sub(r"[^\w\s]","",text)
	#remover espacos
	text = " ".join(text.strip().split())
	text = re.sub(r"[\W\s]"," ",text)
	text = re.sub("\n","",text)

	return text

def caracteresRepetidos(text):
	# é preciso ter em conta as palavras inglesas.... "good", "god", ... 
	# https://www.nltk.org/_modules/nltk/tokenize/casual.html#reduce_lengthening
	pattern = regex.compile(r"(.)\1{2,}")
	return pattern.sub(r"\1\1\1", text)


def spellCorrection(text):
	t = TextBlob(text).correct()
	#print(t)
	return t



def runPreprocessing(t):
	#print("running clean ... ")

	if(len(t) >= 3):
		#print("\n",t)
		t = clearText(t)
		#print(len(t))
		t = caracteresRepetidos(t)
		t = spellCorrection(t) # rever

		if (len(t) >= 3 and isEnglish(str(t))):
			return t
	return "None"

	"""
	c=0
	for t in comments:
		c+=1
		if(len(t) >= 3):
			print("\n",t)
			t = clearText(t)
			#print(len(t))
			t = caracteresRepetidos(t)
			t = spellCorrection(t)

			if (len(t) >= 3 and isEnglish(str(t))):
				print(">>",t)
			else:
				print(">> ---")
			# google clould ... 90 dias com 300$ ver e enviar docs
			
			try:
				if (len(t) >= 3 and isEnglish(str(t))):
					print(">>",t)
				else:
					print(">> ---")
			except:
				print("detect language - something wrong ...")
			
		if c > 200:
			break
	"""

#runPreprocessing(comments)
#print("#################\n")



# letras repetidas
# abreviaturas
# OMG, ahahah, @ddddd, #dijdij

	# ANOTAÇÃO 
	# lower string ...
	# remove stop words

	# excluir palavras q nao estao no dicionario ingles... ou seja, invalidas
	# ver se é um comentario relevante...
	# se só tiver uma palavra e for um nome ou pronome talvez n seja...

	# lemmatization -> converts the word into its root word




