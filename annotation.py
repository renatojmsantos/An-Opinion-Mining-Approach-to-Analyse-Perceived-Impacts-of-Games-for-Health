
from preprocessing import *
from connectDB import *

from vocabulary import *

import pandas as pd

from nrclex import NRCLex
#from senticnet.senticnet import SenticNet
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet


#from vocabulary import *

#tagger = SequenceTagger.load("flair/ner-english-large") # EXPLODE ....
#tagger = SequenceTagger.load("ner") # ESTE !!


#nltk.download('averaged_perceptron_tagger')
#tagger = SequenceTagger.load("flair/ner-english-large")

def insertToTable(query):
	idBack = None
	conn = None
	
	try:
		params = config()
		conn = psycopg2.connect(**params)
		conn.autocommit = True
		cur = conn.cursor()

		#cur.execute('SELECT version()')
		#db_version = cur.fetchone()
		#print(db_version)

		#print("tables")
		#query="SELECT * FROM opinion"
		#cur.execute(query)
		#print(cur.fetchone())

		#cur.execute("select * from usability")
		#print(cur.fetchone())
		query = query + " returning 1;" # duplicados deste id = 1 ????
		#print(query)
		#print(tableName)
		#cur.execute(query, (tableName,))
		cur.execute(query)
		idBack = cur.fetchone()
		#print(idBack)
		conn.commit()
		#print("inserted!")
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack


#insertTablesConceitos()

