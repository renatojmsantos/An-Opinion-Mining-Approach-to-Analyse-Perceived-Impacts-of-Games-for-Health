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

from emoji.unicode_codes import UNICODE_EMOJI

from textblob import TextBlob

import time

import emoji
import unicodedata



import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector
#from spacy_fastlang import LanguageDetector




#from abbr import expandall

DetectorFactory.seed = 0


#path = '../CSV/YT_10_03_2021_v6 - cópia 2.csv'
path = '../CSV/YT_10_03_2021_v6.csv'
#path = 'YT_repliesDif-Descript-ALL'
#path = '../CSV/YT_10_03_2021_v6.csv'
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
	#time.sleep(0.30)
	#lang = TextBlob(text)
	#print(lang.detect_language())
	#language = lang.detect_language()

	#print(detect(text))

	"""
	nlp = spacy.load('en_core_web_sm') #trf
	nlp.add_pipe(LanguageDetector())#,name='language_detector',last=True)
	doc = nlp(text)
	detect_language = doc._.language
	print(detect_language)
	"""

	"""
	# Add LanguageDetector and assign it a string name
	@Language.factory("language_detector")
	def create_language_detector(nlp, name):
	    return LanguageDetector(language_detection_function=None)

	# Use a blank Pipeline, also a model can be used, e.g. nlp = spacy.load("en_core_web_sm")
	nlp = spacy.load("en_core_web_trf")

	# Add sentencizer for longer text
	nlp.add_pipe('sentencizer')

	# Add components using their string names
	nlp.add_pipe("language_detector")

	# Analyze components and their attributes
	#text = "This is an English text."
	doc = nlp(text)


	# Document level language detection.
	print(doc._.language)

	# See what happened to the pipes
	#nlp.analyze_pipes(pretty=True)
	
	"""

	
	try:
		language = detect(text)
		print(text)
		print(language)
		if (language == "en"):
			return True
		else:
			return False
	except:
		print("ERRO lang_detect ...")
	
	return False
	

#listaPalavras = ["🤗","l","I’d like to know how I’d done that!","I'd like to play!", "abc","sex","stop","this game/ is! great!","this is great", "isto é bom","i love thiq gam ","u know","hi","a","aaa","big https://wwww.uc.pt THE BEST url: http://blah.com/path/to/here?p=1&q=abc,def#posn2 #ahashtag http://t.co/FNkPfmii-","@rui ola 🙀🤗🤗🤗🤗","best game #yolo :)","my best  friend from   germany !!!!!!!!!! lol ...... ","beautifulllll","OMG 🤯", "YOU 🤯🤯🤯🤯are goooood ", "issijjsij","laranja","orange","how","fix this"]
#listaPalavras = ["🙀","🤗","that's great", "90 years old", "it's ok! " "i'm renato", "u are good","renato", "benfica champions", "luv omg bff 4ever", "bd eheheheheheni ijij","you are my bff", "yes omg ", "ly <3", "@rui ola 🙀🤗🤗🤗🤗","OMG 🤯", "LOL", "amazing thing 2 u", "YOU 🤯🤯🤯🤯are goooood "]
listaPalavras = ["🙀","🤗","that's great", "90 years old", "it's ok! " "my name is Renato", "u are good"]


def emojiToCLDRshortName(text):
	has_emoji = bool(emoji.get_emoji_regexp().search(text))
	#print(has_emoji)
	if (has_emoji):
	    emoji_chars = emoji.EMOJI_ALIAS_UNICODE.values()
	    def _emoji(char):
	        if char in emoji_chars:
	            return unicodedata.name(char) + " "
	    #for char in text:
	    #	print(_emoji(char))
	    return ''.join(_emoji(char) or char for char in text)
	else:
		return text


