
from preprocessing import *
from connectDB import *
import pandas as pd

# ver artigo CHI 13, table 8
dict={	'Usability':{
			'Memorability': {'memory': 1.0, 'forgot': 0.6}, 
			'Learnability': {'learnability': 1.0, 'learn': 1.0, 'intuit': 1.0, 'easier': 1.0,'figur': 0.8,'straightforward': 0.8,'foreword': 0.8, 'practic': 0.6}, 
			'Efficiency': {'efficiency': 1.0, 'perfect': 0.9}, 
			'Errors/Effectiveness': {'errors': 1.0,'effectiveness':1.0, 'fix': 0.8,'problem':0.5, 'camera': 0.7, 'glitch': 0.8,'issu': 0.8,'lag': 0.8,'bug': 0.8, 'inconsist': 0.8},
			'Satisfaction': {'happy': 1.0, 'fun': 1.0, 'great': 1.0, 'love': 1.0, 'worth': 1.0, 'nice': 1.0, 'best': 1.0, 'recommend': 1.0, 'disappoint': 0.8, 'good': 0.8, 'favorite': 0.8, 'cool': 0.8, 'perfect': 1.0}
		},
		'UX':{
			'Likeability': {'likeability': 1.0, 'like':0.9}, 
			'Pleasure': {'pleasure': 1.0, 'fun': 0.7, 'enjoy': 0.7, 'love': 0.7, 'entertain': 0.7, 'awesome': 0.8, 'stimulation':0.7, 'felt': 0.7, 'sooth': 0.7, 'adict': 0.7, 'nostalgia': 0.7},
			'Comfort': {'comfort': 1.0, 'physical': 0.7},
			'Trust': {'trust': 1.0, 'behavior': 0.8},
			'Anticipation': {'anticipation': 1.0, 'expectation': 1.0},
			'Overall Usability': {'overall usability': 1.0, 'new version': 0.8, 'upgrade':0.8, 'edition': 0.8, 'previous edition'},
			'Hedonic': {'hedonic': 1.0, 'fun': 0.8, 'enjoy': 0.8, 'frustrat': 0.8, 'fulfillment': 0.9, 'needs': 0.8, 'pleasure':0.7,'enjoyment':0.7,'frustration':0.7, 'annoy': 0.8, 'entertain': 0.8, 'game': 0.8,'multiplayer': 0.8, 'gaming': 0.8, 'gameplay': 0.8, 'play': 0.8, 'humor': 0.8, 'workout': 0.8, 'nostalgia': 0.6},
			'Detailed Usability': {'detailed usability': 1.0, 'great': 0.7, 'details': 0.9, 'functions': 0.9, 'satisfaction': 0.7,'usability': 0.7, 'best':0.7, 'problem': 0.7},
			'User Differences': {'user differences': 1.0,'user group': 0.7,'group': 0.7,'buyers': 0.7,'target': 0.7,'features': 0.7, 'differences': 0.7, 'if you': 0.6},
			'Support': {'support':1.0, 'help':0.8, 'wish': 0.7,'software': 0.7,},
			'Impact': {'impact': 1.0, 'pattern': 0.7},
			'Affect and Emotion': {'affect': 1.0, 'emotion': 1.0, 'frustration': 0.7,'fun': 0.8, 'enjoy': 0.8, 'excit': 0.8, 'cute': 0.8, 'nevertheless': 0.8, 'laugh': 0.8, 'annoy': 0.8},
			'Enjoyment and Fun': {'joy':0.9, 'enjoyment': 1.0, 'hedonic': 1.0,'emotion': 1.0,'affect': 1.0,'fun': 1.0, 'entertain': 0.9},
			'Aesthetics and Appeal': {'aesthetics': 1.0, 'taste': 1.0,'beauty': 1.0,'appreciation': 1.0,'appeal': 1.0, 'graphic':0.9, 'sound':0.9, 'song': 0.9, 'voice':0.9, 'playlist':0.9, 'music':0.9, 'soundtrack':0.9, 'effect':0.8, 'look':0.8, 'color':0.8, 'visual': 0.8, 'detail': 0.6, 'render': 0.5, 'pixel': 0.5},
			'Engagement': {'engagement': 1.0, 'challeng': 0.9, 'flow': 1.0,'skills': 1.0,'needs': 1.0,'forget': 1.0,'engaged': 1.0,'addict': 0.9, 'addition': 1.0, 'replay':0.7, 'nonstop': 0.9, 'interest':0.7},
			'Motivation': {'motivation': 1.0, 'task': 1.0},
			'Enchantment': {'enchantment': 1.0, 'concentration': 1.0,'attention': 1.0,'liveliness': 1.0,'fullness': 1.0,'pleasure': 1.0,'disorientation': 1.0,'experience': 1.0},
			'Frustration': {'frustration': 1.0, 'hardship': 1.0,'boring': 0.8, 'hardest': 0.7, 'insult': 0.7, 'injuri': 0.7, 'nerv': 0.7, 'unfair':0.7, 'cheat':0.7, 'annoy':0.7, 'incompatibilit':0.7},
		},
		'Health':{
			'Pain and discomfort': {'pain': 1.0, 'distressing': 1.0,'unpleasant': 1.0,'discomfort': 1.0}, 
			'Energy': {'energy': 1.0, 'alive': 1.0, 'endurance': 1.0,'enthusiasm': 0.9 },
			'Fatigue': {'fatigue': 1.0, 'exhaustion': 0.9},
			'Sleep and rest': {'sleep': 1.0,'waking up': 1.0, 'refreshment': 1.0,'rest': 1.0},
			'Positive feelings': {'positive feelings': 1.0, 'enjoyment': 1.0,'joy': 1.0,'hopefulness': 1.0,'happiness': 1.0,'peace': 1.0,'balance': 1.0,'contentment': 1.0},
			'Thinking, learning, memory and concentration': {'thinking': 1.0, 'aware': 1.0,'awake': 1.0,'alert': 1.0,'cognitive': 1.0,'thought': 1.0,'decisions': 1.0,'forget': 1.0, 'learning': 1.0, 'memory': 1.0, 'concentration': 1.0},
			'Self-esteem': {'self-esteem': 1.0, 'meaningful': 1.0,'self-acceptance': 1.0,'dignity': 1.0,'family': 1.0,'people': 1.0,'education': 1.0,'control': 1.0,'oneself': 1.0,'satisfaction': 1.0},
			'Bodily image and appearance': {'bodily image': 1.0, 'handicapped': 1.0,'physical handicapped': 1.0,'physical': 1.0,'body image': 1.0,'limbs': 1.0,'artificial limbs': 1.0,'clothing': 1.0,'make-up': 1.0,'impairments': 1.0,'looks': 1.0,'appearance': 0.9, 'body': 0.8},
			'Negative feelings': {'negative feelings': 1.0, 'lack': 1.0,'anxiety': 1.0,'nervousness': 1.0,'despair': 1.0,'tearfulness': 1.0,'sadness': 1.0,'guilt': 1.0,'despondency': 1.0},
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

def annotate(text):
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
			for p in pals.items():
				pal = p[0]
				probalidade = p[1]
				#print("  ",pal,probalidade)
				if (pal in text):
					#print(pal, termo, chave)
					#r = []
					#r.append(termo)
					#r.append(chave)
					#return r
					return (termo, chave)
				else:
					continue

#print(comments)

#print(comments[0])

def executeAnnotation():
	row = 0
	for t in comments: #t in comments:
		t = runPreprocessing(t)
		if (t != "None"):
			# print texto tratado e valido
			#print(">>",t) 
			#sentiment analysis
			try:
				text = TextBlob(str(t))
				#print(text.sentiment)
				#print(text.sentiment.polarity, text.sentiment.subjectivity)
				if text.sentiment.polarity < 0:
					polarity="Negative"
					#print(">>", polarity)
				elif(text.sentiment.polarity > 0):
					polarity="Positive"
					#print(">>", polarity)
				else:
					polarity="Neutral"
					#print(">>", polarity)
				#subjectivity = text.sentiment.subjectivity
				#print(subjectivity)

				#print(timestampComment[row])
				#'2014-06-01T00:00:00Z'
				
				try:
					dateComment = timestampComment[row]
					dateVideo = videoPublishedAt[row]
					dateComment = re.sub('T[0-9:Z]+','',dateComment)
					dateVideo = re.sub('T[0-9:Z]+','',dateVideo)
				except:
					print("something wrong on convert dates...")

				title = videoTitle[row]
				title = demoji(title)
				title = re.sub('&quot;+','',title)
				title = title.lower()


				#print(title)
				#https://en.wikipedia.org/wiki/Just_Dance_(video_game_series)
				if("just dance now" in title):
					print("JD NOW")
					# vai dar duplicado .... guardar numa lista e ir vendo se está? assim evita-se insercoes...
					query = "insert into youtube values('Youtube','"+str(channelID[row])+"', '"+channel[row]+"', '"+str(videoID[row])+"','"+title+"','"+str(dateVideo)+"', '"+str(views[row])+"', '"+str(likesVideo[row])+"', '"+str(dislikesVideo[row])+"', '"+str(totalCommentsVideo[row])+"')"
					insertToTable(query)
					# este nao...
					query = "insert into opinion values('"+str(commentID[row])+"', '"+str(t)+"', '"+str(likes[row])+"', '"+str(dateComment)+"', True, 'Just Dance Now', '"+str(polarity)+"', '"+str(videoID[row])+"')"
					insertToTable(query)
				else:
					#print("JD")
					query = "insert into youtube values('Youtube','"+str(channelID[row])+"', '"+channel[row]+"', '"+str(videoID[row])+"','"+title+"','"+str(dateVideo)+"', '"+str(views[row])+"', '"+str(likesVideo[row])+"', '"+str(dislikesVideo[row])+"', '"+str(totalCommentsVideo[row])+"')"
					insertToTable(query)
					query = "insert into opinion values('"+str(commentID[row])+"', '"+str(t)+"', '"+str(likes[row])+"', '"+str(dateComment)+"', 'True', 'Just Dance', '"+str(polarity)+"', '"+str(videoID[row])+"')"
					insertToTable(query)
					
				result = annotate(t)
				#print(result)
				if(result is not None):
					#print("> ",result[0])
					#print(">>",result[1])
					field = result[1]
					concept = result[0]			

					if (field == "Usability"):
						query = "insert into opinion_usability values('"+str(commentID[row])+"', '"+str(concept)+"')"
						insertToTable(query)
					elif (field == "UX"):
						query = "insert into opinion_ux values('"+str(commentID[row])+"', '"+str(concept)+"')"
						insertToTable(query)
					elif (field == "Health"):
						query = "insert into opinion_health values('"+str(commentID[row])+"', '"+str(concept)+"')"
						insertToTable(query)
					#query = "insert into ux values('"+termo+"')"
					#insertToTable(query)

					#print(views[row])
					#print(likesVideo[row])
			except:
				print("something wrong.... annotate")
		row += 1
		#print(comments[2])

		#print(data['Video Title'], index = t)
		"""
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
		"""

insertTablesConceitos()
#executeAnnotation()

#connect()
"""
print("tables")
query="SELECT * FROM opinion"
t = pd.read_sql_query(query,conn)
print(t)
"""
#closeConnection()










