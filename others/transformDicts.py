
from vocabulary import *
from nrclex import NRCLex
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import re 

from textblob import TextBlob, Word

# to get dicitionary with lemmas words

def pos_tagger(nltk_tag):
		if nltk_tag.startswith('J'):
			return wordnet.ADJ
		elif nltk_tag.startswith('V'):
			return wordnet.VERB
		elif nltk_tag.startswith('N'):
			return wordnet.NOUN
		else:          
			return None

def getDictLemmas():

	dictLemmas = {}
	dictStem = {}
	lemmatizer = WordNetLemmatizer()
	sno = nltk.stem.SnowballStemmer('english') 

	for items in dictVocabulary.items():
		concept = items[0]
		pals = items[1]
		print("\n>",concept)
		
		for pal,prob in pals.items():
			
			pos_tagged = nltk.pos_tag([pal])
			
			wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))
			for word, tag in wordnet_tagged:
				if (tag is not None):
					keyword = lemmatizer.lemmatize(word, tag)

			if(pal!=keyword):
				if keyword not in dictLemmas.keys():
					dictLemmas[keyword] = prob
				print(">"+pal+"--->"+keyword)
				print(keyword, prob)
			else:
				if pal not in dictLemmas.keys():
					dictLemmas[pal] = prob

	#print(dictLemmas)

getDictLemmas()

