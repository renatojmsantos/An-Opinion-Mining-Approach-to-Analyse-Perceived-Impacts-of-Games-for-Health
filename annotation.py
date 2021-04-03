
from preprocessing import *
from connectDB import *
import pandas as pd

from nrclex import NRCLex
from senticnet.senticnet import SenticNet
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

#nltk.download('averaged_perceptron_tagger')

# ver artigo CHI 13, table 8
dict={	
		'Usability':{
			'Memorability': {'memory': 1.0, 'forgot': 0.6}, 
			'Learnability': {'learnability': 1.0, 'learn': 1.0, 'intuit': 1.0, 'easier': 1.0,'figur': 0.8,'straightforward': 0.8,'foreword': 0.8, 'practic': 0.6}, 
			'Efficiency': {'efficiency': 1.0, 'perfect': 0.9, 'works well': 1.0}, 
			'Errors/Effectiveness': {'errors': 1.0,'effectiveness':1.0, 'fix': 0.8,'problem':0.5, 'camera': 0.7, 'glitch': 0.8,'issu': 0.8,'lag': 0.8,'bug': 0.8, 'inconsist': 0.8},
			'Satisfaction': {'happy': 1.0, 'fun': 1.0, 'great': 1.0, 'love': 1.0, 'worth': 1.0, 'nice': 1.0, 'best': 1.0, 'recommend': 1.0, 'disappoint': 0.8, 'good': 0.8, 'favorite': 0.8, 'cool': 0.8, 'perfect': 1.0}
		},
		'UX':{
			'Likeability': {'likeability': 1.0, 'like':0.9}, 
			'Pleasure': {'pleasure': 1.0, 'fun': 0.7, 'moneybag':0.7, 'enjoy': 0.7, 'love': 0.7, 'entertain': 0.7, 'awesome': 0.8, 'stimulation':0.7, 'felt': 0.7, 'sooth': 0.7, 'adict': 0.7, 'nostalgia': 0.7},
			'Comfort': {'comfort': 1.0, 'physical': 0.7},
			'Trust': {'trust': 1.0, 'behavior': 0.8},
			'Anticipation': {'anticipation': 1.0, 'expectation': 1.0},
			'Overall Usability': {'overall usability': 1.0, 'new version': 0.8, 'upgrade':0.8, 'edition': 0.8, 'previous edition':0.8},
			'Hedonic': {'hedonic': 1.0, 'fun': 0.8, 'enjoy': 0.8, 'frustrat': 0.8, 'fulfillment': 0.9, 'needs': 0.8, 'pleasure':0.7,'enjoyment':0.7,'frustration':0.7, 'annoy': 0.8, 'entertain': 0.8, 'game': 0.8,'multiplayer': 0.8, 'gaming': 0.8, 'gameplay': 0.8, 'play': 0.8, 'humor': 0.8, 'workout': 0.8, 'nostalgia': 0.6},
			'Detailed Usability': {'detailed usability': 1.0, 'great': 0.7, 'details': 0.9, 'functions': 0.9, 'satisfaction': 0.7,'usability': 0.7, 'best':0.7, 'problem': 0.7},
			'User Differences': {'user differences': 1.0,'user group': 0.7,'group': 0.7,'beginners':0.9, 'veterans':0.9,'pro player':0.9, 'amateur':0.9,'professional':0.9,'finalists':0.6, 'professional dancers':0.8,'buyers': 0.7,'target': 0.7,'features': 0.7, 'differences': 0.7, 'if you': 0.6},
			'Support': {'support':1.0, 'help':0.8, 'wish': 0.7,'software': 0.7,},
			'Impact': {'impact': 1.0, 'pattern': 0.7, 'surprise': 1.0,'fear': 1.0,'change gameplay': 0.9},
			'Affect and Emotion': {'affect': 1.0, 'emotion': 1.0, 'trust': 1.0,'surprise': 1.0,'fear': 1.0,'disgust': 1.0,'frustration': 0.7,'anger': 1.0,'fun': 0.8, 'enjoy': 0.8, 'addict': 0.7, 'workout': 0.7, 'excit': 0.8, 'cute': 0.8, 'nevertheless': 0.8, 'laugh': 0.8, 'annoy': 0.8},
			'Enjoyment and Fun': {'joy':0.9, 'enjoyment': 1.0, 'hedonic': 1.0,'emotion': 1.0,'affect': 1.0,'fun': 1.0, 'younger': 0.7, 'entertain': 0.9},
			'Aesthetics and Appeal': {'aesthetics': 1.0, 'taste': 1.0,'beauty': 1.0,'appreciation': 1.0,'appeal': 1.0, 'graphic':0.9, 'sound':0.9, 'song': 0.9, 'voice':0.9, 'playlist':0.9, 'music':0.9, 'soundtrack':0.9, 'effect':0.8, 'look':0.8, 'color':0.8, 'visual': 0.8, 'detail': 0.6, 'render': 0.5, 'pixel': 0.5},
			'Engagement': {'engagement': 1.0, 'challeng': 0.9, 'flow': 1.0,'skills': 1.0,'needs': 1.0,'forget': 1.0,'engaged': 1.0,'addict': 0.9, 'addition': 1.0, 'replay':0.7, 'nonstop': 0.9, 'interest':0.7},
			'Motivation': {'motivation': 1.0, 'task': 1.0, 'joy': 0.8},
			'Enchantment': {'enchantment': 1.0, 'concentration': 1.0,'attention': 1.0,'liveliness': 1.0,'fullness': 1.0,'pleasure': 1.0,'disorientation': 1.0,'experience': 1.0},
			'Frustration': {'frustration': 1.0, 'hardship': 1.0,'boring': 0.8, 'anger': 1.0,'hardest': 0.7, 'dissadvantag': 0.8, 'insult': 0.7, 'injuri': 0.7, 'nerv': 0.7, 'unfair':0.7, 'cheat':0.7, 'annoy':0.7, 'incompatibilit':0.7},
		},
		'Health':{
			'Pain and discomfort': {'pain': 1.0, 'distressing': 1.0,'unpleasant': 1.0,'discomfort': 1.0}, 
			'Energy': {'energy': 1.0, 'alive': 1.0, 'endurance': 1.0,'enthusiasm': 0.9 },
			'Fatigue': {'fatigue': 1.0, 'exhaustion': 0.9},
			'Sleep and rest': {'sleep': 1.0,'waking up': 1.0, 'refreshment': 1.0,'rest': 1.0},
			'Positive feelings': {'positive feelings': 1.0, 'enjoyment': 1.0,'joy': 1.0,'hopefulness': 1.0,'happiness': 1.0,'peace': 1.0,'balance': 1.0,'contentment': 1.0},
			#'Thinking, learning, memory and concentration': {'thinking': 1.0, 'aware': 1.0,'awake': 1.0,'alert': 1.0,'cognitive': 1.0,'thought': 1.0,'decisions': 1.0,'forget': 1.0, 'learning': 1.0, 'memory': 1.0, 'concentration': 1.0},
			'Thinking': {'thinking': 1.0, 'aware': 1.0,'awake': 1.0,'cognitive': 1.0,'intelligent': 1.0,'idea': 1.0,'thought': 1.0,'decisions': 1.0},
			'Learning': {'cognitive': 1.0, 'education': 1.0,'knowledge': 1.0,'pedagogy': 1.0, 'learning': 1.0,  'learn': 1.0},
			'Memory': {'forget': 1.0, 'alzheimer': 0.7, 'dementia': 0.8,'nostalgia':0.9, 'memory': 1.0, 'cognitive': 0.8},
			'Concentration': {'aware': 1.0,'awake': 1.0,'alert': 1.0,'attention': 0.9, 'cognitive': 0.8, 'concentration': 1.0},
			'Self-esteem': {'self-esteem': 1.0, 'meaningful': 1.0,'self-acceptance': 1.0,'dignity': 1.0,'family': 1.0,'people': 1.0,'education': 1.0,'control': 1.0,'oneself': 1.0,'satisfaction': 1.0},
			'Bodily image and appearance': {'bodily image': 1.0, 'handicapped': 1.0,'physical handicapped': 1.0,'physical': 1.0,'body image': 1.0,'limbs': 1.0,'artificial limbs': 1.0,'clothing': 1.0,'make-up': 1.0,'impairments': 1.0,'looks': 1.0,'appearance': 0.9, 'body': 0.8},
			'Negative feelings': {'negative feelings': 1.0, 'disgust': 1.0, 'fear': 1.0,'lack': 1.0,'anger': 1.0,'anxiety': 1.0,'nervousness': 1.0,'despair': 1.0,'tearfulness': 1.0,'sadness': 1.0,'guilt': 1.0,'despondency': 1.0},
			'Personal relationships': {'personal relationships': 1.0, 'homosexual': 1.0,'heterosexual': 1.0,'marriage': 1.0,'friendship': 1.0,'satisfaction': 1.0,'hug': 1.0,'happy': 1.0,'emotionally': 1.0,'relationships': 1.0,'intimate': 1.0,'love': 1.0,'support': 1.0,'companionship': 1.0,'friends': 1.0, 'family': 1.0, 'alone': 1.0},
			'Social support': {'Social support': 1.0, 'encouragement': 1.0,'solve': 1.0,'personal': 1.0,'responsability': 1.0,'assistance': 1.0,'approval': 1.0,'commitment': 1.0,'friends': 1.0,'family': 1.0},
			'Sexual activity': {'Sexual activity': 1.0, 'physical intimacy': 1.0,'sexual': 1.0,'desire for sex': 1.0,'sex': 0.9}
		}
	}



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
		print(query)
		#print(tableName)
		#cur.execute(query, (tableName,))
		cur.execute(query)
		idBack = cur.fetchone()
		#print(idBack)
		conn.commit()
		print("inserted!")
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack

