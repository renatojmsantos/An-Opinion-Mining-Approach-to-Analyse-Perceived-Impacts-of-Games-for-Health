from nltk.corpus import wordnet
import sys

# example run: 
# > python3 inputsWordNet.py father

word = sys.argv[1]

for syn in wordnet.synsets(word):
	print("\n",syn.name())

	for l in syn.lemmas():
		if (l.antonyms()):
			print("antonimo -> "+l.antonyms()[0].name())
		else:
			print("sinonimo -> "+l.name())

	#lexical relations
	lexical = wordnet.synset(syn.name())

	
	# conceito especifico
	for s in lexical.hyponyms():
		for l in s.lemmas():
			print("hiponimo -> ", l.name())
			hyponym = l.name()
			
	for s in lexical.hypernyms():
		for l in s.lemmas():
			print("hiperonimo -> ", l.name())
			
	# parte de algo
	for s in lexical.part_meronyms():
		for l in s.lemmas():
			print("meronimo -> ", l.name())
			

