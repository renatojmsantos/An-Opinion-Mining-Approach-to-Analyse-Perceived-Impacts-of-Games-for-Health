
#from preprocessing import *
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

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from flair.data import Sentence
from flair.models import SequenceTagger


tagger = SequenceTagger.load("hunflair-disease")



def insertToTable(query):
	idBack = None
	conn = None
	
	try:
		params = config()
		conn = psycopg2.connect(**params)
		conn.autocommit = True
		cur = conn.cursor()

		
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

def getDiseases(comment):
	sentence = Sentence(comment)
	tagger.predict(sentence)

	diseases = []
	for disease in sentence.get_spans():
		diseases.append(disease)

	if(len(diseases)>1):
		return True
	else:
		return False
	#return diseases

def updateGame(gameid, edition, platform):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		conn.autocommit = True
		cur = conn.cursor()

		#query = "SELECT field, concept FROM dimension where dimension_id='"+dimensionid+"'"
		query = "UPDATE game SET edition = '"+edition+"', platform = '"+platform+"' where game_id = '"+gameid+"' returning *;"
		#print(query)
		cur.execute(query)
		idBack = cur.fetchall()

		conn.commit()
		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO upd!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

def annotate(text, polarity):
	#print("\n>>>>>>> ",text)
	#print(">>> ", polarity)

	sno = nltk.stem.SnowballStemmer('english') 

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


	textWords = word_tokenize(text)
	pos_tagged = nltk.pos_tag(textWords)
	#print(pos_tagged)

	wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))
	#print(wordnet_tagged)

	#lemmas
	lemmatizer = WordNetLemmatizer()
	lemmas = []
	for word, tag in wordnet_tagged:
		if (tag is not None):
			lemmas.append(lemmatizer.lemmatize(word, tag))

	text_lemmas = " ".join(lemmas)

	# remove stop words
	words = word_tokenize(text_lemmas)
	stopwords = nltk.corpus.stopwords.words('english')
	pals_lemmas = [word for word in words if not word in stopwords]

	if (getDiseases(text)):
		pals_lemmas.append("disease")

	#print(pals_lemmas)

	text_lemmas = " ".join(pals_lemmas)
	#print(text_lemmas)

	score = 0.00
	scoreDict = {}

	#print("\n>>>>>>> ",text_lemmas)
	#print(">>> ", polarity)
	total_pals = len(word_tokenize(text_lemmas))

	t = NRCLex(str(text_lemmas))
	#print(t)
	#print(t.affect_list)
	#print(t.affect_dict)
	#print(t.raw_emotion_scores)
	#print(t.top_emotions)
	emotions = t.affect_frequencies
	# valid > 0.18
	print(emotions)
	emo = {}
	if(emotions):
		for c,v in emotions.items():
			if (v>0.18):
				#print(c,v)
				polarity = polarity.lower()
				"""
				if (c == "positive" and c != polarity):
					#print("erro positive")
					continue
				elif(c == "negative" and c != polarity):
					#print("erro negative")
					continue
				elif(polarity == "positive" and c == "anger" and c == "disgust" and c == "fear" and c == "sadness"):
					continue
				elif(polarity == "negative" and c == "joy"):
					continue
				"""
				if (c not in emo.keys()):
					emo[c] = v
					
	#print(emo)
	#words = word_tokenize(text_lemmas)
	#pals_stems = [sno.stem(word) for word in words]

	# stem = sno.stem(word)

	#print(pals_stems)
	#pals_stems = " ".join(pals_stems)
	#print(pals_stems)
	#print(pals_lemmas)
	
	lexs = []
	for d in dictVocabulary.items():
		#print(voc)
		concept = d[0]
		pals = d[1]
		#print(len(pals))
		#total_pals_dict = len(pals)
		countPalsDict = 0
		score=0.00
		#print("====================="+concept+"=====================")
		#conta = 0
		for pal, prob in pals.items():
			if (emo):
				#emolex
				for c,v in emo.items():	
					#score=0.00
					if (c in pal):
						#print("----> emolex")
						countPalsDict += 0.35 #1
						score = (v*prob)*1.8 #2
						print("# EMO ",concept, score)
						if concept not in scoreDict.keys():
							scoreDict[concept] = score
						else:
							# NR TOTAL DE VEZES QUE APARECE A DIVIDIR PELO NR TOTAL DE VEZES DE pals DETETADOS
							# 5 PALS DETETADAS.... 2 JOY / 5 = ...
							#score = score/conta
							#print(pal, conta, v, prob, score)
							scoreDict[concept] += score
			else:
				continue

			#print(score)
			# check dict
			#score=0.00
			stems=[]

			for lemma in pals_lemmas:

				word_stem = sno.stem(lemma)

				#score...  ?
				#print("#######################"+lemma)
				if (lemma == pal): 
					# total_pals_dict
					#print("--> MATCH ", lemma)
					countPalsDict += 0.65 #1

					#score = (prob/total_pals)*1.6
					score = prob*1.4
					#print(score,countPalsDict,lemma,pal)

					#score = score/total_pals_dict
					#print(concept,pal, score)
					#print(score)
					print(" match * 1.0 ", lemma, score, concept)
					if concept not in scoreDict.keys():
						scoreDict[concept] = score
					else:
						scoreDict[concept] += score
				elif (lemma in pal and len(lemma) >=3):
					try:
						palwn = wordnet.synsets(str(pal))[0]
						lemmawn = wordnet.synsets(str(lemma))[0]

						similarity = lemmawn.path_similarity(palwn)
						if(similarity > 0.45):
							countPalsDict += 1
							score = prob*1.0
							print("in * 1.0 ", lemma,score, concept)
							if concept not in scoreDict.keys():
								scoreDict[concept] = score
							else:
								scoreDict[concept] += score
					except Exception as e:
						#print(e)
						continue
				elif (word_stem in pal and len(word_stem)>1):
					stems.append(word_stem)
					try:
						palwn = wordnet.synsets(str(pal))[0]
						stemwn = wordnet.synsets(str(word_stem))[0]

						similarity = stemwn.path_similarity(palwn)
						if(similarity > 0.45):
							countPalsDict += 1
							score = prob*0.95
							print("stem * 0.95 ", word_stem,score,concept)
							if concept not in scoreDict.keys():
								scoreDict[concept] = score
							else:
								scoreDict[concept] += score
					except Exception as e:
						#print(e)
						continue
				else: 
					for syn in wordnet.synsets(lemma):
						#print(syn.name(), syn.lemma_names())
						for l in syn.lemmas():
							#print(l.name())
							antonym=""
							synonym=""
							if (l.antonyms()):
								#print("###### "+l.antonyms()[0].name())
								# condicoes...
								if (concept == "Negative feelings" or concept == "Frustration" or concept == "Positive feelings" or concept == "Pain and discomfort" 
									or concept == "Fatigue" or concept == "Pleasure" or concept == "Enjoyment and Fun"):
									continue
									#break
								else:
									antonym = l.antonyms()[0].name()
									stem = sno.stem(antonym)
							else:
								#print("---> "+l.name())
								synonym = l.name()
								stem = sno.stem(synonym)
							#print(stem)
							if (stem not in stems):

								stems.append(stem)
								#print(stem)
								# calculate score
								#print(stem, pal)
								if (synonym != "" and synonym == pal):
									#print("--> MATCH synonym ")
									countPalsDict += 1

									#score = (prob/total_pals)*1.0
									score = prob*0.8
									#print(score, countPalsDict, synonym,pal)

									#score = score/total_pals_dict
									#print(concept,pal, score)
									#print(score)
									print("synonym * 0.8", lemma, synonym, score, concept)
									if concept not in scoreDict.keys():
										scoreDict[concept] = score
									else:
										scoreDict[concept] += score
								elif (antonym != "" and antonym == pal):
									#print("--> MATCH antonym")
									countPalsDict += 1

									#score = (prob/total_pals)*1.0
									score = prob*0.75
									#print(score, countPalsDict, antonym,pal)

									#score = score/total_pals_dict
									#print(concept,pal, score)
									#print(score)
									print("antonym * 0.75", lemma, antonym, score, concept)
									if concept not in scoreDict.keys():
										scoreDict[concept] = score
									else:
										scoreDict[concept] += score
								elif (stem in pal and len(stem)>=3):
									# similarity
									# Recall that each synset has one or more parents (hypernyms). If two of them are linked to the same root they might have several hypernyms in common — that fact might mean that they are closely related.
									
									# WordNet also introduces a specific metric for quantifying the similarity of two words by measuring shortest path between them. It outputs:
										# range (0,1) → 0 if not similar at all, 1 if perfectly similar
										# -1 → if there is no common hypernym
									
									#lowest_common_hypernyms()
									# WORD1.path_similarity(WORD2)
									
									# https://www.nltk.org/howto/wordnet.html

									#print(syn, l, syn.lemmas())
									try:
										palwn = wordnet.synsets(str(pal))[0]
										stemwn = wordnet.synsets(str(stem))[0]
										#print(stemwn.name() + " "+ palwn.name())

										similarity = stemwn.path_similarity(palwn)
										
										if(similarity > 0.45):
											#print("--> syns")
											#print("similarity = ",similarity)
											countPalsDict += 1

											#score = (prob/total_pals)*1.0
											score = prob*0.7
											print("stem syn / ant * 0.7", lemma, stem, score, concept)
											if concept not in scoreDict.keys():
												scoreDict[concept] = score
											else:
												scoreDict[concept] += score

									except Exception as e:
										#print(e)
										continue
									
							else:
								continue
								#break #???????????

						if (lemma not in lexs):
							lexs.append(lemma)
							#print("################### >"+lemma)
							#print("###"+syn.name())

							#lexical relations
							lexical = wordnet.synset(syn.name())
							#print(lexical)
							
							# conceito especifico
							for s in lexical.hyponyms():
								for l in s.lemmas():
									#print(l.name())
									hyponym = l.name()
									stem = sno.stem(hyponym)
									if (stem not in stems):
										stems.append(stem)
										#print(stem)
										# calculate score
										if (hyponym == pal):
											#print("--> MATCH hyponym")
											countPalsDict += 1

											#score = (prob/total_pals)*0.5
											score = prob * 0.6
											print("match hyponym * 0.6", lemma, hyponym, score, concept)
											if concept not in scoreDict.keys():
												scoreDict[concept] = score
											else:
												scoreDict[concept] += score
										elif (stem in pal and len(stem)>=3):

											try:										
												palwn = wordnet.synsets(str(pal))[0]
												stemwn = wordnet.synsets(str(stem))[0]
												#print(stemwn.name() + " "+ palwn.name())

												similarity = stemwn.path_similarity(palwn)
												
												if(similarity > 0.45):
													#print("--> hyponyms")
													#print("similarity = ",similarity)
													countPalsDict += 1

													#score = (prob/total_pals)*0.5
													print(" hyponym * 0.55",lemma, stem, score, concept)
													score = prob * 0.55
													#print(score, countPalsDict, stem,pal)

													#score = score/total_pals_dict
													#print(concept,pal, score)
													#print(score)
													if concept not in scoreDict.keys():
														scoreDict[concept] = score
													else:
														scoreDict[concept] += score

											except Exception as e:
												#print(e)
												continue
									else:
										continue
										#break #???
							
							
							#countPalsDict = 0
							# conceitos mais gerais
							for s in lexical.hypernyms():
								for l in s.lemmas():
									#print(l.name())
									hypernym = l.name()
									stem = sno.stem(hypernym)
									if (stem not in stems):
										stems.append(stem)
										#print(stem)
										# calculate score
										if (hypernym == pal):
											#print("----> MATCH hypernym")
											countPalsDict += 1
											#score = (prob/total_pals)*0.6
											print(" match hypernym * 0.55",lemma, hypernym, score, concept)
											score = prob * 0.55
											#print(score, countPalsDict,hypernym,pal)

											if concept not in scoreDict.keys():
												scoreDict[concept] = score
											else:
												scoreDict[concept] += score
										elif (stem in pal and len(stem)>=3):
											try:										
												palwn = wordnet.synsets(str(pal))[0]
												stemwn = wordnet.synsets(str(stem))[0]
												#print(stemwn.name() + " "+ palwn.name())

												similarity = stemwn.path_similarity(palwn)
												
												if(similarity > 0.45):
													#print("----> hypernyms")
													#print("similarity = ",similarity)
													countPalsDict += 1

													#score = (prob/total_pals)*0.5
													print(" hypernym * 0.55", lemma, stem, score, concept)
													score = prob * 0.5
													#print(score, countPalsDict, stem,pal)

													#score = score/total_pals_dict
													#print(concept,pal, score)
													#print(score)
													if concept not in scoreDict.keys():
														scoreDict[concept] = score
													else:
														scoreDict[concept] += score
											except Exception as e:
												#print(e)
												continue
									else:
										continue
										#break#???

							#countPalsDict = 0
							# parte de algo
							for s in lexical.part_meronyms():
								for l in s.lemmas():
									#print(l.name())
									meronym = l.name()
									stem = sno.stem(meronym)
									if (stem not in stems):
										stems.append(stem)
										#print(stem)
										# calculate score
										if (meronym == pal):
											#print("--------> MATCH meronyms")
											countPalsDict += 1
											#score = (prob/total_pals)*0.6
											score = prob * 0.5
											#print(score, countPalsDict,meronym,pal)
											print(" meronym * 0.55", lemma, meronym, score, concept)
											if concept not in scoreDict.keys():
												scoreDict[concept] = score
											else:
												scoreDict[concept] += score
										elif (stem in pal and len(stem)>=3):
											try:										
												palwn = wordnet.synsets(str(pal))[0]
												stemwn = wordnet.synsets(str(stem))[0]
												#print(stemwn.name() + " "+ palwn.name())

												similarity = stemwn.path_similarity(palwn)
												
												if(similarity > 0.45):
													
													countPalsDict += 1

													score = prob * 0.45
													print(" meronym * 0.55", lemma, stem, score, concept)
													if concept not in scoreDict.keys():
														scoreDict[concept] = score
													else:
														scoreDict[concept] += score
											except Exception as e:
												#print(e)
												continue

									else:
										continue
										#break #???
			
							
						else:
							continue
							#break #????
						
					
								
		# dividir pelo nr de pals detetadas do dicionario...
		# alguns conceitos Têm muitas e outras poucas...
		# o que beneficia quem tem muitas...
		#print(score)
		#countPalsDict = ...
		
		if concept in scoreDict.keys():
			#print(score, countPalsDict)
			#print(scoreDict[concept])
			scoreDict[concept] = scoreDict[concept]/countPalsDict #score/countPalsDict
			#print(scoreDict[concept])
	#print(scoreDict)
	return scoreDict




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

