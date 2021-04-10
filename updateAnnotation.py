


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


def getcomments():
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT comment, commentid FROM comment"
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
		print("ERRO!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack


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
		print("ERRO!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack[0]# is not None #idBack

def getdimension_id(commentid):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT dimension_dimension_id, comment_commentid FROM opinion where comment_commentid='"+commentid+"'"
		#print(query)
		cur.execute(query)
		idBack = cur.fetchall()

		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO dim!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

def getAnnotation(dimensionid):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT field, concept FROM dimension where dimension_id='"+dimensionid+"'"
		print(query)
		cur.execute(query)
		idBack = cur.fetchall()

		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO anno!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

def getGameVideoID(commentid):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT game_game_id, video_videoid FROM opinion where comment_commentid='"+commentid+"'"
		print(query)
		cur.execute(query)
		idBack = cur.fetchone()

		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO anno!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

def updateDimension(dimensionid, field, concept):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		#query = "SELECT field, concept FROM dimension where dimension_id='"+dimensionid+"'"
		query = "UPDATE dimension SET field = '"+field+"', concept = '"+concept+"' where dimension_id='"+dimensionid+"' returning *;"
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




def update():
	opinionid = int(countRowsTable('opinion'))# + 1
	dimensionid = int(countRowsTable('dimension'))# + 1

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

update()

