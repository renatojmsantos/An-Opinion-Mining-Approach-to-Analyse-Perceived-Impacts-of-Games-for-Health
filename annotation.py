from connectDB import *

from vocabulary import *

from nrclex import NRCLex
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

import time

tagger = SequenceTagger.load("hunflair-disease")



def insertToTable(query):
	idBack = None
	conn = None
	
	try:
		params = config()
		conn = psycopg2.connect(**params)
		conn.autocommit = True
		cur = conn.cursor()
		query = query + " returning 1;" 

		cur.execute(query)
		idBack = cur.fetchone()
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			conn.close()
	return idBack


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


def annotate(text, polarity):

	text = re.sub('just dance','game',text)
	text = re.sub('im','i am',text)
	
	sno = nltk.stem.SnowballStemmer('english') 

	def pos_tagger(nltk_tag):
		if nltk_tag.startswith('J'):
			return wordnet.ADJ
		elif nltk_tag.startswith('V'):
			return wordnet.VERB
		elif nltk_tag.startswith('N'):
			return wordnet.NOUN
		else:          
			return None


	textWords = word_tokenize(text)
	pos_tagged = nltk.pos_tag(textWords)

	wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))

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

	
	text_lemmas = " ".join(pals_lemmas)
	

	score = 0.00
	scoreDict = {}

	print(" > ",text_lemmas)
	total_pals = len(word_tokenize(text_lemmas))

	t = NRCLex(str(text_lemmas))
	emotions = t.affect_frequencies

	emo = {}
	if(emotions):
		for c,v in emotions.items():
			if (v>0.18):
				if (c not in emo.keys()):
					emo[c] = v
	lexs = []
	for d in dictVocabulary.items():
		concept = d[0]
		pals = d[1]
		countPalsDict = 0
		score=0.00
		for pal, prob in pals.items():
			if (emo):
				for c,v in emo.items():	
					if (c in pal):
						countPalsDict += 0.5 
						if(len(text.split()) > 7):
							score = (v*prob)*1.4
						else:
							score = (v*prob)*1.0 
						if concept not in scoreDict.keys():
							scoreDict[concept] = score
						else:
							scoreDict[concept] += score
			else:
				pass

			stems=[]
			for lemma in pals_lemmas:
				word_stem = sno.stem(lemma)

				if (lemma == pal): 
					countPalsDict += 0.85 
					score = prob*1.0
					
					if concept not in scoreDict.keys():
						scoreDict[concept] = score
					else:
						scoreDict[concept] += score
				elif (lemma in pal and len(lemma) >=3):
					try:
						palwn = wordnet.synsets(str(pal))[0]
						lemmawn = wordnet.synsets(str(lemma))[0]

						similarity = lemmawn.path_similarity(palwn)
						if(similarity > 0.18):
							countPalsDict += 1
							score = prob*1.0
							if concept not in scoreDict.keys():
								scoreDict[concept] = score
							else:
								scoreDict[concept] += score
					except Exception as e:
						continue
				elif (word_stem in pal and len(word_stem)>1):
					stems.append(word_stem)
					try:
						palwn = wordnet.synsets(str(pal))[0]
						stemwn = wordnet.synsets(str(word_stem))[0]

						similarity = stemwn.path_similarity(palwn)
						if(similarity > 0.2):
							countPalsDict += 1
							score = prob*1.0
							if concept not in scoreDict.keys():
								scoreDict[concept] = score
							else:
								scoreDict[concept] += score
					except Exception as e:
						continue
				else: 
					for syn in wordnet.synsets(lemma):
						for l in syn.lemmas():
							antonym=""
							synonym=""
							if (l.antonyms()):
								if (concept == "Negative feelings" or concept == "Frustration" or concept == "Positive feelings" or concept == "Pain and discomfort" 
									or concept == "Fatigue" or concept == "Pleasure" or concept == "Errors/Effectiveness"):
									continue
								else:
									antonym = l.antonyms()[0].name()
									stem = sno.stem(antonym)
							else:
								synonym = l.name()
								stem = sno.stem(synonym)
							if (stem not in stems):
								stems.append(stem)
								
								if (synonym != "" and synonym == pal):
									countPalsDict += 1
									score = prob*0.87

									if concept not in scoreDict.keys():
										scoreDict[concept] = score
									else:
										scoreDict[concept] += score
								elif (antonym != "" and antonym == pal):
									countPalsDict += 1

									score = prob*0.85
									if concept not in scoreDict.keys():
										scoreDict[concept] = score
									else:
										scoreDict[concept] += score
								elif (stem in pal and len(stem)>=3):
									# similarity
									try:
										palwn = wordnet.synsets(str(pal))[0]
										stemwn = wordnet.synsets(str(stem))[0]

										similarity = stemwn.path_similarity(palwn)
										
										if(similarity > 0.35):
											countPalsDict += 1
											score = prob*0.80
											if concept not in scoreDict.keys():
												scoreDict[concept] = score
											else:
												scoreDict[concept] += score
										else:
											pass
									except Exception as e:
										continue									
							else:
								pass

						if (lemma not in lexs):
							lexs.append(lemma)

							#lexical relations
							lexical = wordnet.synset(syn.name())
							
							# conceito especifico
							for s in lexical.hyponyms():
								for l in s.lemmas():
									hyponym = l.name()
									stem = sno.stem(hyponym)
									if (stem not in stems):
										stems.append(stem)
										
										if (hyponym == pal):
											countPalsDict += 1
											score = prob * 0.72
											if concept not in scoreDict.keys():
												scoreDict[concept] = score
											else:
												scoreDict[concept] += score
										elif (stem in pal and len(stem)>=3):

											try:										
												palwn = wordnet.synsets(str(pal))[0]
												stemwn = wordnet.synsets(str(stem))[0]

												similarity = stemwn.path_similarity(palwn)
												
												if(similarity > 0.3):
													countPalsDict += 1
													score = prob * 0.68

													if concept not in scoreDict.keys():
														scoreDict[concept] = score
													else:
														scoreDict[concept] += score

											except Exception as e:
												continue
									else:
										pass
										
							# conceitos mais gerais
							for s in lexical.hypernyms():
								for l in s.lemmas():
									hypernym = l.name()
									stem = sno.stem(hypernym)
									if (stem not in stems):
										stems.append(stem)
										if (hypernym == pal):
											countPalsDict += 1
											score = prob * 0.72

											if concept not in scoreDict.keys():
												scoreDict[concept] = score
											else:
												scoreDict[concept] += score
										elif (stem in pal and len(stem)>=3):
											try:										
												palwn = wordnet.synsets(str(pal))[0]
												stemwn = wordnet.synsets(str(stem))[0]

												similarity = stemwn.path_similarity(palwn)
												
												if(similarity > 0.3):
													countPalsDict += 1
													score = prob * 0.68
													
													if concept not in scoreDict.keys():
														scoreDict[concept] = score
													else:
														scoreDict[concept] += score
											except Exception as e:
												continue
									else:
										pass
										
							# parte de algo
							for s in lexical.part_meronyms():
								for l in s.lemmas():
									meronym = l.name()
									stem = sno.stem(meronym)
									if (stem not in stems):
										stems.append(stem)
										
										if (meronym == pal):
											countPalsDict += 1
											score = prob * 0.72
											if concept not in scoreDict.keys():
												scoreDict[concept] = score
											else:
												scoreDict[concept] += score
										elif (stem in pal and len(stem)>=3):
											try:										
												palwn = wordnet.synsets(str(pal))[0]
												stemwn = wordnet.synsets(str(stem))[0]

												similarity = stemwn.path_similarity(palwn)
												
												if(similarity > 0.3):
													
													countPalsDict += 1

													score = prob * 0.68
													if concept not in scoreDict.keys():
														scoreDict[concept] = score
													else:
														scoreDict[concept] += score
											except Exception as e:
												continue

									else:
										pass
			
							
						else:
							continue
		
		if concept in scoreDict.keys():
			scoreDict[concept] = scoreDict[concept]/countPalsDict

	return scoreDict