def getSentiment(t):

	try:
		analyzer = SentimentIntensityAnalyzer()
		vsOriginal = analyzer.polarity_scores(str(t))
		#vsProcessed = analyzer.polarity_scores(processedtext)
		#print("{:-<65} {}".format(originaltext, str(vsOriginal)))
		#print("\n>>>>>>> ", originaltext)
		#print("#",originalPolarity)
		#print(vsOriginal)
		#print(vsOriginal['compound'])

		if (vsOriginal['compound'] >= 0.05):
			polarity = "Positive"
		elif(vsOriginal['compound'] <= -0.05):
			polarity = "Negative"
		else:
			polarity = "Neutral"

		return polarity

	except Exception as e:
		print("sentiment — ",e)



def getEditionAndPlataform(game_id, title, descript):
	try:
		title = re.sub('&quot;+','',title)
		title = title.lower().strip()

		# substituir JD por Just Dance .... no titulo do video ....
		title = re.sub('jd','just dance',title)
		title = re.sub('justdance','just dance',title)
		title = re.sub('wiiu','wii u',title)
		#title = re.sub('ps2','PlayStation 2',title)
		title = re.sub('ps3','PlayStation 3',title)
		title = re.sub('ps4','PlayStation 4',title)
		title = re.sub('ps5','PlayStation 5',title)
		#title = re.sub('playstation2','PlayStation 2',title)
		title = re.sub('playstation3','PlayStation 3',title)
		title = re.sub('playstation4','PlayStation 4',title)
		title = re.sub('playstation5','PlayStation 5',title)
		title = re.sub('x360','Xbox 360',title)
		title = re.sub('xbox sx','Xbox Series X',title)
		title = re.sub('xbox ss','Xbox Series S',title)
		title = re.sub('xbox360','Xbox 360',title)
		title = re.sub('xboxone','Xbox One',title)
		title = re.sub('switch','Nintendo Switch',title)
		title = re.sub('nintendoswitch','Nintendo Switch',title)
		title = re.sub('nintendo','Nintendo Switch',title)
		title = re.sub('windows','Microsoft Windows',title)
		title = re.sub('pc','Microsoft Windows',title)
		title = re.sub('iphone','iOS',title)

		#titleWords = word_tokenize(title.strip()) 
		#title = " ".join(titleWords)

		title = re.sub('yo-kai watch dance just dance special version','yo-kai watch dance: just dance special version', title)
		title = re.sub('yo-kai watch dance just dance','yo-kai watch dance: just dance special version', title)
		title = re.sub('yo-kai watch dance: just dance','yo-kai watch dance: just dance special version', title)
		title = re.sub('just dance disney party','just dance: disney party',title)
		title = re.sub('just dance disney party 2','just dance: disney party 2',title)
		title = re.sub('just dance greatest hits','just dance: greatest hits',title)
		title = re.sub('just dance summer party','just dance: summer party',title)

		title = title.lower()

		#descript = description[row]
		"""
		descriptWords = word_tokenize(descript.strip()) 
		descript = " ".join(descriptWords)

		descript = " ".join(descript.strip().split())
		descript = re.sub(r"[\W\s]"," ",descript)
		descript = re.sub("\n","",descript)

		descript = descript.lower()
		descript = re.sub('jd','just dance',descript)
		descript = re.sub('justdance','just dance',descript)
		descript = re.sub('wiiu','wii u',descript)
		#descript = re.sub('ps2','PlayStation 2',descript)
		descript = re.sub('ps3','PlayStation 3',descript)
		descript = re.sub('ps4','PlayStation 4',descript)
		descript = re.sub('ps5','PlayStation 5',descript)
		descript = re.sub('playstation3','PlayStation 3',descript)
		descript = re.sub('playstation4','PlayStation 4',descript)
		descript = re.sub('playstation5','PlayStation 5',descript)
		descript = re.sub('x360','Xbox 360',descript)
		descript = re.sub('xbox sx','Xbox Series X',descript)
		descript = re.sub('xbox ss','Xbox Series S',descript)
		descript = re.sub('xbox360','Xbox 360',descript)
		descript = re.sub('xboxone','Xbox One',descript)
		descript = re.sub('nintendoswitch','Nintendo Switch',descript)
		descript = re.sub('switch','Nintendo Switch',descript)
		descript = re.sub('nintendo','Nintendo Switch',descript)
		descript = re.sub('windows','Microsoft Windows',descript)
		descript = re.sub('pc','Microsoft Windows',descript)
		descript = descript.lower()
		"""

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
		
		for game in games:
			serie = game.lower()

			if(serie in title.lower()):
				edition=game
				#print(edition)
				if (edition == "Just Dance 2"):
					continue
				if (edition == "Just Dance Wii"):
					continue
				if (edition == "Just Dance Kids"):
					continue
				if (edition == "Just Dance Kids 2"):
					continue
				if (edition == "Just Dance: Disney Party"):
					continue
				
			"""
			elif(serie in descript.lower()):
				edition=game
				if (edition == "Just Dance 2"):
					continue
				if (edition == "Just Dance Wii"):
					continue
				if (edition == "Just Dance Kids"):
					continue
				if (edition == "Just Dance Kids 2"):
					continue
				if (edition == "Just Dance: Disney Party"):
					continue
				else:
					break
			"""
		if(edition == ""): # PROBLEM 2018, 2019 ???
			serie = "Just Dance"
			if(serie.lower() in title.lower()):
				edition = "Just Dance"


		platforms = ['Wii', 'Wii U', 'PlayStation 3', 'PlayStation 4', 'PlayStation 5', 'Xbox 360', 'Xbox One', 'Xbox Series X', 'Xbox Series S','iOS', 'Android', 'Nintendo Switch', 'Microsoft Windows', 'Stadia']
		# detetar plataforma no titulo do video e na descrição ...
		platform = ""
		for p in platforms:
			c = p.lower()
			if(c in title.lower()):
				#print(p)
				if (c == 'android' or platform == 'ios'):
					if(edition != "Just Dance Now"):
						continue
					else:
						pass
				platform = p
				if (platform == "Wii"):
					continue
				if (platform == "Xbox Series X"):
					continue
				
				#break
			"""
			elif(c in descript.strip().lower()):
				platform = p
				if (platform == "Wii"):
					continue
				elif (platform == "Xbox Series X"):
					continue
				else:
					break
			"""

		if(platform == 'Android' or platform == 'iOS'):
			if (edition != "Just Dance Now"):
				platform="Unknown"
			else:
				pass

		if(platform==""):
			platform="Unknown"

		print("-> ",edition," -> ", platform)
		game_id +=1 
		query = "insert into game values('"+str(game_id)+"', '"+str(edition)+"', '"+str(platform)+"')"
		insertToTable(query)

		return game_id
	except Exception as e:
		print("get game and console ->", e)

