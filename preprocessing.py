import pandas as pd
import re   # regular expression
import regex
import demoji
import numpy as np
import time
import emoji
import unicodedata

from nltk.corpus import wordnet
from langdetect import detect
from langdetect import DetectorFactory
from emoji.unicode_codes import UNICODE_EMOJI
from textblob import TextBlob, Word
from flair.data import Sentence
from flair.models import SequenceTagger

tagger = SequenceTagger.load("ner") 


DetectorFactory.seed = 0


def isEnglish(text):
	if(len(text.split()) < 5):
		try:
			lang = TextBlob(text)
			if(lang.detect_language() =="en"):
				return True
			else:
				return False
		except Exception as e:
			print("isEnglish - ", e)
			try:
				language = detect(text)
				if (language == "en"):
					return True
				else:
					return False
			except Exception as e:
				print("isEnglish - ", e)
	else:
		try:
			language = detect(text)
			if (language == "en"):
				return True
			else:
				return False
		except Exception as e:
			print("isEnglish - ", e)
	
	return False
	

def emojiToCLDRshortName(text):
	try:
		has_emoji = bool(emoji.get_emoji_regexp().search(text))
		if (has_emoji):
			emoji_chars = emoji.EMOJI_ALIAS_UNICODE_ENGLISH.values()
			def _emoji(char):
				if char in emoji_chars:
					return unicodedata.name(char) + " "
			return ''.join(_emoji(char) or char for char in text)
		else:
			return text
	except Exception as e:
		print("Emoji convert - ", e)


def clearText(text):
	try:
		# contractions
		text = contractions(str(text))
		#acronyms
		text = slangs(str(text))
		# emojis to cldr
		text = str(emojiToCLDRshortName(str(text)))
		# remove URLs
		text = re.sub('https?://[A-Za-z0-9./?&=_]+','',text)
		# hashtags
		text = re.sub('#[A-Za-z0-9]+','',text)
		# mentions
		text = re.sub('@[A-Za-z0-9._-]+','',text)
		# to lower
		text = text.lower()
		# remove pontuation
		text = re.sub(r"[^\w\s]","",text)
		#remove white spaces
		text = " ".join(text.strip().split())
		text = re.sub(r"[\W\s]"," ",text)
		text = re.sub("\n","",text)
	except Exception as e:
		print("clearText - ", e)

	return text