def annotate(text, polarity):
	#print("\n>>>>>>> ",text)
	#print(">>> ", polarity)

	# remove stop words

	# emolex 
	t = NRCLex(str(text))
	#print(t)
	#print(t.affect_list)
	emotions = t.affect_list
	#print(t.affect_dict)
	#print(t.raw_emotion_scores)
	#print(t.top_emotions)
	#print(t.affect_frequencies)


	# POS Tagger
	def pos_tagger(nltk_tag):
		if nltk_tag.startswith('J'):
			return wordnet.ADJ
		elif nltk_tag.startswith('V'):
			return wordnet.VERB
		elif nltk_tag.startswith('N'):
			return wordnet.NOUN
		elif nltk_tag.startswith('R'):
			return wordnet.ADV
		else:          
			return None

	# POS Tagger adjetivos
	def pos_taggerJJ(nltk_tag):
		if nltk_tag.startswith('J'):
			return wordnet.ADJ
		else:          
			return None

	textWords = word_tokenize(text)
	pos_tagged = nltk.pos_tag(textWords)
	#print(pos_tagged)

	wordnet_tagged = list(map(lambda x: (x[0], pos_taggerJJ(x[1])), pos_tagged))
	#print(wordnet_tagged)

	#lemmas
	lemmatizer = WordNetLemmatizer()
	lemmas = []
	for word, tag in wordnet_tagged:
		if (tag is not None):
			lemmas.append(lemmatizer.lemmatize(word, tag))

	text_lemmas = " ".join(lemmas)


	#print(text_lemmas)

	"""
	words = word_tokenize(text_lemmas)
	print(words)
	# remove stop words
	stopwords = nltk.corpus.stopwords.words('english')
	keywords = [word for word in words if not word in text_lemmas]
	print(keywords)
	"""


	dictAnotado = {}
	for items in dict.items():
		chave = items[0]
		conceitos = items[1]
		#print("\n",chave,conceitos)
		#print("\n>> ",chave)
		for vocabulario in conceitos.items():
			termo = vocabulario[0]
			pals = vocabulario[1]
			#print(termo,pals)
			#print(" #", termo)
			#print("---------->",len(pals), pals)
			for p in pals.items():
				#print(len(p),p)
				# se fosse lista nas pals associadas...
				# print p   .... in pals
				pal = p[0]
				#probalidade = p[1]
				if (pal in text):
					if chave not in dictAnotado.keys():
						dictAnotado[chave] = [termo]
					elif termo not in dictAnotado[chave]:
						dictAnotado[chave].append(str(termo))
					#print(dictAnotado)
				if (emotions):
					#estrategia ...
					#print("TRUE")
					#print(emotions)
					for e in emotions:
						if (e in pal):
							#print(e, termo)
							if chave not in dictAnotado.keys():
								dictAnotado[chave] = [termo]
							elif termo not in dictAnotado[chave]:
								dictAnotado[chave].append(str(termo))
					#continue
				#print(pal)

				# processo de lematização
				pos_tagged = nltk.pos_tag([pal])
				#print(pos_tagged)
				wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))
				#print(wordnet_tagged)
				#keyword = []
				for word, tag in wordnet_tagged:
					if (tag is not None):
						keyword = lemmatizer.lemmatize(word, tag)
						#keyword.append(lemmatizer.lemmatize(word, tag))
				#print(keyword)
				#if(pal!=keyword):
				#	print(pal, keyword)

				# só com a lematização encontra-se logo o termo...
				if (keyword in text):
					if chave not in dictAnotado.keys():
						dictAnotado[chave] = [termo]
					elif termo not in dictAnotado[chave]:
						dictAnotado[chave].append(str(termo))

				# check if keyword está nos lemmas do comentario
				if (keyword in text_lemmas):
					if chave not in dictAnotado.keys():
						dictAnotado[chave] = [termo]
					elif termo not in dictAnotado[chave]:
						dictAnotado[chave].append(str(termo))

				# sinonimos, hiponimos, meronimos -> wordnet 
				listAnalysis=[]
				for lemma in word_tokenize(text_lemmas):
					#print("->",lemma)
					# palavras que significam o mesmo
					#sinonimos = wordnet.synsets(lemma)
					#print(sinonimos)
					for syn in wordnet.synsets(lemma):
						#print(syn.name(), syn.lemma_names())
						for l in syn.lemmas():
							#print(l.name())
							#print(l)
							if (l.name() not in listAnalysis):
								listAnalysis.append(l.name())

						#lexical relations
						lexical = wordnet.synset(syn.name())

						# conceito especifico
						for s in lexical.hyponyms():
							for l in s.lemmas():
								#print(l.name())
								if (l.name() not in listAnalysis):
									listAnalysis.append(l.name())

						# conceitos mais gerais
						for s in lexical.hypernyms():
							for l in s.lemmas():
								#print(l.name())
								if (l.name() not in listAnalysis):
									listAnalysis.append(l.name())

						# membro de alguma coisa
						"""
						for s in lexical.part_holonyms():
							for l in s.lemmas():
								#print(l.name())
								if (l.name() not in listAnalysis):
									listAnalysis.append(l.name())
						"""
						# parte de algo
						for s in lexical.part_meronyms():
							for l in s.lemmas():
								#print(l.name())
								if (l.name() not in listAnalysis):
									listAnalysis.append(l.name())

						# entailments -> implicacoes, como estao ligados.. verbos
						"""
						for s in lexical.entailments():
							for l in s.lemmas():
								#print(l.name())
								if (l.name() not in listAnalysis):
									listAnalysis.append(l.name())
						"""

				#print(listAnalysis)
				if(keyword in listAnalysis):
					if chave not in dictAnotado.keys():
						#print(keyword, termo)
						dictAnotado[chave] = [termo]
					elif termo not in dictAnotado[chave]:
						#print(keyword, termo)
						dictAnotado[chave].append(str(termo))

				# CHECK SIMILARITY ENTRE AS PALAVRAS DA LISTA E AS KEYWORDS? ...............


	return dictAnotado


#teste = ["this give me nostalgia","this game is awesome", "can you fix the servers?", "i burned a lot of calories playing this", 'if you like multiplayer strategy games, buy this with confidence',
#			'those expectations were met. Mostly, anyway', 'making the game enjoyable for beginners as well as veterans.','Multiplayer is excellent, but the single player campaign isn’t.',
#			'Most of the inter-mission story telling happen in this mode, which tend to be awkward and clumsy.',
#			'Most of the missions are enjoyable, and each one has optional goals which add replay value.']