def insertVideo(channelID,channel,videoID,title,dateVideo,views,likesVideo,dislikesVideo,totalCommentsVideo,descript):
	#insert youtube video ...
	query = "insert into video values('"+str(channelID)+"', '"+channel+"', '"+str(videoID)+"','"+title+"','"+str(dateVideo)+"', '"+str(views)+"', '"+str(likesVideo)+"', '"+str(dislikesVideo)+"', '"+str(totalCommentsVideo)+"', '"+descript+"')"
	insertToTable(query)
	#pass

def getConceptsAnnotated(comment, polarity):
	try:
		concepts=[]
		DictResult = annotate(str(comment), polarity) 
		if(bool(DictResult)):
			#print("\n")
			#print(DictResult)
			print("-----—————————————————————————————————————————————————————————————-")
			for c,v in DictResult.items():	
				if (v>0.70):
					
					polarity = polarity.lower()
					if (c=="Positive feelings" and polarity=="negative"):
						continue
					elif(c=="Negative feelings" and polarity=="positive"):
						continue
					elif(c=="Frustration" and polarity=="positive"):
						continue
					elif(c=="Pleasure" and polarity=="negative"):
						continue
					elif(c=="Enjoyment and Fun" and polarity=="negative"):
						continue
					elif(c=="Frustration" and polarity=="neutral"):
						continue
					elif(c=="Pleasure" and polarity=="neutral"):
						continue
					elif(c=="Enjoyment and Fun" and polarity=="neutral"):
						continue
					elif(c=="Fatigue" and polarity=="positive"):
						continue
					elif (c=="Pain and Discomfort" and polarity=="positive"):
						continue 
					elif (c=="Affect and Emotion" and polarity=="neutral"):
						continue
					else:
						print(c, v)
						concepts.append(c)
		# ... values = dict.values() -> total = sum (values) -> total de cada dim... 
		return concepts
	except Exception as e:
		print(e)

