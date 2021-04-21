


from annotation import * 


def annotate(text):
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
		elif nltk_tag.startswith('V'):
			return wordnet.VERB
		elif nltk_tag.startswith('N'):
			return wordnet.NOUN
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

def getcomments():
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT commentid, originaltext, processedtext FROM comment"
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

def getAnnotation(commentid):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT field, concept, game_game_id, video_videoid FROM annotation where comment_commentid='"+commentid+"'"
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

		query = "SELECT video_videoid, comment_commentid FROM annotation where game_game_id='"+gameid+"'"
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
		print(query)
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


#-----------
# UPDATE ALSO GAME EDITION!!! NAO DETECT JUST DANCE 2016, 2017, ...
# select videotitle from video where videotitle like '%Just Dance 2 %'

#-----------------------------------------------------------------------------------------

def updateVocabulary():
	pass

def updatePolarityComment():
	pass

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


updateInfoGame()


#-----------------------------------------------------------------------------------------

def update():
	opinionid = int(countRowsTable('opinion'))# + 1

	comments = getcomments()
	#print(idBack)
	for c in comments:
		if (c is not None):
			#print(c[0])
			comment = c[0]
			commentid = c[1]
			req = getGameVideoID(commentid)
			if (req is not None):
				game_id = req[0]
				videoID = req[1]
				print(game_id,videoID)
			try:
				DictResult = annotate(str(comment))

				#idsDimensions = getdimension_id(commentid)
				old = []
				for dim in getdimension_id(str(commentid)):
					dimID = dim[0]
					#print(dim[0])
					
					annot = getAnnotation(str(dimID))
					#print(annot)
					
					for res in annot:
						#field_OLD = res[0]
						concept_OLD = res[1]
						#print(field_OLD,concept_OLD)
						old.append(concept_OLD)
					
				print(old)
				print(DictResult)
				if(bool(DictResult)):
					for field in DictResult.keys():
						for concept in DictResult[field]:
							#opinion_id+=1
							#dimension_id+=1
							if(concept in old):
								break
							else:	
								dimensionid +=1
								opinionid += 1
								#updateDimension(str(dimID), field, concept) ???? NAO FAZ UPDATE !!!!!!!!!!!!!!!! SÓ ESTAMOS A ACRESCENTAR MAIS COISAS...
								query = "insert into dimension values('"+str(dimensionid)+"', '"+str(field)+"', '"+str(concept)+"')"
								insertToTable(query)

								query = "insert into opinion values('"+str(opinionid)+"', '"+str(commentid)+"', '"+str(dimensionid)+"', '"+str(game_id)+"', '"+str(videoID)+"')"
								insertToTable(query)
								# ver caso do nr de ids da dimensao desse comentario exceder...... ou nao tiver, e entao é apagado.
						
			except Exception as e:
				print("execute annotation - ", e)
		else:
			print("none....")

#update()