def checkDimensionID(field,concept):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT dimension_id FROM dimension WHERE field = '"+field+"' and concept = '"+ concept +"'"
		#print(query)
		cur.execute(query)

		idBack = cur.fetchall()
		for row in idBack:
			if (row is not None):
				#print(row)
				idBack=row
				#return idBack 
		#print(idBack)
		#conn.commit()
		#print("inserted!")
		
		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

def checkGameID(edition,platform):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT game_id FROM game WHERE edition = '"+edition+"' and platform = '"+platform+"'"

		#print(query)
		cur.execute(query)

		#idBack = cur.fetchone()
		idBack = cur.fetchall()
		#while idBack is not None:
		#	print(idBack)
		#	return idBack 
		for row in idBack:
			if (row is not None):
				#print(row)
				idBack=row
				#return idBack 
		#print(idBack)
		#conn.commit()
		#print("inserted!")
		
		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

def executeAnnotation():
	row = 0
	opinion_id=0
	dimension_id=0
	game_id=0
	for t in comments: #t in comments: , teste
		try:
			t = runPreprocessing(t)
			if (t != "None"):
				# print texto tratado e valido
				#print(">>>>>",t) 
				#sentiment analysis
				try:
					title = videoTitle[row]
					
					#title = demoji(title)
					title = re.sub('&quot;+','',title)
					title = title.strip().lower()

					
					#title = " ".join(title.strip().split())
					#title = re.sub(r"[\W\s]"," ",title)
					#title = re.sub("\n","",title)


					#print(title)
					if("ps22 chorus" not in title):
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

						titleWords = word_tokenize(title.strip())
						title = " ".join(titleWords)

						text = TextBlob(str(t))
						#print(text.sentiment)
						#print(text.sentiment.polarity, text.sentiment.subjectivity)

						#sentiment analysis
						if text.sentiment.polarity < 0:
							polarity="Negative"
						elif(text.sentiment.polarity > 0):
							polarity="Positive"
						else:
							polarity="Neutral"
						try:
							dateComment = timestampComment[row]
							dateVideo = videoPublishedAt[row]
							dateComment = re.sub('T[0-9:Z]+','',dateComment)
							dateVideo = re.sub('T[0-9:Z]+','',dateVideo)
						except Exception as e:
							print(e)
							#print("something wrong on convert dates...")

						isMain = mainComment[row] # TRUE -> comentario principal

						descript = description[row]
						descriptWords = word_tokenize(descript.strip())
						descript = " ".join(descriptWords)

						descript = " ".join(descript.strip().split())
						descript = re.sub(r"[\W\s]"," ",descript)
						descript = re.sub("\n","",descript)

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

						platforms = ['Wii', 'Wii U', 'PlayStation 3', 'PlayStation 4', 'PlayStation 5', 'Xbox 360', 'Xbox One', 'Xbox Series X', 'Xbox Series S','iOS', 'Android', 'Nintendo Switch', 'Microsoft Windows', 'Stadia']
						# tratar abreviaturas das consolas... ps3 -> playstation 3 ou no if... meter as duas hipoteses...

						if (isMain):
							isMain = "Main"
						else:
							isMain = "Reply"
						#insert youtube video ...
						query = "insert into video values('"+str(channelID[row])+"', '"+channel[row]+"', '"+str(videoID[row])+"','"+title+"','"+str(dateVideo)+"', '"+str(views[row])+"', '"+str(likesVideo[row])+"', '"+str(dislikesVideo[row])+"', '"+str(totalCommentsVideo[row])+"', '"+descript+"')"
						insertToTable(query)
						query = "insert into comment values('"+str(commentID[row])+"', '"+str(t)+"', '"+str(polarity)+"', '"+str(likes[row])+"', '"+str(dateComment)+"', '"+str(isMain)+"')"
						insertToTable(query)

						# detetar plataforma no titulo do video e na descrição ...
						#for p in plataform:
							#print(p)
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

						#print(console)
						# detetar o nome do jogo no titulo do video ...
						edition=""
						serie=""
						
						for game in games:
							serie = game.lower()
							if(serie in title.lower()):
								#print("\n1...Video ID = "+str(videoID[row])+'\nConsole = '+ console + "\nGame = "+ game + "\nTitle = " +title)
								# select where edition  = ... and console = .... ---> get ID
								#query = "insert into opinion values('"+str(commentID[row])+"', '"+str(t)+"', '"+str(polarity)+"', '"+str(likes[row])+"', '"+str(dateComment)+"', '"+str(isMain)+"', '"+str(dimension_id)+"', '"+str(game_id)+"', '"+str(videoID[row])+"')"
								#insertToTable(query)
								edition=game
								break
							elif(serie in descript.lower().lower()):
								#print("\n2...Video ID = "+str(videoID[row])+'\nConsole = '+ console + "\nGame = "+ game + "\nTitle = " +title)
								# select where edition  = ... and console = .... ---> get ID
								#query = "insert into opinion values('"+str(commentID[row])+"', '"+str(t)+"', '"+str(likes[row])+"', '"+str(dateComment)+"', '"+str(isMain)+"', '"+str(game)+"', '"+str(console)+"', '"+str(polarity)+"', '"+str(videoID[row])+"')"
								#query = "insert into opinion values('"+str(commentID[row])+"', '"+str(t)+"', '"+str(polarity)+"', '"+str(likes[row])+"', '"+str(dateComment)+"', '"+str(isMain)+"', '"+str(dimension_id)+"', '"+str(game_id)+"', '"+str(videoID[row])+"')"
								#insertToTable(query)
								edition=game
								break
							else:
								serie=""
						if(serie ==""):
							serie = "Just Dance"
							if(serie.lower() in title.lower()):
								#print("\n3...Video ID = "+str(videoID[row])+'\nConsole = '+ console + "\nGame = "+ edition + "\nTitle = " +title)
								edition = "Just Dance"
								# select where edition  = ... and console = .... ---> get ID
								#query = "insert into opinion values('"+str(commentID[row])+"', '"+str(t)+"', '"+str(likes[row])+"', '"+str(dateComment)+"', '"+str(isMain)+"', '"+str(edition)+"', '"+str(console)+"', '"+str(polarity)+"', '"+str(videoID[row])+"')"
								#query = "insert into opinion values('"+str(commentID[row])+"', '"+str(t)+"', '"+str(polarity)+"', '"+str(likes[row])+"', '"+str(dateComment)+"', '"+str(isMain)+"', '"+str(dimension_id)+"', '"+str(game_id)+"', '"+str(videoID[row])+"')"
								#insertToTable(query)

						#game_id = checkGameID(edition, platform)
						#game_id = str(game_id)
						#game_id = game_id.replace(',','')
						#game_id = game_id.replace('(','')
						#game_id = game_id.replace(')','')
						#game_id = game_id.replace('[','')
						#game_id = game_id.replace(']','')
						game_id +=1 
						query = "insert into game values('"+str(game_id)+"', '"+str(edition)+"', '"+str(platform)+"')"
						insertToTable(query)

						DictResult = annotate(str(t),str(polarity)) 
						#print("> ",DictResult)
						if(bool(DictResult)):
							#print("		######################################## true")
							#print("> ",result[0])
							#print(">>",result[1])
							#print(DictResult)
							for field in DictResult.keys():
								#print("FIELD = ", field)
								for concept in DictResult[field]:
									opinion_id+=1
									dimension_id+=1
									#print(field + "->"+concept)
									#print(concept)
									if (field == "Usability"):
										# select where field = ... and concept = ... get dimension_id
										#query = "insert into opinion_usability values('"+str(commentID[row])+"', '"+str(concept)+"')"
										#dimension_id = checkDimensionID(field,concept)
										#dimension_id = str(dimension_id)
										#print(dimension_id)
										#dimension_id = dimension_id.replace(',','')
										#dimension_id = dimension_id.replace('(','')
										#dimension_id = dimension_id.replace(')','')
										#dimension_id = dimension_id.replace('[','')
										#dimension_id = dimension_id.replace(']','')
										#query = "insert into opinion values('"+str(opinion_id)+"', '"+str(commentID[row])+"', '"+str(t)+"', '"+str(polarity)+"', '"+str(likes[row])+"', '"+str(dateComment)+"', '"+str(isMain)+"', '"+str(dimension_id)+"', '"+str(game_id)+"', '"+str(videoID[row])+"')"
										
										query = "insert into dimension values('"+str(dimension_id)+"', '"+str(field)+"', '"+str(concept)+"')"
										insertToTable(query)

										query = "insert into opinion values('"+str(opinion_id)+"', '"+str(commentID[row])+"', '"+str(dimension_id)+"', '"+str(game_id)+"', '"+str(videoID[row])+"')"
										
										#query = "insert into dimension values('"+str(dimension_id)+"', '"+str(field)+"', '"+str(concept)+"')"
										#print(query)
										insertToTable(query)
									elif (field == "UX"):
										"""
										dimension_id = checkDimensionID(field,concept)
										dimension_id = str(dimension_id)
										#print(dimension_id)
										dimension_id = dimension_id.replace(',','')
										dimension_id = dimension_id.replace('(','')
										dimension_id = dimension_id.replace(')','')
										dimension_id = dimension_id.replace('[','')
										dimension_id = dimension_id.replace(']','')
										"""

										query = "insert into dimension values('"+str(dimension_id)+"', '"+str(field)+"', '"+str(concept)+"')"
										insertToTable(query)

										query = "insert into opinion values('"+str(opinion_id)+"', '"+str(commentID[row])+"', '"+str(dimension_id)+"', '"+str(game_id)+"', '"+str(videoID[row])+"')"
										#query = "insert into opinion_ux values('"+str(commentID[row])+"', '"+str(concept)+"')"
										#query = "insert into dimension values('"+str(dimension_id)+"', '"+str(field)+"', '"+str(concept)+"')"
										#print(query)
										insertToTable(query)
									elif (field == "Health"):
										"""
										dimension_id = checkDimensionID(field,concept)
										dimension_id = str(dimension_id)
										#print(dimension_id)
										dimension_id = dimension_id.replace(',','')
										dimension_id = dimension_id.replace('(','')
										dimension_id = dimension_id.replace(')','')
										dimension_id = dimension_id.replace('[','')
										dimension_id = dimension_id.replace(']','')
										"""
										
										query = "insert into dimension values('"+str(dimension_id)+"', '"+str(field)+"', '"+str(concept)+"')"
										insertToTable(query)

										query = "insert into opinion values('"+str(opinion_id)+"', '"+str(commentID[row])+"', '"+str(dimension_id)+"', '"+str(game_id)+"', '"+str(videoID[row])+"')"
										#query = "insert into opinion_health values('"+str(commentID[row])+"', '"+str(concept)+"')"
										#query = "insert into dimension values('"+str(dimension_id)+"', '"+str(field)+"', '"+str(concept)+"')"
										#print(query)
										insertToTable(query)
						
				except Exception as e:
					print(e)
					#print("something wrong.... annotate")
			row += 1
		except Exception as e:
			print(e)
		#row += 1

#insertTablesConceitos()
executeAnnotation()

#connect()
"""
print("tables")
query="SELECT * FROM opinion"
t = pd.read_sql_query(query,conn)
print(t)
"""
#closeConnection()