def insertTablesConceitos():
	for items in dict.items():
		chave = items[0]
		conceitos = items[1]
		#print("\n",chave,conceitos)
		#print("\n>> ",chave)
		for vocabulario in conceitos.items():
			termo = vocabulario[0]
			#pals = vocabulario[1]
			#print(termo,pals)
			#print(" #", termo)
			if(chave=="Usability"):
				#insert into usability values('Satisfaction');
				query = "insert into usability values('"+termo+"')"
				#print(query)
				#tableName = "usability"
				insertToTable(query)
			elif(chave=="UX"):
				#print("ux")
				query = "insert into ux values('"+termo+"')"
				insertToTable(query)
			elif(chave == "Health"):
				#print("health")
				query = "insert into health values('"+termo+"')"
				insertToTable(query)

#insertTablesConceitos()

def annotate(text, polarity):
	print("\n>>>>>>> ",text)
	print(">>> ", polarity)

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

						# conceitos mais gerais
						for s in lexical.hyponyms():
							for l in s.lemmas():
								#print(l.name())
								if (l.name() not in listAnalysis):
									listAnalysis.append(l.name())

						for s in lexical.hypernyms():
							for l in s.lemmas():
								#print(l.name())
								if (l.name() not in listAnalysis):
									listAnalysis.append(l.name())

						# parte de um todo de uma relação
						for s in lexical.part_holonyms():
							for l in s.lemmas():
								#print(l.name())
								if (l.name() not in listAnalysis):
									listAnalysis.append(l.name())

						for s in lexical.part_meronyms():
							for l in s.lemmas():
								#print(l.name())
								if (l.name() not in listAnalysis):
									listAnalysis.append(l.name())

						# entailments -> implicacoes
						for s in lexical.entailments():
							for l in s.lemmas():
								#print(l.name())
								if (l.name() not in listAnalysis):
									listAnalysis.append(l.name())

				#print(listAnalysis)
				if(keyword in listAnalysis):
					if chave not in dictAnotado.keys():
						print(keyword)
						dictAnotado[chave] = [termo]
					elif termo not in dictAnotado[chave]:
						print(keyword)
						dictAnotado[chave].append(str(termo))

				# CHECK SIMILARITY ENTRE AS PALAVRAS DA LISTA E AS KEYWORDS? ...............

	return dictAnotado


