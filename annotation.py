
#\item \textbf{Usability}: Memorability, Learnability, Efficiency, Errors/Effectiveness, Satisfaction; 
#\item \textbf{User Experience (UX)}: Likeability, Pleasure, Comfort, Trust, Anticipation, Overall Usability, Hedonic, Detailed usability, User Differences, 
	#Support, Impact, Affect and Emotion, Enjoyment and Fun, Aesthetics and Appeal, Engagement, Motivation, Enchantment, Frustration; 
#\item \textbf{"Perceived" Impacts of \gls{qol}}: Pain and discomfort, Energy and fatigue, Sleep and rest, Positive feelings, 
		#Thinking, learning, memory and concentration, Self-esteem, Bodily image and appearance, Negative feelings, Personal relationships,
		# Social support, Sexual activity.
#\end{itemize}


dict={	'Usability':{
			'Memorability': {'memory': 1.0, 'forgot': 0.6}, 
			'Learnability': {'learn': 1.0}, 
			'Efficiency': {'efficiency': 1.0, 'perfect': 0.9}, 
			'Errors/Effectiveness': {'errors': 1.0,'fix': 0.8}, 
			'Satisfaction': {'happy': 1.0, 'fun': 1.0}
		},
		'UX':{
			'Likeability': {'like': 1.0}, 
			'Pleasure': {'pleasure': 1.0},
			'Comfort': {'comfort': 1.0},
			'Trust': {'trust': 1.0},
			'Anticipation': {'anticipation': 1.0},
			'Overall Usability': {'overall usability': 1.0},
			'Hedonic': {'hedonic': 1.0},
			'Detailed Usability': {'detailed usability': 1.0},
			'User Differences': {'user differences': 1.0},
			'Support': {"support":1.0, "help":0.8},
			'Impact': {'impact': 1.0},
			'Affect and Emotion': {'affect': 1.0, 'emotion': 1.0},
			'Enjoyment and Fun': {'joy':0.9, 'enjoyment': 1.0, 'fun': 1.0},
			'Aesthetics and Appeal': {'aesthetics': 1.0, 'appeal': 1.0},
			'Engagement': {'engagement': 1.0},
			'Motivation': {'motivation': 1.0},
			'Enchantment': {'enchantment': 1.0},
			'Frustration': {'frustration': 1.0, 'boring': 0.8},
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