def contractions(text):
	# https://gist.github.com/nealrs/96342d8231b75cf4bb82
	# https://en.wikipedia.org/wiki/Wikipedia:List_of_English_contractions

	cDict = {
	  "ain't": "am not",
	  "aren't": "are not",
	  "can't": "cannot",
	  "can't've": "cannot have",
	  "'cause": "because",
	  "could've": "could have",
	  "couldn't": "could not",
	  "couldn't've": "could not have",
	  "didn't": "did not",
	  "doesn't": "does not",
	  "don't": "do not",
	  "hadn't": "had not",
	  "hadn't've": "had not have",
	  "hasn't": "has not",
	  "haven't": "have not",
	  "he'd": "he would",
	  "he'd've": "he would have",
	  "he'll": "he will",
	  "he'll've": "he will have",
	  "he's": "he is",
	  "how'd": "how did",
	  "how'd'y": "how do you",
	  "how'll": "how will",
	  "how's": "how is",
	  "I'd": "I would",
	  "I'd've": "I would have",
	  "I'll": "I will",
	  "I'll've": "I will have",
	  "I'm": "I am",
	  "I've": "I have",
	  "isn't": "is not",
	  "it'd": "it had",
	  "it'd've": "it would have",
	  "it'll": "it will",
	  "it'll've": "it will have",
	  "it's": "it is",
	  "let's": "let us",
	  "ma'am": "madam",
	  "mayn't": "may not",
	  "might've": "might have",
	  "mightn't": "might not",
	  "mightn't've": "might not have",
	  "must've": "must have",
	  "mustn't": "must not",
	  "mustn't've": "must not have",
	  "needn't": "need not",
	  "needn't've": "need not have",
	  "o'clock": "of the clock",
	  "oughtn't": "ought not",
	  "oughtn't've": "ought not have",
	  "shan't": "shall not",
	  "sha'n't": "shall not",
	  "shan't've": "shall not have",
	  "she'd": "she would",
	  "she'd've": "she would have",
	  "she'll": "she will",
	  "she'll've": "she will have",
	  "she's": "she is",
	  "should've": "should have",
	  "shouldn't": "should not",
	  "shouldn't've": "should not have",
	  "so've": "so have",
	  "so's": "so is",
	  "that'd": "that would",
	  "that'd've": "that would have",
	  "that's": "that is",
	  "thats": "that is",
	  "there'd": "there had",
	  "there'd've": "there would have",
	  "there's": "there is",
	  "they'd": "they would",
	  "they'd've": "they would have",
	  "they'll": "they will",
	  "they'll've": "they will have",
	  "they're": "they are",
	  "they've": "they have",
	  "to've": "to have",
	  "wasn't": "was not",
	  "we'd": "we had",
	  "we'd've": "we would have",
	  "we'll": "we will",
	  "we'll've": "we will have",
	  "we're": "we are",
	  "we've": "we have",
	  "weren't": "were not",
	  "what'll": "what will",
	  "what'll've": "what will have",
	  "what're": "what are",
	  "what's": "what is",
	  "what've": "what have",
	  "when's": "when is",
	  "when've": "when have",
	  "where'd": "where did",
	  "where's": "where is",
	  "where've": "where have",
	  "who'll": "who will",
	  "who'll've": "who will have",
	  "who's": "who is",
	  "who've": "who have",
	  "why's": "why is",
	  "why've": "why have",
	  "will've": "will have",
	  "won't": "will not",
	  "won't've": "will not have",
	  "would've": "would have",
	  "wouldn't": "would not",
	  "wouldn't've": "would not have",
	  "y'all": "you all",
	  "y'alls": "you alls",
	  "y'all'd": "you all would",
	  "y'all'd've": "you all would have",
	  "y'all're": "you all are",
	  "y'all've": "you all have",
	  "you'd": "you had",
	  "you'd've": "you would have",
	  "you'll": "you you will",
	  "you'll've": "you you will have",
	  "you're": "you are",
	  "you've": "you have"
	}
	try:
		c_re = re.compile('(%s)' % '|'.join(cDict.keys()))

		def expandContractions(text, c_re=c_re):
			def replace(match):
				return cDict[match.group(0)]
			return c_re.sub(replace, text)
		
		text = expandContractions(text.lower())
		return text
	except Exception as e:
		print("contractions", e)


def caracteresRepetidos(text):
	# https://www.nltk.org/_modules/nltk/tokenize/casual.html#reduce_lengthening
	try:
		if (len(text) > 1):
			pattern = regex.compile(r"(.)\1{2,}")
			return pattern.sub(r"\1\1\1", text)
		else:
			return text
	except Exception as e:
		print("caracteresRepetidos - ", e)


def spellCorrection(text):
	# NER - Name Entity Reconection 
	# se for NER nao corrigir... person name, locations, organizations, other names...
	try:
		# Flair NER works based on context
		sentence = Sentence(text)
		tagger.predict(sentence)

		d = sentence.to_dict(tag_type='ner')
		if (d.get('entities') is not None):
			pass
		else:
			text = TextBlob(text).correct()
	except Exception as e:
		print("spellCorrection - ", e)
	
	return text


def slangs(text):
	try:
		file = 'acronimos.csv'
		acron = pd.read_csv(file,lineterminator='\n',encoding='utf-8')

		slang = acron['slang']
		complete = acron['complete']
		row = 0

		for s in slang:
			if(slang[row] in text.lower().strip().split()):
				text = text.lower()
				text = text.replace(slang[row],str(complete[row].strip()))
			else:
				row+=1
		return text
	except IOError as e:
		print(e)
	except FileNotFoundError:
		print("File not found...", file)
	except Exception as ex:
		print("slangs...", ex)
	
	#return text

def runPreprocessing(t):
	
	if(len(t) > 3 and len(t) < 9999):
		if(isEnglish(str(t))):
			t = clearText(t)
			t = caracteresRepetidos(t)

			if(isEnglish(str(t))):
				t = spellCorrection(t) 
				if (len(t.split()) > 3 and isEnglish(str(t))): 
					return t
	return "None"