teste = ["this give me nostalgia","this game is awesome", "can you fix the servers?", "i burned a lot of calories playing this", 'if you like multiplayer strategy games, buy this with confidence',
			'those expectations were met. Mostly, anyway', 'making the game enjoyable for beginners as well as veterans.','Multiplayer is excellent, but the single player campaign isn’t.',
			'Most of the inter-mission story telling happen in this mode, which tend to be awkward and clumsy.',
			'Most of the missions are enjoyable, and each one has optional goals which add replay value.']

def executeAnnotation():
	row = 0
	for t in teste: #t in comments:
		try:
			t = runPreprocessing(t)
			if (t != "None"):
				# print texto tratado e valido
				#print(">>>>>",t) 
				#sentiment analysis
				try:
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

					title = videoTitle[row]
					title = demoji(title)
					title = re.sub('&quot;+','',title)
					title = title.lower()

					# substituir JD por Just Dance .... no titulo do video ....

					# detetar o nome do jogo no titulo do video ...
					# detetar plataforma no titulo do video e na descrição ...

					#print(title)
					#https://en.wikipedia.org/wiki/Just_Dance_(video_game_series)
					games = ['Just Dance', 'Just Dance 2', 'Just Dance 3', 'Just Dance 4', 'Just Dance 2014', 'Just Dance 2015', 'Just Dance 2016', 'Just Dance 2017', 'Just Dance 2018', 'Just Dance 2019', 'Just Dance 2020', 'Just Dance 2021',
							'Just Dance Wii', 'Just Dance Wii 2', 'Just Dance Wii U', 'Yo-kai Watch Dance: Just Dance Special Version',
							'Just Dance Kids', 'Just Dance Kids 2', 'Just Dance Kids 2014',
							'Just Dance: Disney Party', 'Just Dance: Disney Party 2',
							'Just Dance: Greatest Hits',
							'Just Dance: Summer Party', 'Just Dance Now', 'Just Dance Unlimited']
					# Just Dance é o ultimo jogo a ser inserido... RISCO neste!!! pode nao ser o 1.º JD.... pq no titulo podem nao especificar qual é a versao
					# quem nao quiser saber de qual é a edicao, simplesmente nao aplica o filtro, e vê tudo.

					plataform = ['Wii', 'Wii U', 'PlayStation 3', 'PlayStation 4', 'PlayStation 5', 'Xbox 360', 'Xbox One', 'Xbox Series X/S', 'iOS', 'Android', 'Nintendo Switch', 'Microsoft Windows', 'Stadia']
					# tratar abreviaturas das consolas... ps3 -> playstation 3 ou no if... meter as duas hipoteses...

					if("just dance now" in title):
						print("JD NOW")
						# vai dar duplicado .... guardar numa lista e ir vendo se está? assim evita-se insercoes...
						query = "insert into youtube values('Youtube','"+str(channelID[row])+"', '"+channel[row]+"', '"+str(videoID[row])+"','"+title+"','"+str(dateVideo)+"', '"+str(views[row])+"', '"+str(likesVideo[row])+"', '"+str(dislikesVideo[row])+"', '"+str(totalCommentsVideo[row])+"')"
						#insertToTable(query)
						# este nao...
						query = "insert into opinion values('"+str(commentID[row])+"', '"+str(t)+"', '"+str(likes[row])+"', '"+str(dateComment)+"', True, 'Just Dance Now', '"+str(polarity)+"', '"+str(videoID[row])+"')"
						#insertToTable(query)
					else:
						#print("JD")
						query = "insert into youtube values('Youtube','"+str(channelID[row])+"', '"+channel[row]+"', '"+str(videoID[row])+"','"+title+"','"+str(dateVideo)+"', '"+str(views[row])+"', '"+str(likesVideo[row])+"', '"+str(dislikesVideo[row])+"', '"+str(totalCommentsVideo[row])+"')"
						#insertToTable(query)
						query = "insert into opinion values('"+str(commentID[row])+"', '"+str(t)+"', '"+str(likes[row])+"', '"+str(dateComment)+"', 'True', 'Just Dance', '"+str(polarity)+"', '"+str(videoID[row])+"')"
						#insertToTable(query)
						
					DictResult = annotate(str(t),str(polarity)) 
					#print("> ",DictResult)
					if(bool(DictResult)):
						#print("		######################################## true")
						#print("> ",result[0])
						#print(">>",result[1])
						print(DictResult)
						for field in DictResult.keys():
							#print("FIELD = ", field)
							for concept in DictResult[field]:
								#print(field + "->"+concept)
								#print(concept)
								if (field == "Usability"):
									query = "insert into opinion_usability values('"+str(commentID[row])+"', '"+str(concept)+"')"
									#print(query)
									#insertToTable(query)
								elif (field == "UX"):
									query = "insert into opinion_ux values('"+str(commentID[row])+"', '"+str(concept)+"')"
									#print(query)
									#insertToTable(query)
								elif (field == "Health"):
									query = "insert into opinion_health values('"+str(commentID[row])+"', '"+str(concept)+"')"
									#print(query)
								#insertToTable(query)
						#query = "insert into ux values('"+termo+"')"
						#insertToTable(query)

						#print(views[row])
						#print(likesVideo[row])
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










