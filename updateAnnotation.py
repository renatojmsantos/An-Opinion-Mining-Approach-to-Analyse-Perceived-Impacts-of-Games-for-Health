


from annotation import * 

#from vaderSentiment import SentimentIntensityAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from flair.data import Sentence
from flair.models import SequenceTagger

#tagger = SequenceTagger.load("hunflair-disease")

def annotate(text, polarity):
	

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


	score = 0.00
	scoreDict = {}

	print("\n>>>>>>> ",text_lemmas)
	print(">>> ", polarity)
	t = NRCLex(str(text_lemmas))
	#print(t)
	#print(t.affect_list)
	#print(t.affect_dict)
	#print(t.raw_emotion_scores)
	#print(t.top_emotions)
	emotions = t.affect_frequencies
	# valid > 0.18
	#print(emotions)
	emo = {}
	if(emotions):
		for c,v in emotions.items():
			if (v>0.18):
				#print(c,v)
				polarity = polarity.lower()
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
				if (c not in emo.keys()):
					emo[c] = v
					# check polarity...
					#check if is negative and positive...

	print(emo)
	
	
	for d in dictVocabulary.items():
		#print(voc)
		concept = d[0]
		pals = d[1]
		print("====================="+concept+"=====================")
		conta = 0
		for pal, prob in pals.items():
			for c,v in emo.items():	
				score=0.00
				if (c in pal):
					conta+=1
					score = v*prob
					if concept not in scoreDict.keys():
						scoreDict[concept] = score
					else:
						# NR TOTAL DE VEZES QUE APARECE A DIVIDIR PELO NR TOTAL DE VEZES DE pals DETETADOS
						# 5 PALS DETETADAS.... 2 JOY / 5 = ...
						#score = score/conta
						print(pal, conta, v, prob, score)
						scoreDict[concept] += score

		# STEMMING ......
		# IF STEM IN PAL... RADICAL DENTRO DOS TERMOS EM ESTUDO.... + FACIL

	return scoreDict



def countRowsTable(tableName):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT count(*) FROM "+tableName+""

		#print(query)

		cur.execute(query)

		idBack = cur.fetchone() # TUPLO
		
		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO! count rows", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack[0]# is not None #idBack

def getcomments(commentid):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT processedtext, polarity FROM comment where commentid='"+commentid+"'"
		#print(query)
		cur.execute(query)

		idBack = cur.fetchall()
		#print(idBack)
		#for row in idBack:
		#	if (row is not None):
		#		print(row)
				#idBack=row
				#return idBack 
		#print(idBack)
		#conn.commit()
		#print("inserted!")
		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO! get comments", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

def getIDs():
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT comment_commentid, game_game_id, video_videoid FROM annotation group by comment_commentid, game_game_id,video_videoid;"
		#print(query)
		cur.execute(query)
		idBack = cur.fetchall()

		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO get annotation!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

def getVideo(videoid):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT videotitle, description FROM video where videoid='"+videoid+"'"
		#print(query)
		cur.execute(query)
		idBack = cur.fetchone()

		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO get video!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

def getVideoID(gameid):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT videoid FROM video where totalcommentsvideo > 0;"
		#print(query)
		cur.execute(query)
		idBack = cur.fetchone()

		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO get video!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

def getGames():
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT game_id FROM game"
		#print(query)
		cur.execute(query)
		idBack = cur.fetchall()

		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO get game!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

# UPDATE

def updateAnnotation(annotationid, field, concept):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		#query = "SELECT field, concept FROM dimension where dimension_id='"+dimensionid+"'"
		query = "UPDATE annotation SET field = '"+field+"', concept = '"+concept+"' where annotationid='"+annotationid+"' returning *;"
		print(query)
		cur.execute(query)
		idBack = cur.fetchall()

		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO upd!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

def updateComment(commentid, polarity):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		conn.autocommit = True
		cur = conn.cursor()

		#query = "SELECT field, concept FROM dimension where dimension_id='"+dimensionid+"'"
		query = "UPDATE comment SET polarity = '"+polarity+"' where commentid='"+commentid+"' returning *;"
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
#print(countRowsTable('game'))
#game_id = int(countRowsTable('game'))# + 1

def updateAnnotation(annotationid, field, concept, commentid,gameid, videoid):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		conn.autocommit = True
		cur = conn.cursor()

		#query = "SELECT field, concept FROM dimension where dimension_id='"+dimensionid+"'"
		query = "UPDATE annotation SET annotationid = '"+annotationid+"', field = '"+field+"', concept = '"+concept+"', comment_commentid = '"+commentid+"', game_game_id = '"+gameid+"' , video_videoid = '"+videoid+"' returning *;"
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
#print(countRowsTable('game'))
#game_id = int(countRowsTable('game'))# + 1


def insertToTable(query):
	idBack = None
	conn = None
	
	try:
		params = config()
		conn = psycopg2.connect(**params)
		conn.autocommit = True
		cur = conn.cursor()

		query = query + " returning 1;" 
		print(query)
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


def deleteRow(query):
	idBack = None
	conn = None
	
	try:
		params = config()
		conn = psycopg2.connect(**params)
		conn.autocommit = True
		cur = conn.cursor()

		query = query + " returning *;" 
		print(query)
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

def updatePolarityComment():
	
	#print(idBack)
	try:
		comments = getcomments()
		analyzer = SentimentIntensityAnalyzer()
		for c in comments:
			commentid = c[0]
			originaltext = c[1]
			#processedtext = c[2]
			#originalPolarity = c[3]
			#print(commentid, originaltext, processedtext)
			vsOriginal = analyzer.polarity_scores(originaltext)
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
			#print(polarity)
			updateComment(commentid,polarity)
			
			#positive sentiment: compound score >= 0.05
			#neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
			#negative sentiment: compound score <= -0.05

	except Exception as e:
		print(e)

