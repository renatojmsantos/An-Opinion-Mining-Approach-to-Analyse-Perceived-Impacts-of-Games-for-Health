

# ver artigo CHI 13, table 8
dict={	'Usability':{
			'Memorability': {'memory': 1.0, 'forgot': 0.6}, 
			'Learnability': {'learnability': 1.0, 'learn': 1.0, 'intuit': 1.0, 'easier': 1.0,'figur': 0.8,'straightforward': 0.8,'foreword': 0.8, 'practic': 0.6}, 
			'Efficiency': {'efficiency': 1.0, 'perfect': 0.9}, 
			'Errors/Effectiveness': {'errors': 1.0,'effectiveness':1.0, 'fix': 0.8,'problem':0.5, 'glitch': 0.8,'issu': 0.8,'lag': 0.8,'bug': 0.8, 'inconsist': 0.8},
			'Satisfaction': {'happy': 1.0, 'fun': 1.0, 'great': 1.0, 'love': 1.0, 'worth': 1.0, 'nice': 1.0, 'best': 1.0, 'recommend': 1.0, 'disappoint': 0.8, 'good': 0.8, 'favorite': 0.8, 'cool': 0.8, 'perfect': 1.0}
		},
		'UX':{
			'Likeability': {'likeability': 1.0, 'like':0.9}, 
			'Pleasure': {'pleasure': 1.0, 'fun': 0.7, 'enjoy': 0.7, 'love': 0.7, 'entertain': 0.7, 'felt': 0.7, 'sooth': 0.7, 'adict': 0.7, 'nostalgia': 0.7},
			'Comfort': {'comfort': 1.0},
			'Trust': {'trust': 1.0},
			'Anticipation': {'anticipation': 1.0},
			'Overall Usability': {'overall usability': 1.0},
			'Hedonic': {'hedonic': 1.0, 'fun': 0.8, 'enjoy': 0.8, 'frustrat': 0.8, 'annoy': 0.8, 'entertain': 0.8, 'humor': 0.8, 'workout': 0.8, 'nostalgia': 0.6},
			'Detailed Usability': {'detailed usability': 1.0, 'great': 0.7, 'best':0.7, 'problem': 0.7},
			'User Differences': {'user differences': 1.0},
			'Support': {"support":1.0, "help":0.8},
			'Impact': {'impact': 1.0},
			'Affect and Emotion': {'affect': 1.0, 'emotion': 1.0, 'fun': 0.8, 'enjoy': 0.8, 'excit': 0.8, 'cute': 0.8, 'nevertheless': 0.8, 'laugh': 0.8, 'annoy': 0.8},
			'Enjoyment and Fun': {'joy':0.9, 'enjoyment': 1.0, 'fun': 1.0, 'entertain': 0.9},
			'Aesthetics and Appeal': {'aesthetics': 1.0, 'appeal': 1.0, 'graphic':0.9, 'sound':0.9, 'song': 0.9, 'voice':0.9, 'playlist':0.9, 'music':0.9, 'soundtrack':0.9, 'effect':0.8, 'look':0.8, 'color':0.8, 'visual':0.8, 'detail':0.6, 'render':0.5, 'pixel':0.5},
			'Engagement': {'engagement': 1.0, 'challeng': 0.9, 'addict': 0.9, 'replay':0.7, 'nonstop': 0.9, 'interest':0.7},
			'Motivation': {'motivation': 1.0},
			'Enchantment': {'enchantment': 1.0},
			'Frustration': {'frustration': 1.0, 'boring': 0.8, 'hardest': 0.7, 'insult': 0.7, 'injuri': 0.7, 'nerv': 0.7, 'unfair':0.7, 'cheat':0.7, 'annoy':0.7, 'incompatibilit':0.7},
		},
		'QOL':{
			'Pain and discomfort': {'pain': 1.0, 'discomfort': 1.0}, 
			'Energy and fatigue': {'energy': 1.0, 'fatigue': 1.0},
			'Sleep and rest': {'sleep': 1.0, 'rest': 1.0},
			'Positive feelings': {'positive feelings': 1.0},
			'Thinking, learning, memory and concentration': {'thinking': 1.0, 'learning': 1.0, 'memory': 1.0, 'concentration': 1.0},
			'Self-esteem': {'self-esteem': 1.0},
			'Bodily image and appearance': {'bodily image': 1.0, 'appearance': 0.9, 'body': 0.8},
			'Negative feelings': {'negative feelings': 1.0},
			'Personal relationships': {'personal relationships': 1.0, 'friends': 1.0, 'family': 1.0, 'alone': 1.0},
			'Social support': {'Social support': 1.0},
			'Sexual activity': {'Sexual activity': 1.0, 'sex': 0.9}
		}
	}


#print(dict)

"""
for item in dict.items():
	print(item)

print("\n")

for i in dict:
	print(dict[i])

print("\n")
"""

for items in dict.items():
	chave = items[0]
	conceitos = items[1]
	#print("\n",chave,conceitos)
	print("\n>> ",chave)
	for vocabulario in conceitos.items():
		termo = vocabulario[0]
		pals = vocabulario[1]
		#print(termo,pals)
		print(" #", termo)
		for p in pals.items():
			pal = p[0]
			probalidade = p[1]
			print("  ",pal,probalidade)