def clearText(text):
	# remove emojis
	#text = demoji(text)
	#print("0 — " , text)

	#contracoes inglesas... that's -> that is
	text = contractions(text)
	# acronimos e expressoes da giria popular
	text = slangs(text)
	#print("0 — " , text)
	# emojis to string
	text = str(emojiToCLDRshortName(text))
	#print("#",text)
	# remove URLs
	text = re.sub('https?://[A-Za-z0-9./?&=_]+','',text)

	#text = slangs(text)

	# hashtags
	text = re.sub('#[A-Za-z0-9]+','',text)
	# mencoes
	text = re.sub('@[A-Za-z0-9._-]+','',text)
	# to lower
	text = text.lower()

	#print("0 — " , text)
	#https://pypi.org/project/pycontractions/
	# expand abreviaturas ...
	# remover pontuacao
	text = re.sub(r"[^\w\s]","",text)
	#remover espacos
	text = " ".join(text.strip().split())
	text = re.sub(r"[\W\s]"," ",text)
	text = re.sub("\n","",text)

	#print("0 — " , text)
	return text

def contractions(text):
	#https://gist.github.com/nealrs/96342d8231b75cf4bb82
	cDict = {
	  "ain't": "am not",
	  "aren't": "are not",
	  "can't": "cannot",
	  "can't've": "cannot have",
	  "'cause": "because",
	  "could've": "could have",
	  "couldn't": "could not",
	  "couldn't've": "could not have",
	  "didn't": "did not",
	  "doesn't": "does not",
	  "don't": "do not",
	  "hadn't": "had not",
	  "hadn't've": "had not have",
	  "hasn't": "has not",
	  "haven't": "have not",
	  "he'd": "he would",
	  "he'd've": "he would have",
	  "he'll": "he will",
	  "he'll've": "he will have",
	  "he's": "he is",
	  "how'd": "how did",
	  "how'd'y": "how do you",
	  "how'll": "how will",
	  "how's": "how is",
	  "I'd": "I would",
	  "I'd've": "I would have",
	  "I'll": "I will",
	  "I'll've": "I will have",
	  "I'm": "I am",
	  "I've": "I have",
	  "isn't": "is not",
	  "it'd": "it had",
	  "it'd've": "it would have",
	  "it'll": "it will",
	  "it'll've": "it will have",
	  "it's": "it is",
	  "let's": "let us",
	  "ma'am": "madam",
	  "mayn't": "may not",
	  "might've": "might have",
	  "mightn't": "might not",
	  "mightn't've": "might not have",
	  "must've": "must have",
	  "mustn't": "must not",
	  "mustn't've": "must not have",
	  "needn't": "need not",
	  "needn't've": "need not have",
	  "o'clock": "of the clock",
	  "oughtn't": "ought not",
	  "oughtn't've": "ought not have",
	  "shan't": "shall not",
	  "sha'n't": "shall not",
	  "shan't've": "shall not have",
	  "she'd": "she would",
	  "she'd've": "she would have",
	  "she'll": "she will",
	  "she'll've": "she will have",
	  "she's": "she is",
	  "should've": "should have",
	  "shouldn't": "should not",
	  "shouldn't've": "should not have",
	  "so've": "so have",
	  "so's": "so is",
	  "that'd": "that would",
	  "that'd've": "that would have",
	  "that's": "that is",
	  "there'd": "there had",
	  "there'd've": "there would have",
	  "there's": "there is",
	  "they'd": "they would",
	  "they'd've": "they would have",
	  "they'll": "they will",
	  "they'll've": "they will have",
	  "they're": "they are",
	  "they've": "they have",
	  "to've": "to have",
	  "wasn't": "was not",
	  "we'd": "we had",
	  "we'd've": "we would have",
	  "we'll": "we will",
	  "we'll've": "we will have",
	  "we're": "we are",
	  "we've": "we have",
	  "weren't": "were not",
	  "what'll": "what will",
	  "what'll've": "what will have",
	  "what're": "what are",
	  "what's": "what is",
	  "what've": "what have",
	  "when's": "when is",
	  "when've": "when have",
	  "where'd": "where did",
	  "where's": "where is",
	  "where've": "where have",
	  "who'll": "who will",
	  "who'll've": "who will have",
	  "who's": "who is",
	  "who've": "who have",
	  "why's": "why is",
	  "why've": "why have",
	  "will've": "will have",
	  "won't": "will not",
	  "won't've": "will not have",
	  "would've": "would have",
	  "wouldn't": "would not",
	  "wouldn't've": "would not have",
	  "y'all": "you all",
	  "y'alls": "you alls",
	  "y'all'd": "you all would",
	  "y'all'd've": "you all would have",
	  "y'all're": "you all are",
	  "y'all've": "you all have",
	  "you'd": "you had",
	  "you'd've": "you would have",
	  "you'll": "you you will",
	  "you'll've": "you you will have",
	  "you're": "you are",
	  "you've": "you have"
	}

	c_re = re.compile('(%s)' % '|'.join(cDict.keys()))

	def expandContractions(text, c_re=c_re):
	    def replace(match):
	        return cDict[match.group(0)]
	    return c_re.sub(replace, text)
	
	text = expandContractions(text)

	return text