#updatePolarityComment()

def checkInfoGame(title, descript):
	try:
		title = re.sub('&quot;+','',title)
		title = title.lower() 

		# substituir JD por Just Dance .... no titulo do video ....
		title = re.sub('jd','just dance',title)
		title = re.sub('justdance','just dance',title)
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
		title = re.sub('switch','Nintendo Switch',title)
		title = re.sub('nintendo','Nintendo Switch',title)
		title = re.sub('windows','Microsoft Windows',title)
		title = re.sub('pc','Microsoft Windows',title)

		titleWords = word_tokenize(title.strip()) 
		title = " ".join(titleWords)
		title = title.lower()

		#descript = description[row]
		descriptWords = word_tokenize(descript.strip()) 
		descript = " ".join(descriptWords)

		descript = " ".join(descript.strip().split())
		descript = re.sub(r"[\W\s]"," ",descript)
		descript = re.sub("\n","",descript)

		descript = descript.lower()
		descript = re.sub('jd','just dance',descript)
		descript = re.sub('justdance','just dance',descript)
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
		descript = re.sub('switch','Nintendo Switch',descript)
		descript = re.sub('nintendo','Nintendo Switch',descript)
		descript = re.sub('windows','Microsoft Windows',descript)
		descript = re.sub('pc','Microsoft Windows',descript)
		descript = descript.lower()

		platforms = ['Wii', 'Wii U', 'PlayStation 3', 'PlayStation 4', 'PlayStation 5', 'Xbox 360', 'Xbox One', 'Xbox Series X', 'Xbox Series S','iOS', 'Android', 'Nintendo Switch', 'Microsoft Windows', 'Stadia']
		# detetar plataforma no titulo do video e na descrição ...
		platform = ""
		for p in platforms:
			c = p.lower()
			if(c in title.lower()):
				platform = p
				if (platform == "Wii"):
					continue
				else:
					break
				#break
			elif(c in descript.strip().lower()):
				platform = p
				if (platform == "Wii"):
					continue
				else:
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
		
		for game in games:
			serie = game.lower()
			if(serie in title.lower()):
				edition=game
				#print(edition)
				if (edition == "Just Dance 2"):
					continue
				else:
					break
			elif(serie in descript.lower()):
				edition=game
				if (edition == "Just Dance 2"):
					continue
				else:
					break
		if(edition == ""): # PROBLEM 2018, 2019 ???
			serie = "Just Dance"
			if(serie.lower() in title.lower()):
				edition = "Just Dance"

		#game_id +=1 
		#query = "insert into game values('"+str(game_id)+"', '"+str(edition)+"', '"+str(platform)+"')"
		#insertToTable(query)

		#return game_id
		return (edition,platform)
	except Exception as e:
		print("erro check update: ", e)
	pass

def updateInfoGame():

	try:
		idsGame = getGames()
		for g in idsGame:
			gameid = g[0]

			videoid = getVideoID(str(gameid))
			
			#print(videoid[0])
			if (videoid is not None):
				commentid = videoid[1]
				video = getVideo(str(videoid[0]))
				if (video is not None):
					#print(video)
					descript = str(video[1]).lower()
					#print(descript)
					if (("covers" in descript) or ("maristela" in descript) or ("killebom" in descript)
						or ("ivi adamou" in descript) or ("talent show" in descript) or ("music video" in descript) 
						or ("the nanny" in descript) or ("josh turner" in descript) or ("karaoke" in descript) or ("quadriphonix" in descript) or ("acoustic" in descript)
						or ("Jerónimo de Sousa" in descript) or ("paul johnson" in descript) and ("remix" in descript) or ("flashmob" in descript) or ("ps22 chorus" in descript)
						or ("chipettes" in descript) or ("chipmunk" in descript) or ("chipmunks" in descript) or ("just dance india" in descript) or ("official music video" in descript)):
						
						query = "delete from annotation where game_game_id='"+str(gameid)+"'"
						#print(query)
						deleteRow(query)
						query = "delete from video where videoid='"+str(videoid[0])+"'"
						#print(query)
						deleteRow(query)
						query = "delete from game where game_id='"+str(gameid)+"'"
						#print(query)
						deleteRow(query)
						query = "delete from comment where commentid='"+str(commentid)+"'"
						#print(query)
						deleteRow(query)
						
					else:
						check = checkInfoGame(str(video[0]), str(video[1]))
						if (check is not None):
							#print(check[0], check[1])
							updateGame(str(gameid), str(check[0]), str(check[1]))

	except Exception as e:
		print(e)

#updateInfoGame()

#-----------------------------------------------------------------------------------------

def update():
	annotationid=0
	
	try:
		ids = getIDs()
		for i in ids:
			commentid = i[0]
			gameid = i[1]
			videoid = i[2]
			
			comments = getcomments(commentid)
			for c in comments:
				comment = c[0]
				polarity = c[1]
				#print(commentid, gameid, videoid, comment)
				# update ... annotation id = 1,2,3...
				DictResult = annotate(str(comment), polarity) 
				if(bool(DictResult)):
					print(DictResult)

					# ... values = dict.values() -> total = sum (values) -> total de cada dim... 
					#updateAnnotation(annotationid, field, concept, commentid,gameid, videoid)
	except Exception as e:
		print(e)
	

update()