def checkGameID(edition,platform):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()

		query = "SELECT game_id FROM game WHERE edition = '"+edition+"' and platform = '"+platform+"'"

		cur.execute(query)
		idBack = cur.fetchall()

		for row in idBack:
			if (row is not None):
				idBack=row
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			conn.close()
	return idBack

def getSentiment(t):

	try:
		analyzer = SentimentIntensityAnalyzer()
		vsOriginal = analyzer.polarity_scores(str(t))
		
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
		title = re.sub('apple','iOS',title)
		title = re.sub('xbox one s','Xbox Series S',title)
		title = re.sub('xbox one x','Xbox Series X',title)

		title = re.sub('yo-kai watch dance just dance special version','yo-kai watch dance: jd sv', title)
		title = re.sub('yo-kai watch dance just dance','yo-kai watch dance: jd sv', title)
		title = re.sub('yo-kai watch dance: just dance','yo-kai watch dance: jd sv', title)
		title = re.sub('just dance disney party','just dance: disney party',title)
		title = re.sub('just dance disney party 2','just dance: disney party 2',title)
		title = re.sub('just dance greatest hits','just dance: greatest hits',title)
		title = re.sub('just dance summer party','just dance: summer party',title)

		title = title.lower()

		#https://en.wikipedia.org/wiki/Just_Dance_(video_game_series)
		games = ['Just Dance 2', 'Just Dance 3', 'Just Dance 4', 'Just Dance 2014', 'Just Dance 2015', 'Just Dance 2016', 'Just Dance 2017', 'Just Dance 2018', 'Just Dance 2019', 'Just Dance 2020', 'Just Dance 2021', 'Just Dance 2022', 'Just Dance 2023',
				'Just Dance Wii', 'Just Dance Wii 2', 'Just Dance Wii U', 'Yo-kai Watch Dance: JD SV',
				'Just Dance Kids', 'Just Dance Kids 2', 'Just Dance Kids 2014',
				'Just Dance: Disney Party', 'Just Dance: Disney Party 2',
				'Just Dance: Greatest Hits',
				'Just Dance: Summer Party', 'Just Dance Now', 'Just Dance Unlimited']
		
		# detetar o nome do jogo no titulo do video ...
		edition=""
		serie=""
		
		for game in games:
			serie = game.lower()

			if(serie in title.lower()):
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
				
		if(edition == ""): 
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
	query = "insert into video values('"+str(channelID)+"', '"+channel+"', '"+str(videoID)+"','"+title+"','"+str(dateVideo)+"', '"+str(views)+"', '"+str(likesVideo)+"', '"+str(dislikesVideo)+"', '"+str(totalCommentsVideo)+"', '"+descript+"')"
	insertToTable(query)