def executeAnnotation(game_id, annotation_id, videoID, comment, original_comment, commentID, likes, dateComment, isMain):

	try:
		#print(original_comment)
		#polarity = getSentiment(comment)
		polarity = getSentiment(original_comment)

		print("\n>>>>>>> ",original_comment)
		print(">>> ", polarity)

		#isMain = mainComment[row] # TRUE -> comentario principal

		#insert youtube video ...
		#query = "insert into video values('"+str(channelID)+"', '"+channel+"', '"+str(videoID)+"','"+title+"','"+str(dateVideo)+"', '"+str(views)+"', '"+str(likesVideo)+"', '"+str(dislikesVideo)+"', '"+str(totalCommentsVideo)+"', '"+descript+"')"
		#insertToTable(query)
		original_comment = original_comment.replace("'","")
		query = "insert into comment values('"+str(commentID)+"', '"+str(original_comment)+"', '"+str(comment)+"', '"+str(polarity)+"', '"+str(likes)+"', '"+str(dateComment)+"', '"+str(isMain)+"')"
		insertToTable(query)

		try:
			concepts = getConceptsAnnotated(str(comment), str(polarity))
			#print(concepts)
			if (len(concepts)>0):
				for d in dictFields.items():
					field = d[0]
					conceitos = d[1]
					#print(d[1])
					for c in conceitos:
						if (str(c) in concepts):
							annotation_id+=1
							#print(annotation_id,"... "+str(field)+" --> "+str(c))
												
							query = "insert into annotation values("+str(annotation_id)+",'"+str(field)+"','"+str(c)+"','"+str(commentID)+"','"+str(game_id)+"','"+str(videoID)+"')"
							insertToTable(query)
							
			else:
				print("NAO ANOTADO! sem conceitos ...")

			return annotation_id

		except Exception as e:
			print(e)
			
	except Exception as e:
		print("execute annotation - ", e)

	#return annotation_id
#insertTablesConceitos()

#executeAnnotation()










