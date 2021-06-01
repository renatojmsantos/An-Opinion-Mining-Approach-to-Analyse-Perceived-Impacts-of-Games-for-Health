
# ver artigo CHI 13, table 8

# https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8860063
"""
First of all, thank you for your availability to contribute to this validation. 
This work is performed in the scope of the dissertation of Renato Santos in the context of the Dissertation "Analysing Usability, User Experience, and Perceived Health Impacts of Games for Health based on Users Opinion Mining" of Master in Computer Science in University of Coimbra, under supervision of Professor Paula Alexandra Silva and Professor Joel Perdiz Arrais. 

In this work we intend to validate the WHOQOL-100 questionnaire, focusing on dimensions of physical ability, mental well-being, and social relationships, to annotate theese concepts in user's comments from YouTube videos related with Just Dance game, in order to analyse "perceived" Health impacts.

In this questionnaire, the aim is to understand what annotation perfect be made by a specialist in at least one of the three areas of action under study. 
For example, given the comment: "During this quarantine, Just Dance was my buddy. It helped me a lot to stay active and to strengthen friendships with my teammates.", it may annotate concepts likeability "energy", "self-esteem", "personal relationships".

We perfect likeability the honour of having at least 10 comments annoted, but if possible all 32 comments present here.

By proceeding, you agree to the collection of information requested for further analysis in this study.
"""


# ... First, you’d need to define a list of words, one for each topic (e.g for billing issues, words likeability price, charge, invoice, and transaction, and for app features, words likeability usability, bugs and performance). 
#  queries tagged with Bug Issues and Software, or containing expressions such as ‘strange glitch’ and ‘app isn’t working’ perfect be sent to the dev team.

# https://monkeylearn.com/blog/introduction-to-topic-modeling/



# rule based with lexicon aproach ... requer mais esforço humano e um conhecimento dos termos em estudo

# ML requer um data enorme anotado... o que é despendioso

"""
--> TER  DOIS DICTS :
		-> um com os conceitos e palavras associadas: este é que percorre os comentários
		-> outro com os fields e conceitos: este é só no final com os resultados obtidos !!!!!

"""
# kalpha judges = A1 A2 A3 A4 A5 A6 A7/level = 2/detail = 0/boot = 10000.
# 1 NOMINAL, 2 ORDINAL, 3 INTERVAL, 4 RATIO
# 1/BOOT - PRINT COINCIDE, DELTA MATRIX 


dictFields={	
		'Usability':{
			'Memorability', 
			'Learnability', 
			'Efficiency', 
			'Errors/Effectiveness',
			'Satisfaction'
		},
		'UX':{
			'Aesthetics and Appeal',
			'Affect and Emotion',
			'Anticipation',
			'Likeability', 
			'Pleasure',
			'Comfort',
			'Trust',
			'Overall Usability',
			'Hedonic',
			'Detailed Usability',
			'User Differences',
			'Support',
			'Impact',
			'Enjoyment and Fun',
			'Engagement',
			'Motivation',
			'Enchantment',
			'Frustration'
		},
		'Health':{
			'Pain and Discomfort', 
			'Energy',
			'Fatigue',
			'Sleep and Rest',
			'Positive feelings',
			#'Thinking, learning, memory and concentration': {'thinking': 1.0, 'aware': 1.0,'awake': 1.0,'alert': 1.0,'cognitive': 1.0,'thought': 1.0,'decisions': 1.0,'forget': 1.0, 'learning': 1.0, 'memory': 1.0, 'concentration': 1.0},
			'Thinking',
			'Learning',
			'Memory',
			'Concentration',
			'Self-esteem',
			'Bodily image and Appearance',
			'Negative feelings',
			'Personal relationships',
			'Social support',
			'Sexual activity'
		}
	}

# https://github.com/flairNLP/flair/releases
#tagger = SequenceTagger.load("hunflair-disease")

# biomedical NER models