def caracteresRepetidos(text):
	# é preciso ter em conta as palavras inglesas.... "good", "god", ... 
	# https://www.nltk.org/_modules/nltk/tokenize/casual.html#reduce_lengthening
	#print(len(text.split()))
	#print("**", text)
	if (len(text) > 1):
		pattern = regex.compile(r"(.)\1{2,}")
		#print("***", text)
		return pattern.sub(r"\1\1\1", text)
	else:
		return text


def spellCorrection(text):
	t = TextBlob(text).correct()

	# NER - Name Entity Reconection 
	# se for NER nao corrigir... person name, locations, organizations, other names...
	#print(t)
	return t


def slangs(text):
	#print("** ",text)
	#print(text.lower().strip().split())
	file = 'acronimos.csv'
	acron = pd.read_csv(file,lineterminator='\n',encoding='utf-8')

	slang = acron['slang']
	complete = acron['complete']
	row = 0

	"""
	for s in slang:
		#print(text.lower().strip().split())
		#print(text.lower().strip().split())
		#print(text.lower().strip())
		#print(text.lower())

		#slang[row] in text.lower().strip())
		s = text.lower().strip()
		if ( (s.find(slang[row])) != -1 ):
			print("TRUE")
			print(slang[row], text.lower().strip())
			#s = "'["+str(slang[row].strip())+"]'"
			#c = "'"+str(complete[row].strip())+"'"
			print("#",slang[row], str(complete[row].strip()))
			#print("##",row,s,c)
			text = text.replace(slang[row],str(complete[row].strip()))
			#text = re.sub(s, c, text)
			break
		else
			row+=1
	"""

	for s in slang:
		if(slang[row] in text.lower().strip().split()):
			#print("TRUE")
			#print(text)
			print("#",slang[row]+ "-->"+ str(complete[row].strip()))
			#print("##",row,s,c)
			text = text.lower()
			text = text.replace(slang[row],str(complete[row].strip()))
			#print("$",text)
			
			#text = re.sub(s, c, text)
			#break
		else:
			row+=1
	return text

	"""
	for t in text.strip().split():
		#print (t)
		if (slang[row] in t):
			print("TRUE")
			text = text.replace(slang[row],str(complete[row].strip()))
		else:
			row+=1
	"""
	#for s in slang:
	#	print(s)

	"""
	if(any (slang[row] in str(text.lower().strip()) for s in slang)):
		print(slang[row])
		print("true")

	else:
		row+=1
	"""
	#print("~",text)

	"""
	try:
	except IOError as e:
		print(e)
	except FileNotFoundError:
		print("File not found...", file)
	except Exception:
		print("Another Error...", file)
	"""
	return text

def runPreprocessing(t):
	#print("running clean ... ")
	#check csv slangs...
	t = clearText(t)
	#t = slangs(t)
	if(len(t) >= 3):
		#print("\n",t)
		#print(len(t))
		t = caracteresRepetidos(t)
		#print(t)
		t = spellCorrection(t) # rever
		#print(t)
		if (len(t) >= 3 and isEnglish(str(t))):
			return t
	return "None"
	


for t in listaPalavras: #t in comments:
	print("\n>>> ",t)
	t = runPreprocessing(t)
	print("> ",t)



"""
# contra tratados
contaFinal = 0
for t in comments:
	if(len(t) >= 3):
		#print("\n",t)
		t = clearText(t)
		#print(len(t))
		t = caracteresRepetidos(t)
		t = spellCorrection(t) # rever

		if (len(t) >= 3 and isEnglish(str(t))):
			contaFinal += 1
			print(contaFinal)

print(">>>>>>>>>>>>>>>", contaFinal)
"""


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