def getConceptsAnnotated(comment, polarity):
	try:
		concepts=[]
		DictResult = annotate(str(comment), polarity) 
		if(bool(DictResult)):
			print("-----—————————————————————————————————————————————————————————————-")
			print(DictResult)
			print("-----—————————————————————————————————————————————————————————————-")
			for c,v in DictResult.items():	
				if (v>=0.75):
					
					polarity = polarity.lower()
					if (c=="Positive feelings" and polarity=="negative"):
						continue
					elif(c=="Negative feelings" and polarity=="positive"):
						continue
					if (c=="Positive feelings" and polarity=="neutral"):
						continue
					elif(c=="Negative feelings" and polarity=="neutral"):
						continue
					elif(c=="Frustration" and polarity=="positive"):
						continue
					elif(c=="Frustration" and polarity=="neutral"): 
						continue
					elif(c=="Pleasure" and polarity=="negative"):
						continue
					elif(c=="Enjoyment and Fun" and polarity=="neutral"):
						continue
					elif(c=="Pleasure" and polarity=="neutral"):
						continue
					elif(c=="Fatigue" and polarity=="positive"):
						continue
					elif (c=="Pain and Discomfort" and polarity=="positive"):
						continue 
					elif (c=="Affect and Emotion" and polarity=="neutral"): 
						continue
					elif (c=="Trust" and polarity=="neutral"):
						continue
					elif (c=="Errors/Effectiveness" and polarity=="positive"):
						continue
					elif (c=="Motivation" and polarity=="neutral"): 
						continue
					elif (c=="Hedonic" and polarity=="neutral"): 
						continue
					elif (c=="Enchantment" and polarity=="neutral"): 
						continue
					elif (c=="Likeability" and polarity=="neutral"): 
						continue
					elif (c=="Satisfaction" and polarity=="neutral"):
						continue
					else:
						concepts.append(c)
		print ("\n",concepts,"\n")
		return concepts
	except Exception as e:
		print(e)


def executeAnnotation(game_id, annotation_id, videoID, comment, original_comment, commentID, likes, dateComment, isMain):

	try:
		polarity = getSentiment(original_comment)

		print("\n=======================================================================================================================")
		print(">>> ",original_comment,"\n")

		print("# ", polarity)


		original_comment = original_comment.replace("'"," ")
		query = "insert into comment values('"+str(commentID)+"', '"+str(original_comment)+"', '"+str(comment)+"', '"+str(polarity)+"', '"+str(likes)+"', '"+str(dateComment)+"', '"+str(isMain)+"')"
		insertToTable(query)

		try:
			concepts = getConceptsAnnotated(str(comment), str(polarity))
			
			if (len(concepts)>0):
				for d in dictFields.items():
					field = d[0]
					conceitos = d[1]
					for c in conceitos:
						if (str(c) in concepts):
							annotation_id+=1
							print(annotation_id,"... "+str(field)+" --> "+str(c))

							query = "insert into annotation values("+str(annotation_id)+",'"+str(field)+"','"+str(c)+"','"+str(commentID)+"','"+str(game_id)+"','"+str(videoID)+"')"
							insertToTable(query)
			else:
				pass

			return annotation_id

		except Exception as e:
			print(e)
			
	except Exception as e:
		print("execute annotation - ", e)












