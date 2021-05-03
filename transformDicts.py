from annotation import * 

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

def getDictLemmas():

	dictLemmas = {}
	dictStem = {}
	lemmatizer = WordNetLemmatizer()
	sno = nltk.stem.SnowballStemmer('english') #this... fairly em vez de fairli
	#ps = nltk.stem.PorterStemmer()
	#st = nltk.stem.LancasterStemmer()
	for items in dictVocabulary.items():
		concept = items[0]
		#dictLemmas[concept] = [concept]
		pals = items[1]
		print("\n>",concept)
		#print(">>> ",pals)
		

		for pal,prob in pals.items():
			

			sb = sno.stem(pal)
			#pt = ps.stem(pal)
			#ls = st.stem(pal)
			#print(">"+pal+"--->"+sb+" | "+pt+" | "+ls)
			if(sb not in dictStem.keys()):
				dictStem[sb] = prob
			print(sb)

			#print(">",pal)
			#print(">>> ",prob)
			# processo de lematização
			#pal = word_tokenize(pal)
			
			pos_tagged = nltk.pos_tag([pal])
			
			#print(pos_tagged)
			wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))
			#print(wordnet_tagged)
			#keyword = []
			for word, tag in wordnet_tagged:
				if (tag is not None):
					keyword = lemmatizer.lemmatize(word, tag)

			if(pal!=keyword):
				if keyword not in dictLemmas.keys():
					dictLemmas[keyword] = prob
				#print(">"+pal+"--->"+keyword)
				#print(keyword, prob)
				#dictLemmas[keyword].append(prob)
			else:
				if pal not in dictLemmas.keys():
					dictLemmas[pal] = prob
				#print(pal, prob)
				#dictLemmas[pal].append(prob)
			#print(pals[pal])
			#pal = keyword
			#print(pals)
			#dictVocabulary[pals] = [keyword]
			#print(dictVocabulary[concept])

			

	#print(dictLemmas)
	#for k,v in dictLemmas.items():
	#	print(k)
	#	print(v)
	#	print("\n")

	#print(dictLemmas)

getDictLemmas()



