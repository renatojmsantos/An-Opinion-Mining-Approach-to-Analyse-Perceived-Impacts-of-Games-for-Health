from connectDB import *

from vocabulary import *

#import pandas as pd

from nrclex import NRCLex
#from senticnet.senticnet import SenticNet
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import re 

from textblob import TextBlob, Word

def getEditionAndPlataform(game_id, title, descript):
	try:
		title = re.sub('&quot;+','',title)
		title = title.strip().lower() 

		# substituir JD por Just Dance .... no titulo do video ....
		title = re.sub('jd','just dance',title)
		title = re.sub('justdance','just dance',title)
		title = re.sub('ps4','PlayStation 4',title)
		title = re.sub('ps2','PlayStation 2',title)
		title = re.sub('ps3','PlayStation 3',title)
		title = re.sub('x360','PlayStation 4',title)
		title = re.sub('xbox sx','Xbox Series X',title)
		title = re.sub('xbox ss','Xbox Series S',title)
		title = re.sub('switch','Nintendo Switch',title)
		title = re.sub('nintendo','Nintendo Switch',title)
		title = re.sub('windows','Microsoft Windows',title)
		title = re.sub('pc','Microsoft Windows',title)

		titleWords = word_tokenize(title.strip()) # PROBLEM 2017, 2018?
		title = " ".join(titleWords)


		#descript = description[row]
		descriptWords = word_tokenize(descript.strip()) # PROBLEM 2017, 2018?
		descript = " ".join(descriptWords)

		descript = " ".join(descript.strip().split())
		descript = re.sub(r"[\W\s]"," ",descript)
		descript = re.sub("\n","",descript)

		descript = descript.lower()
		descript = re.sub('jd','just dance',descript)
		descript = re.sub('justdance','just dance',descript)
		descript = re.sub('ps4','PlayStation 4',descript)
		descript = re.sub('ps2','PlayStation 2',descript)
		descript = re.sub('ps3','PlayStation 3',descript)
		descript = re.sub('x360','PlayStation 4',descript)
		descript = re.sub('xbox sx','Xbox Series X',descript)
		descript = re.sub('xbox ss','Xbox Series S',descript)
		descript = re.sub('switch','Nintendo Switch',descript)
		descript = re.sub('nintendo','Nintendo Switch',descript)
		descript = re.sub('windows','Microsoft Windows',descript)
		descript = re.sub('pc','Microsoft Windows',descript)


		platforms = ['Wii', 'Wii U', 'PlayStation 3', 'PlayStation 4', 'PlayStation 5', 'Xbox 360', 'Xbox One', 'Xbox Series X', 'Xbox Series S','iOS', 'Android', 'Nintendo Switch', 'Microsoft Windows', 'Stadia']
		# detetar plataforma no titulo do video e na descrição ...

		# pode ser mais do que uma .... VERIFICAR e guardar em LISTA !
		platform = ""
		for p in platforms:
			c = p.lower()
			if(c in title.lower()):
				platform = p
				break
			elif(c in descript.strip().lower()):
				platform = p
				break
		if(platform==""):
			platform="Unknown"

		#print(title)
		#https://en.wikipedia.org/wiki/Just_Dance_(video_game_series)
		games = ['Just Dance 2', 'Just Dance 3', 'Just Dance 4', 'Just Dance 2014', 'Just Dance 2015', 'Just Dance 2016', 'Just Dance 2017', 'Just Dance 2018', 'Just Dance 2019', 'Just Dance 2020', 'Just Dance 2021',
				'Just Dance Wii', 'Just Dance Wii 2', 'Just Dance Wii U', 'Yo-kai Watch Dance: Just Dance Special Version',
				'Just Dance Kids', 'Just Dance Kids 2', 'Just Dance Kids 2014',
				'Just Dance: Disney Party', 'Just Dance: Disney Party 2',
				'Just Dance: Greatest Hits',
				'Just Dance: Summer Party', 'Just Dance Now', 'Just Dance Unlimited']
		# Just Dance é o ultimo jogo a ser inserido... RISCO neste!!! pode nao ser o 1.º JD.... pq no titulo podem nao especificar qual é a versao
		# quem nao quiser saber de qual é a edicao, simplesmente nao aplica o filtro, e vê tudo.
		
		# detetar o nome do jogo no titulo do video ...
		edition=""
		serie=""
		
		"""
		checklist = ['A', 'FOO']
		words = ['fAr', 'near', 'A']
		matches = set(checklist).intersection(set(words))
		print(matches)  # {'A'}
		"""
		#titleWords
		#print(games)
		#print(titleWords)
		#matches = set(games).intersection(set(titleWords))
		#print(matches)

#----

		#matches = [c for c in checklist if c in words]

		#matches = []
		#for c in checklist:
		#  if c in words:
		#    matches.append(c)
#---
		editions=[]
		for game in games:
			serie = game.lower()
			#print(serie)
			if(serie in titleWords): #dont work, # PROBLEM 2018, 2019 ???
				editions.appends(game)
			elif(serie in descript.lower()):
				edition=game
				break
			else:
				serie=""
		if(serie ==""): 
			serie = "Just Dance"
			if(serie.lower() in title.lower()):
				edition = "Just Dance"

		print(editions)

#---
		for game in games:
			serie = game.lower()
			#print(serie)
			if(serie in title.lower()): #dont work, # PROBLEM 2018, 2019 ???
				edition=game
				break
			elif(serie in descript.lower()):
				edition=game
				break
			else:
				serie=""
		if(serie ==""): 
			serie = "Just Dance"
			if(serie.lower() in title.lower()):
				edition = "Just Dance"

		game_id +=1 
		
		print(edition, platform)
		#query = "insert into game values('"+str(game_id)+"', '"+str(edition)+"', '"+str(platform)+"')"
		#insertToTable(query)

		return game_id
	except Exception as e:
		print("get game and console ->", e)



getEditionAndPlataform(1, "Just Dance 2015", "something on ps5 or wii")