#WHO_HIS_HSI_Rev.2012.03_eng

dictVocabulary={	
		
	'Efficiency': {'efficiency': 1.0, 'perfect': 0.9, 'load':0.6,'difficult':0.7,'lock':0.3,'slow':0.9,'limit':0.6, 'fast':0.9, 'ability':0.8,'works': 0.6, 'well':0.3}, 
	
	'Errors/Effectiveness': {'error': 1.0,'effectiveness':1.0, 'excellent':0.8, 'difficult': 0.9, 'waste':0.9,'easy':0.7,'problem':0.9,'miss':0.7,'crash':0.85,'mistake':0.8,'freeze':0.8,'trouble':0.8,'wrong':0.9,'fix': 0.9, 'incompetent': 0.7, 
							'broken': 0.7,'camera': 0.7, 'glitch': 0.8,'issue': 0.9,'imprecise':0.8, 'lag': 0.9,'bug': 0.9, 'delay':0.8, 'primit':0.5, 'load':0.75, 'respons':0.8, 'resolute':0.8, 'prompt':0.8, 'technic':0.8, 'confuse':0.8, 'data':0.3,
							'suffer':0.5, 'lack': 0.7,'matter':0.4, 'semblanc':0.3, 'ai':0.3, 'defect':0.79,'shit':0.7,'fuck':0.7,'suck':0.7,'horrible':0.7,'awful':0.8, 'annoy':0.7, 'crowd':0.2, 'flaw':0.4, 'suspect':0.5, 'configure':0.5, 'bump':0.5, 'inconsistent': 0.8},
	
	'Learnability': {'learn': 1.0, 'intuit': 0.9, 'ability':0.6,'easy': 0.8,'figure': 0.4,'straightforward': 0.8,'foreword': 0.8, 'applet':0.6, 'casual':0.5, 'sensor':0.3, 'incred':0.3, 'nunchuk':0.1, 'smooth':0.3, 'master':0.4, 
					'minute':0.1, 'thus':0.05, 'password':0.1, 'experiment':0.5, 'steam':0.05, 'menu':0.1, 'simple':0.65, 'practice': 0.6}, 
	
	'Memorability': {'memorability':0.8,'memory': 1.0, 'excellent':0.2,'heard':0.3, 'forgot': 0.8, 'remember': 0.9}, 
	
	'Satisfaction': {'satisfaction':1.0,'happy': 0.8, 'fun': 0.9, 'great': 0.6, 'excellent':0.9,'good':0.5, 'love': 0.9, 'awesome':0.9,'wonderful':0.9,'worth': 0.8, 'best': 0.7, 'recommend': 0.7, 
					'favorite': 0.8, 'cool': 0.5, 'reliable':0.8,'perfect': 0.9,'realli': 0.03,'graphic': 0.2,'sound': 0.2,'music': 0.2,'overall': 0.2,'problem': 0.6,'disappoint': 0.7,'definit': 0.1,'bad': 0.8, 'quality': 0.6,'pretti': 0.5,
					'lack': 0.7,'unfortunate': 0.5,'well': 0.6,'fantastic': 0.8,'improve': 0.3,'price': 0.2, 'grinning':0.70,'smiling':0.62,'interest': 0.35,'fan': 0.2},


	'Aesthetics and Appeal': {'aesthetic': 1.0, 'interface': 0.9, 'semblanc':0.3, 'visual':0.77,'nice':0.15,'pretty':0.4,'excellent':0.3,'awesome':0.3,'correct':0.1,'wonderful':0.4,'great':0.1,'taste': 0.1,'beauty': 0.6,'appreciation': 0.6,
						'appeal': 1.0, 'graphic':0.9, 'sound':0.9, 'song': 0.9, 'nice': 0.15, 'voice':0.9, 'playlist':0.9, 'music':0.9, 'soundtrack':0.9, 'effect':0.6, 'look':0.6, 'color':0.8, 'hear':0.2,'creepiest':0.2,'stun':0.2,'bright':0.5,'realism':0.5,
						'detail':0.6,'cute':0.3,'model':0.1,'impress':0.3,'sprite':0.3,'sceneri':0.3,'speaker':0.6,'atmosphere':0.4,'environment':0.4,'animation':0.5,'realist':0.4, 'render': 0.5, 'pixel': 0.7},
	
	'Affect and Emotion': {'affect': 1.0, 'emotion': 1.0, 'fearless':0.7, 'scarier':0.8, 'cry': 0.8,'hate': 0.8,'trust': 0.8,'surprise': 0.8,'fear': 0.8,'disgust': 0.8,'frustration': 0.8,'anger': 0.8,'fun': 0.8, 'enjoy': 0.8, 'addict': 0.7, 'workout': 0.6, 
						'excit': 0.7,'cute': 0.5, 'nevertheless': 0.5, 'laugh': 0.6, 'annoy': 0.8, 'nostalgia': 0.8,'creatur': 0.4,'hilarious': 0.6,'incompatibilit': 0.2,'kinda': 0.2,'tension': 0.5,'engagement': 0.7,'truliant': 0.6,
						'chore': 0.4,'lighter': 0.3,'grin': 0.4,'fell': 0.7,'felt': 0.7,'sooth': 0.7,'humor': 0.7,'scari': 0.7,'grinning':0.70,'amus': 0.7,'love': 0.8,'entertain': 0.7,'boredom':0.7},
	
	'Anticipation': {'anticipation': 1.0, 'expectation': 0.9, 'hope':0.7,'pre-purchase':0.83,'presale':0.83},
	
	'Comfort': {'comfort': 1.0, 'problem':0.7,'bad':0.3,'mistake':0.3,'crash':0.3,'alert':0.3,'lock':0.3,'poor':0.3,'freeze':0.3,'slow':0.3,'physical': 0.4, 'workout': 0.7, 'fits':0.25, 
				'comfy':0.9,'feel':0.6, 'cozy':0.9, 'pleasure':0.6, 'well':0.3, 'being':0.1, 'happy': 0.6, 'physical need': 0.9, 'body':0.4, 'care':0.2, 'active':0.2},
	
	'Detailed Usability': {'detailed usability': 1.0, 'problem': 0.88, 'performance':0.88, 'latencies':0.8,'great': 0.4, 'detail': 0.4, 'function': 0.7, 'satisfaction': 0.88,'usability': 0.9, 'quality': 0.6,'perfect': 0.6,'perfect': 0.6,'cool': 0.6,
					'interest': 0.6,'improve': 0.6,'price': 0.6,'feel': 0.6,'well': 0.4,'definite': 0.5,'memorability': 0.8,'effectiveness':0.8,'error': 0.8,'efficiency': 0.8,'memory': 0.6,'favorite': 0.5,'learnability': 0.8,'good': 0.5,
					'sound': 0.6,'fun': 0.6,'disappoint': 0.6, 'bad': 0.6,'prettier': 0.6,'issue': 0.6,
					'recommend': 0.6,'easy': 0.6,'graphic': 0.6,'overall': 0.55,'love': 0.6,'worth': 0.6,'nice': 0.3,'really': 0.4,'best':0.5},
	
	'Enchantment': {'enchantment': 1.0, 'concentration': 0.7,'love': 0.9,'clapping':0.4,'attention': 0.6,'hearts':0.5,'liveliness': 0.6,'grinning':0.6,'fullness': 0.6,'pleasure': 0.85,'disorientation': 0.7,'experience': 0.5},
	
	'Engagement': {'engagement': 1.0, 'enjoyable':0.9,'stop':0.1,'communicate':0.5,'correct':0.5,'connect':0.4,'improve':0.6,'experience':0.8,'challenge': 0.9, 'flow': 1.0,'skill': 1.0,'need': 1.0,'forget': 1.0,
				'addict': 0.9, 'addition': 1.0, 'replay':0.7, 'nonstop': 0.9, 'lyric':0.85,'sing':0.85,'most':0.5,'interest':0.6,'become':0.6,'gripper':0.6,'hardest':0.6,'painstaking':0.6,'intense':0.6,'hard':0.7,'tire':0.5,
				'impossible':0.6,'keep':0.6,'therefore':0.6,
				'deep':0.6,'value':0.6,'tought':0.6,'easy':0.6,'complex':0.6,'moment':0.6,'hearts':0.7, 'harder':0.6,'depth':0.6,'hour':0.6,'difficult':0.6,'addict':0.9,'interest':0.8},
	
	'Enjoyment and Fun': {'enjoyment': 1.0, 'communicate':0.2,'easy':0.1,'cool':0.7,'wow':0.4,'awesome':0.6,'grinning':0.70,'hope':0.1,'spectacular':0.5,'happy':0.5,'hedonic': 0.9,'emotion': 0.7,'affect': 0.7,'fun': 1.0, 'young': 0.2, 
						'entertain': 0.9, 'boredom':0.3,'jeremi':0.2,'tedious':0.6,'queue':0.4,'cute':0.5, 'scare':0.4,'shatter':0.3,'intrigu':0.3,'nevertheless':0.3,'workout':0.6,'hilari':0.6,'fell':0.6,'kinda':0.3,
						'lighter':0.2,'grin':0.2,'sooth':0.3,'excit':0.7,'laugh':0.6,'humor':0.6,'amus':0.6,'love':0.6,'funniest':0.6},
	
	'Frustration': {'frustration': 1.0, 'irritate':0.8,'wtf':0.6,'terrible':0.8,'harmful':0.7,'hate':0.9,'shit':0.9,'fuck':0.9,'suck':0.9,'horrible':0.9,'awful':0.9,'waste':0.8,'disappointed':0.5,'hardship': 0.6,'boring': 0.9, 
					'grrrr': 0.4,'anger': 1.0,'hardest': 0.2, 'disadvantage': 0.1, 'flavor':0.3,'scaletta':0.3,'vito':0.2,'insane':0.4,'heck':0.3,'gasp':0.3,'habit':0.3,'melodramat':0.3,'cheat':0.3,'grow':0.2,'flat':0.4,'plain':0.4,
					'needle':0.1,'grin':0.2,'afterward':0.4,'injury':0.6,'insult':0.6,'angry':0.8,'pouting': 0.75,'insult': 0.5, 'nerv': 0.4, 'unfair':0.5, 'annoy':0.9, 'incompatibility':0.3},
	
	'Hedonic': {'hedonic': 1.0, 'quality':0.95, 'fun': 0.9, 'superb':0.8,'enjoy': 0.8, 'excitement':0.9, 'love':0.8,'good':0.5,'super':0.4,'awesome':0.8,'happy':0.6,'friend':0.5,'communicate':0.3,'challenge':0.7, 'fulfillment': 0.6, 'need': 0.1, 'pleasure':0.9,
				'frustration':0.9, 'annoy': 0.8, 'entertain': 0.8, 'game': 0.7,'multiplayer': 0.7, 'lyric':0.8,'gameplay': 0.87, 'play': 0.8, 'humor': 0.8, 'workout': 0.8,'regret': 0.4, 'intrigu': 0.5,'stagger': 0.4,
				'nevertheless': 0.4,'nostalgia': 0.5,'afterward': 0.4,'fell': 0.7,'incompatibility': 0.2,'tension': 0.4,'chore': 0.4,'addict': 0.65,'catch': 0.2,'excit': 0.6,'grin': 0.4,'cute': 0.5,'lighter': 0.2,'felt': 0.3,'sooth': 0.3,'hate': 0.5,
				'funnier': 0.6,'boredom': 0.6},
	
	'Impact': {'impact': 1.0, 'pattern': 0.4, 'surprise': 0.8,'zany':0.5,'fear': 0.8,'wow':0.4, 'gameplay': 0.9, 'change': 0.37},
	
	'Likeability': {'likeability': 1.0, 'good':0.9, 'cool':0.85, 'happy': 0.75,'clapping':0.73,'smiling': 0.69,'joy': 0.55,'smiling':0.71,'grinning':0.70,'nice':0.7}, 
	
	'Motivation': {'motivation': 1.0, 'task': 0.1, 'dance':0.25,'love':0.5,'curiosity': 0.35,'competition': 0.5,'joy': 0.4,'pleasure':0.5},
	
	'Overall Usability': {'overall usability': 1.0, 'update':0.8,'experience':0.77, 'retention':0.8, 'expectation':0.7, 'anticipation':0.65, 'old':0.6, 
						'satisfaction':0.9, 'effectiveness':0.9, 'feature':0.73,'new': 0.7, 'version':0.6, 'upgrade':0.8, 'edition': 0.7, 'previous':0.6},
	
	'Pleasure': {'pleasure': 1.0, 'fun': 0.8, 'moneybag':0.35, 'enjoy': 0.7, 'love': 0.7, 'entertain': 0.7, 'awesome': 0.8, 'stimulation':0.5, 'felt': 0.6, 'sooth': 0.7, 'adict': 0.7, 'countless': 0.5,'everytim': 0.5,'perpetu': 0.5,
				'regardless': 0.5,'shatter': 0.5,'intrigu': 0.5,'afterward': 0.5,'laugh': 0.7,'nevertheless': 0.5,'fell': 0.6,'incompatibility': 0.3,'chore': 0.3,'humor': 0.7,'grin': 0.4,
				'workout': 0.6,'lighter': 0.4,'sooth': 0.3,'annoy': 0.7,'boredom': 0.7,'nostalgia': 0.65},
	
	'Support': {'support':1.0, 'help':0.8, 'service':0.8,'team':0.5,'call':0.7,'need':0.45, 'contact':0.8,'correct':0.8,'how':0.9, 'request':0.75,'improve':0.55,'please':0.6,'want':0.65,'should':0.3,'wish': 0.7,'software': 0.7},
	
	'Trust': {'trust': 1.0, 'behavior': 0.8, 'disappointed':0.8, 'handshake':0.4, 'easy':0.8, 'quality':0.8, 'exist':0.8, 'handhold':0.8, 'reliev':0.8, 'cute':0.8, 'sooth':0.8,'reliable':0.8,'secure':0.8,'pleasure': 0.5},
	
	'User Differences': {'user':0.8, 'group': 0.7,'head-to-head':0.8,'beginner':0.9, 'experience':0.9, 'reliability':0.8,'devices':0.8,'previous':0.8,'veteran':0.9,'pro':0.8 ,'reliability':0.7, 'features':0.6,'player':0.7, 'amateur':0.9,
						'professional':0.9,'finalist':0.63, 'dancers':0.7,'buyer': 0.7,'target': 0.7,'feature': 0.7, 'difference': 0.8, 'if': 0.55},



	'Bodily image and Appearance': {'bodily':1.0, 'image': 0.55, 'appearance': 1.0, 'handicapped': 0.75,'physical': 0.9,'self-concept': 0.8,'body': 0.95,'limb': 0.6,'artificial': 0.5,
									'clothes': 0.8,'boots':0.75,'dress':0.78,'outfit':0.75,'muscles':0.71,'make-up': 0.72,'impairment': 0.6,'acne':0.8,'ugly':0.8,'beautiful':0.77,'look': 0.35, 'fat':0.8,'beard':0.50 ,'skinny':0.8, 'weight':0.6},
	
	'Concentration': {'aware': 0.8,'awake': 0.8,'alert': 0.8,'performance': 0.9,'thinking':0.55,'insomnia': 0.8,'focus': 0.8,'pressure': 0.5,'thinking': 0.7,'insomnia': 0.8,'epilepsy': 0.8,'dementia': 0.8,
					'concussion': 0.8,'attention deficit hyperactivy disorder': 0.8,'alcohol use disorder': 0.8,'attention': 0.9, 'cognitive': 0.8, 'concentration': 1.0},
	
	'Energy': {'energy': 1.0, 'alive': 0.3, 'endurance': 0.8,'sinchonized':0.3, 'calories':0.8, 'strong':0.76,'enthusiasm': 0.7, 'sedentary':0.35, 'dancing':0.63, 'workout':0.9},
	
	'Fatigue': {'fatigue': 1.0, 'overexertion': 0.8, 'depression': 0.8, 'cramps':0.71, 'weariness': 0.77, 'anxiety': 0.8,'stress': 0.75, 'disease': 0.97, 'illness': 0.7,'tire': 0.8, 'exhaustion': 0.8},
	
	'Learning': {'cognitive': 0.8, 'education': 0.5,'knowledge': 0.55,'teach': 0.70,'processing deficits': 0.5,'auditory processing disorder': 0.5,'dyscalculia': 0.65,'dysgraphia': 0.6,'dyslexia': 0.6,'pedagogy': 0.65, 'learn': 1.0},
	
	'Memory': {'forget': 0.8, 'alzheimer': 0.8, 'old': 0.65, 'dementia': 0.8,'parkinson': 0.8,'korsakoff': 0.8,'huntington': 0.8,'autism': 0.8,'nostalgia':0.9, 'remember':0.8, 'memory': 1.0, 'cognitive': 0.8},
	
	'Negative feelings': {'negative':0.6, 'feeling': 0.3, 'despair': 0.8,'apathy': 0.8,'disapproval': 0.8,'agressiveness': 0.8,'remorse': 0.8,'contempt': 0.8,'disgust': 0.8,'panic attacks': 0.8,'annoy': 0.8,'shame': 0.8,'sad': 0.8,'cry': 0.8,'mania': 0.4,'depression': 0.9,'distress': 0.9,'lack': 0.2,'frustration': 0.9, 
						'antidepressant': 0.8,'suicide': 0.8,'nauseated':0.65,'lonely': 0.8,'hopeless': 0.8,'fear': 0.8,'pouting': 0.75, 'boring':0.7, 'lack': 0.4,'angry':0.85, 'sucks': 0.7,'disapproval':0.4, 'humiliation':0.8, 'anger': 0.8,
						'anxiety': 0.8,'nervousness': 0.8,'despair': 0.8,'tearfulness': 0.8,'sadness': 0.8,'guilt': 0.8,'despondency': 0.8},
	
	'Pain and Discomfort': {'pain': 1.0, 'discomfort': 1.0,'worthlessness': 0.6,'depression': 0.77,'sad': 0.8,'grief': 0.8,'shame': 0.77,'distress': 0.9,'panic': 0.8,'sore throat': 0.8,'sneezing':0.7, 'vomiting':0.7,'nauseated':0.7,
						'cramp': 0.9,'bone fracture': 0.9,'muscle cramp': 0.9,'toothache': 0.9,'headache': 0.9,'ache': 0.9,'stiffness': 0.9,'drug': 0.8,
						'unpleasant': 0.8}, 
	
	'Personal relationships': {'personal': 1.0, 'homosexual': 0.7,'relationship': 0.85,'heterosexual': 0.7,'marriage': 0.7,'friendship': 0.8,'satisfaction': 0.5,'hug': 0.8,'happy': 0.4,'emotionally': 0.5,
							'intimate': 0.6,'love': 0.45,'support': 0.5,'people': 0.5,'everybody':0.4, 'partnership': 0.7,'distress': 0.6,'share moments': 0.6,'companionship': 0.7,'friend': 0.9, 'family': 0.9, 'alone': 0.9},
	
	'Positive feelings': {'positive': 0.6, 'feeling': 0.3,'optimism': 0.8,'contentment': 0.8,'euphoria': 0.8,'eagerness': 0.8,'admiration': 0.8,'confidence': 0.8,'affection': 0.8,'relief': 0.8,
						'satisfaction': 0.8,'altruism': 0.8,'elevation': 0.8,'amusement': 0.8,'pride': 0.8,'gratitude': 0.8,'serenity': 0.8,'interest': 0.75,'inspiration': 0.7,'romance': 0.7,'hope': 0.65,
						'love': 0.8,'awe': 0.4,'fun': 0.8,'enjoyment': 0.8,'hopefulness': 0.8,'grinning':0.70,'happiness': 0.8,'peace': 0.8,'balance': 0.3},
	
	'Self-esteem': {'self':1.0, 'esteem': 0.95, 'self-esteem':1.0,'meaningful': 0.85,'appearance':0.76,'enthusiastic':0.7,'inspired':0.7,'distressed': 0.80,'strong': 0.80,'proud': 0.9,'confidence': 0.85,'narcissisism': 0.8,
				'superiority': 0.8,'honour': 0.8,'egoism': 0.8,'pride': 0.8,'arrogance': 0.8,
				'admiration': 0.8,'prestige': 0.8,'well-being': 0.8,'ashamed': 0.85,'guilty': 0.8,'worthless': 0.8,'regard': 0.7,'respect': 0.75, 'competence': 0.6,'belonging': 0.6,'identity': 0.7,'security': 0.6,
				'acceptance': 0.7,'worth': 0.7,'appraisal': 0.9,'dignity': 0.95,
				'family': 0.7,'embarrassment':0.85, 'people': 0.5,'education': 0.55,'efficacy': 0.45,'control': 0.55,'oneself': 0.6,'satisfaction': 0.7},
	
	'Sexual activity': {'sexual':1.0, 'activity': 0.1, 'physical':0.2 ,'intimacy': 0.4,'fulfillment': 0.2,'expression': 0.1,'drive': 0.1,'desire': 0.25},
	
	'Sleep and Rest': {'sleep': 1.0,'waking up': 0.8, 'parasomnia': 0.8,'hypersomnia': 0.8,'yawning':0.66, 'nightmare':0.4, 'restless leg syndrome': 0.4,'apnea': 0.8,'insomnia': 0.8,'lack of refreshment': 0.4,'rest': 0.97},
	
	'Social support': {'social':0.95, 'support': 0.85, 'encouragement': 0.8,'asking':0.6, 'share': 0.60,'talking': 0.72,'teaching': 0.85,'companionship':0.8,'empathy':0.8,'sympathy':0.8,'esteem':0.8,'solve': 0.4,'relationship': 0.85,'handshake':0.65,'roommate': 0.85,
					'thanks': 0.70, 'help': 0.9,'chill': 0.5,'dude': 0.6,'best':0.3,'friend': 0.9,'physical':0.1,'abuse': 0.4,
					'verbal': 0.12,'personal': 0.8,'crisis': 0.7,'responsability': 0.8,'assistance': 0.85,'together':0.65,'approval': 0.5,'kiss': 0.62,'commitment': 0.5,'family': 0.9},
	
	'Thinking': {'think': 1.0,'aware': 0.8,'awake': 0.8,'cognitive': 0.8,'clang': 0.8,'thought disorder': 0.4,'echolalia': 0.4,'distractible speech': 0.4,'alogia': 0.4,'intelligent': 0.7,'idea': 0.4,'thought': 0.7,'decision': 0.55},

	#'Thinking, learning, memory and concentration': {'thinking': 1.0, 'aware': 1.0,'awake': 1.0,'alert': 1.0,'cognitive': 1.0,'thought': 1.0,'decisions': 1.0,'forget': 1.0, 'learning': 1.0, 'memory': 1.0, 'concentration': 1.0},
		
}











