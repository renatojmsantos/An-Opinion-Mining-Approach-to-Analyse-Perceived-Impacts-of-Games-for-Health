
# ver artigo CHI 13, table 8

# https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8860063


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

# Errors/effectiveness: The number of (non-fatal) errors made by a user during completing a task.
# Efficiency: The speed or other measure of the cost while performing the task, at a given experience level.
# Satisfaction: A subjective rating of satisfaction with product use or liking of the product or features.
# Learnability: The amount of time it takes to learn to use the system, how difficult it is for a first time user or development over time.
# Memorability: How well users retain information gained about or through the system.

dictVocabulary={	
		
	'Efficiency': {'efficiency': 1.0, 'perfect': 0.65,'speed':0.7, 'load':0.8,'useful':0.7,'performance':0.7, 'experience':0.65,'difficult':0.75,'lock':0.5,'prompt':0.8,'slow':0.9,'limit':0.7, 'fast':0.9, 'ability':0.7,'works': 0.7, 'well':0.5}, 
	
	'Errors/Effectiveness': {'error': 1.0,'effectiveness':1.0, 'difficult': 0.9, 'waste':0.9, 'problem':0.9,'miss':0.7,'crash':0.85,'mistake':0.8,'freeze':0.8,'trouble':0.8,'wrong':0.9,'fix': 0.9, 'incompetent': 0.7, 
							'broken': 0.8,'camera': 0.75, 'glitch': 0.95,'instability':0.8, 'issue': 0.9,'imprecise':0.8, 'lag': 0.9,'bug': 0.95, 'delay':0.9, 'primit':0.5, 'load':0.71, 'responsive':0.7, 'resolute':0.8, 
							'confuse':0.8, 'poor':0.65, 
							'suffer':0.65, 'lack': 0.75, 'laggy':0.8, 'defect':0.79,'shit':0.65,'fuck':0.65,'suck':0.65,'horrible':0.70,'awful':0.8, 'annoy':0.77, 'flaw':0.7, 
							'inconsistent': 0.8},
	
	'Learnability': {'learn': 1.0, 'intuit': 0.9, 'ability':0.65,'easy': 0.7,'straightforward': 0.75,'foreword': 0.75, 'applet':0.8,'smooth':0.5, 'master':0.5, 
					'experiment':0.5, 'simple':0.7, 'practice': 0.65}, 
	
	'Memorability': {'memorability':0.8,'memory': 1.0, 'heard':0.5, 'forgot': 0.8, 'reminds':0.8,'remember': 0.9}, 
	
	'Satisfaction': {'satisfaction':1.0,'happy': 0.8, 'fun': 0.9, 'great': 0.7, 'excellent':0.9,'good':0.6, 'disgust':0.65, 'love': 0.8, 'awesome':0.9,'wonderful':0.9,'worth': 0.8, 'recommend': 0.6, 
					'favorite': 0.8, 'cool': 0.6, 'reliable':0.8,'perfect': 0.9,'disappoint': 0.7,'bad': 0.8, 'quality': 0.7,
					'unfortunate': 0.7,'fantastic': 0.8,'grinning':0.70,'smiling':0.65},


	'Aesthetics and Appeal': {'aesthetic': 1.0, 'interface': 0.9,'semblance':0.75, 'attractive':0.6,'colour':0.65,'layout':0.75,'visual':0.75,'pretty':0.8,'wonderful':0.8,
						'beauty': 0.9,'appreciation': 0.65,
						'appeal': 1.0, 'graphic':0.9, 'sound':0.9, 'song': 0.9, 'voice':0.8, 'playlist':0.9, 'music':0.9, 'soundtrack':0.9, 'effect':0.6, 'look':0.65, 'bright':0.65,'realism':0.7,
						'detail':0.65,'speaker':0.7,'environment':0.6,'animation':0.7,'render': 0.75, 'pixel': 0.75},
	
	'Affect and Emotion': {'affect': 1.0, 'emotion': 1.0, 'fearless':0.7, 'scarier':0.8, 'cry': 0.8,'sadness':0.7, 'hate': 0.8,'trust': 0.75,'surprise': 0.8,'fear': 0.8,'disgust': 0.8,'frustration': 0.8,'anger': 0.8,
						'fun': 0.8, 'enjoy': 0.8, 'addict': 0.7,
						'excit': 0.7,'laugh': 0.65, 'annoy': 0.8, 'nostalgia': 0.65,'hilarious': 0.65,'engagement': 0.7,'truliant': 0.6,
						'chore': 0.4,'lighter': 0.3,'grin': 0.4,'fell': 0.7,'felt': 0.7,'laughing':0.7,'sooth': 0.7,'humor': 0.7,'grinning':0.70,'love': 0.8},
	
	'Anticipation': {'anticipation': 1.0, 'expectation': 0.9, 'hope':0.8,'pre-order':0.90,'pre-purchase':0.8,'soon':0.75,'presale':0.8},
	
	'Comfort': {'comfort': 1.0, 'problem':0.65,'mistake':0.55,'crash':0.5,'lock':0.55,'poor':0.6,'physical': 0.7, 'workout': 0.65, 'fits':0.45, 
				'comfy':0.9, 'cozy':0.9, 'pleasure':0.65,'fear':0.55, 'happy': 0.6, 'body':0.75, 'care':0.6, 'active':0.65},
	
	'Detailed Usability': {'detailed':0.2 ,'usability': 0.95, 'problem': 0.95, 'reliable':0.7,'convenient':0.7,'viewable':0.7,'awkward':0.8,'useful':0.8,'efficient':0.8,'effective':0.8, 'broken': 0.8,'camera': 0.75, 
					'lag': 0.9,'bug': 0.9, 'delay':0.9, 'glitch': 0.8,'performance':0.96, 'latencies':0.8, 
					'great': 0.4, 'detail': 0.6, 'function': 0.7, 'satisfaction': 0.95,'quality': 0.6,'perfect': 0.6,'perfect': 0.6,'cool': 0.6,
					'interest': 0.6,'improve': 0.6,'price': 0.6,'feel': 0.6,'well': 0.4,'definite': 0.5,'memorability': 0.9,'effectiveness':0.9,'error': 0.8,'efficiency': 0.9,'memory': 0.6,'favorite': 0.5,'learnability': 0.9,'good': 0.5,
					'sound': 0.65,'fun': 0.6,'disappoint': 0.65, 'bad': 0.65,'lack': 0.75,'prettier': 0.6,'issue': 0.7,
					'recommend': 0.6,'easy': 0.6,'graphic': 0.7,'choreography':0.9,'playlist':0.9, 'music':0.9, 'soundtrack':0.9,'overall': 0.6,'love': 0.5,'worth': 0.65,'nice': 0.35,'really': 0.4,'best':0.55},
	
	'Enchantment': {'enchantment': 1.0, 'concentration': 0.7,'love': 0.9,'clapping':0.6,'attention': 0.55,'hearts':0.5,'liveliness': 0.6,'grinning':0.6,'fullness': 0.6,'pleasure': 0.85,'disorientation': 0.7,'experience': 0.6},
	
	'Engagement': {'engagement': 1.0, 'enjoyable':0.9,'communicate':0.5,'correct':0.5,'connect':0.4,'improve':0.6,'experience':0.7,'challenge': 0.9, 'flow': 1.0,'skill': 0.95,'need': 0.8,'forget': 0.7,
				'addict': 0.9, 'addition': 1.0, 'replay':0.7,'fun':0.7, 'nonstop': 0.9, 'lyric':0.85,'sing':0.85,'most':0.5,'interest':0.6,'become':0.6,'gripper':0.6,'hardest':0.6,'painstaking':0.6,'intense':0.6,'hard':0.7,'tire':0.5,
				'impossible':0.6,'keep':0.6,'therefore':0.6,
				'value':0.6,'tought':0.5,'easy':0.6,'complex':0.6,'moment':0.7,'hearts':0.7, 'harder':0.6,'depth':0.6,'difficult':0.6,'interest':0.8},
	
	'Enjoyment and Fun': {'enjoyment': 1.0, 'communicate':0.2,'cool':0.7,'wow':0.4,'awesome':0.6,'grinning':0.70,'hope':0.1,'spectacular':0.5,'happy':0.5,'hedonic': 0.9,'emotion': 0.7,'affect': 0.7,'fun': 1.0,  
						'entertain': 0.9, 'cute':0.5, 'nevertheless':0.3,'workout':0.55,'hilari':0.6,'fell':0.6,
						'lighter':0.2,'grin':0.2,'sooth':0.3,'excit':0.7,'laugh':0.68,'laughing':0.73,'humor':0.6,'amus':0.6,'love':0.6,'funniest':0.6},
	
	'Frustration': {'frustration': 1.0, 'irritate':0.8,'wtf':0.6,'terrible':0.8,'harmful':0.7,'hate':0.9,'shit':0.9,'fuck':0.9,'suck':0.9,'horrible':0.9,'awful':0.9,'waste':0.8,'disappointed':0.5,'hardship': 0.6,'boring': 0.9, 
					'grrrr': 0.4,'anger': 1.0,'hardest': 0.2, 'disadvantage': 0.1, 'flavor':0.3,'scaletta':0.3,'vito':0.2,'insane':0.4,'heck':0.3,'gasp':0.3,'habit':0.3,'melodramat':0.3,'cheat':0.3,'grow':0.2,'flat':0.4,'plain':0.4,
					'needle':0.1,'grin':0.2,'afterward':0.4,'injury':0.6,'insult':0.6,'boredom':0.7,'tension': 0.5,'disgust':0.5,'sadness':0.5,'angry':0.8,'pouting': 0.75,'insult': 0.5, 'nerv': 0.4, 'unfair':0.5, 'annoy':0.9, 'incompatibility':0.3},
	
	'Hedonic': {'hedonic': 1.0, 'quality':0.95, 'fun': 0.9, 'superb':0.8,'enjoy': 0.8, 'excitement':0.9, 'love':0.6,'good':0.5,'super':0.4,'awesome':0.8,'happy':0.6,'friend':0.5,'communicate':0.3,'challenge':0.7, 'fulfillment': 0.6, 'need': 0.1,
				'pleasure':0.9, 'frustration':0.9, 'annoy': 0.8, 'entertain': 0.8, 'game': 0.7,'play':0.75,'multiplayer': 0.7, 'lyric':0.8,'gameplay': 0.87, 'play': 0.8, 'humor': 0.8, 'workout': 0.8,'regret': 0.4, 'intrigu': 0.5,'stagger': 0.4,
				'nevertheless': 0.4,'nostalgia': 0.5,'afterward': 0.4,'fell': 0.7,'incompatibility': 0.2,'tension': 0.4,'chore': 0.4,'addict': 0.65,'catch': 0.2,'excit': 0.6,'grin': 0.4,'cute': 0.5,'lighter': 0.2,'felt': 0.3,'sooth': 0.3,'hate': 0.5,
				'funnier': 0.6,'boredom': 0.6},
	
	'Impact': {'impact': 1.0, 'pattern': 0.4, 'surprise': 0.8,'zany':0.5,'fear': 0.8,'wow':0.4, 'gameplay': 0.9, 'change': 0.4},
	
	'Likeability': {'likeability': 1.0, 'good':0.9, 'cool':0.85, 'happy': 0.75,'disgust':0.65, 'clapping':0.70,'smiling': 0.69,'joy': 0.50,'grinning':0.70,'nice':0.6}, 
	
	'Motivation': {'motivation': 1.0, 'task': 0.1, 'dance':0.25,'dancing':0.5, 'inspiring':0.7,'workout':0.65, 'exercising':0.7,'love':0.5,'curiosity': 0.5,'competition': 0.5,'joy': 0.4,'pleasure':0.5},
	
	'Overall Usability': {'overall usability': 1.0, 'update':0.8,'experience':0.77, 'retention':0.8, 'expectation':0.7, 'anticipation':0.7, 'old':0.6, 
						'satisfaction':0.9, 'effectiveness':0.9, 'feature':0.73,'new': 0.7, 'version':0.6, 'nostalgia':0.65, 'upgrade':0.8, 'edition': 0.7, 'previous':0.6},
	
	'Pleasure': {'pleasure': 1.0, 'fun': 0.8, 'moneybag':0.35, 'enjoy': 0.7, 'love': 0.7, 'entertain': 0.7, 'awesome': 0.8, 'stimulation':0.5, 'felt': 0.6, 'sooth': 0.7, 'adict': 0.7, 'countless': 0.5,'everytim': 0.5,'perpetu': 0.5,
				'regardless': 0.5,'shatter': 0.5,'intrigu': 0.5,'afterward': 0.5,'laugh': 0.7,'nevertheless': 0.5,'fell': 0.6,'incompatibility': 0.3,'chore': 0.3,'humor': 0.7,'grin': 0.4,
				'lighter': 0.4,'sooth': 0.3,'boredom': 0.7,'laughing':0.7,'nostalgia': 0.65},
	
	'Support': {'support':1.0, 'help':0.8, 'service':0.75,'team':0.5,'customer':0.6,'credibility':0.5,'call':0.6,'need':0.5, 'FAQ':0.6,'contact':0.8,'correct':0.8,'how':0.95, 
				'request':0.75,'improve':0.6,'add':0.7,'lack': 0.7,'please':0.6,'want':0.65,'should':0.3,'wish': 0.75,'software': 0.7},
	
	'Trust': {'trust': 1.0, 'behavior': 0.8, 'disappointed':0.8, 'handshake':0.4, 'easy':0.8, 'quality':0.8, 'exist':0.8, 'handhold':0.8, 'reliev':0.8, 'cute':0.8, 'sooth':0.8,'reliable':0.8,'secure':0.8,'pleasure': 0.5},
	
	'User Differences': {'user':0.8, 'group': 0.6,'head-to-head':0.8,'beginner':0.9, 'experience':0.9, 'reliability':0.8,'devices':0.8,'consoles':0.7,'platforms':0.7,'previous':0.8,'veteran':0.9,'pro':0.8 ,'reliability':0.7, 'features':0.7,'player':0.7, 'amateur':0.9,
						'professional':0.9, 'finalist':0.63, 'dancers':0.7,'buyer': 0.7,'target': 0.7,'feature': 0.7, 'difference': 0.8, 'if': 0.55},


	'Bodily image and Appearance': {'bodily':1.0, 'image': 0.58, 'appearance': 1.0, 'anorexia':0.8, 'anorexic':0.8, 'handicapped': 0.75,'physical': 0.9,'self-concept': 0.9,'body': 0.95,'limb': 0.6,'artificial': 0.5,
									'clothes': 0.8,'boots':0.75,'dress':0.78,'workout':0.66, 'eat':0.7, 'outfit':0.75,'muscles':0.71,'healthy':0.8,'make-up': 0.72,'impairment': 0.6,'acne':0.8,'ugly':0.8,'beautiful':0.77,
									'look': 0.35, 'fat':0.9,'beard':0.70 ,'skinny':0.9, 'workout':0.6,'exercising':0.6, 'weight':0.8},
	
	'Concentration': {'aware': 0.8,'awake': 0.8,'alert': 0.8,'performance': 0.6,'thinking':0.55,'memory':0.4,'learning':0.4,'insomnia': 0.8,'focus': 0.8,'pressure': 0.6,'think':0.49,'insomnia': 0.8,'epilepsy': 0.8,'dementia': 0.8,
					'concussion': 0.8,'attention deficit hyperactivy disorder': 0.8,'alcohol use disorder': 0.8,'attention': 0.9, 'cognitive': 0.8, 'concentration': 1.0},
	
	'Energy': {'energy': 1.0, 'alive': 0.3, 'endurance': 0.8,'sinchonized':0.4, 'calories':0.9, 'exercise':0.8, 'exercising':0.9, 'strong':0.7,'enthusiasm': 0.7, 'dancing':0.67, 'workout':0.9},
	
	'Fatigue': {'fatigue': 1.0, 'overexertion': 0.8, 'depression': 0.8, 'cramps':0.71, 'vomit':0.7, 'weariness': 0.77, 'anorexia':0.8, 'disorder':0.7,'anxiety': 0.8,'sedentary':0.6,'stress': 0.75, 'disease': 0.97, 'illness': 0.7,'tire': 0.8, 'exhaustion': 0.8},
	
	'Learning': {'cognitive': 0.6, 'education': 0.4,'knowledge': 0.55,'teach': 0.70,'concentration':0.4,'memory':0.4,'thinking':0.4,'processing':0.2, 'deficits': 0.3,'auditory':0.2, 'disorder': 0.3,'dyscalculia': 0.65,
				'dysgraphia': 0.6,'dyslexia': 0.6,'pedagogy': 0.55, 'learn': 1.0},
	
	'Memory': {'forget': 0.8, 'alzheimer': 0.8, 'old': 0.75, 'reminds': 0.75, 'dementia': 0.8,'parkinson': 0.8,'korsakoff': 0.8,'huntington': 0.8,'autism': 0.8,'nostalgia':0.9, 'remember':0.8, 'memory': 1.0, 'cognitive': 0.8},
	
	'Negative feelings': {'negative':0.6, 'feeling': 0.3, 'despair': 0.8,'apathy': 0.8,'disapproval': 0.8,'agressiveness': 0.8,'remorse': 0.8,'contempt': 0.8,'disgust': 0.8,'panic':0.65, 'attacks': 0.2,'annoy': 0.8,'shame': 0.8,'sad': 0.8,
						'cry': 0.8,'mania': 0.4,'depression': 0.9,'distress': 0.9,'lack': 0.2,'frustration': 0.9, 
						'antidepressant': 0.8,'suicide': 0.8,'nauseated':0.65,'lonely': 0.8,'hopeless': 0.8,'fear': 0.8,'pouting': 0.75, 'boring':0.7, 'lack': 0.4,'angry':0.85, 'sucks': 0.7,'disapproval':0.4, 'humiliation':0.8, 'anger': 0.8,
						'anxiety': 0.8,'nervousness': 0.8,'despair': 0.8,'tearfulness': 0.8,'sadness': 0.8,'guilt': 0.8,'despondency': 0.8},
	
	'Pain and Discomfort': {'pain': 1.0, 'discomfort': 1.0,'worthlessness': 0.6,'depression': 0.77,'vomit':0.7, 'sad': 0.8,'grief': 0.8,'shame': 0.77,'distress': 0.9,'panic': 0.8,'sore':0.3, 'throat': 0.35,'sneezing':0.7, 'vomiting':0.7,'nauseated':0.7,
						'cramp': 0.9,'bone':0.3,'fracture': 0.65,'muscle':0.3 ,'cramp': 0.65,'toothache': 0.9,'bingeing':0.6,'bulimarexia':0.6,'headache': 0.9,'ache': 0.9,'disorder':0.7,'stiffness': 0.9,'drug': 0.8,
						'unpleasant': 0.8}, 
	
	'Personal relationships': {'personal': 1.0, 'homosexual': 0.7,'relationship': 0.85,'heterosexual': 0.7,'marriage': 0.7,'friendship': 0.8,'satisfaction': 0.5,'hug': 0.8,'happy': 0.4,'emotionally': 0.5,
							'intimate': 0.6,'love': 0.45,'support': 0.5,'people': 0.5,'who':0.5,'everybody':0.4, 'partnership': 0.7,'distress': 0.6,'share':0.6 ,'moments': 0.45,'companionship': 0.7,'friend': 0.9, 'family': 0.9, 'alone': 0.9},
	
	'Positive feelings': {'positive': 0.55, 'feeling': 0.3,'optimism': 0.7,'contentment': 0.7,'euphoria': 0.57,'eagerness': 0.7,'admiration': 0.7,'confidence': 0.7,'affection': 0.67,'relief': 0.7,
						'satisfaction': 0.8,'altruism': 0.75,'elevation': 0.65,'amusement': 0.70,'pride': 0.73,'gratitude': 0.73,'serenity': 0.73,'interest': 0.71,'inspiration': 0.7,'romance': 0.7,'hope': 0.66,
						'love': 0.8,'awe': 0.4,'fun': 0.8,'enjoyment': 0.8,'hopefulness': 0.8,'relax':0.7,'calm':0.7, 'grinning':0.70,'happiness': 0.8,'peace': 0.76},
	
	'Self-esteem': {'self':1.2, 'esteem': 0.95, 'self-esteem':1.0,'meaningful': 0.9,'public':0.5, 'appearance':0.85,'enthusiastic':0.78,'inspired':0.72,'distressed': 0.86,'strong': 0.85,'proud': 0.9,'confidence': 0.85,'narcissisism': 0.9,
				'superiority': 0.8,'honour': 0.8,'egoism': 0.9,'pride': 0.8,'arrogance': 0.9,
				'admiration': 0.8,'prestige': 0.8, 'well-being': 0.9,'ashamed': 0.9,'guilty': 0.9,'fat':0.73,'ugly':0.73,'worthless': 0.8,'think':0.45,'regard': 0.76,'respect': 0.75, 'competence': 0.65,'belonging': 0.6,'identity': 0.62,'security': 0.55,
				'acceptance': 0.73,'worth': 0.77,'appraisal': 0.9,'dignity': 0.95,'grinning':0.60,'disgust':0.65,'fear':0.65,'sadness':0.65,
				'family': 0.7,'embarrassment':0.9, 'people': 0.5,'education': 0.55,'unloved':0.66,'achievement':0.7,
				'win':0.77,'lose':0.72,'love':0.63, 'happy':0.65,'morality':0.65, 'creativity':0.63, 'spontaneity':0.65, 'prejudice':0.66,
				'integrity':0.66,'triumph':0.73, 'despair':0.77,'worthy':0.7, 'efficacy': 0.45,'control': 0.55,'oneself': 0.6,'healthy':0.66,'satisfaction': 0.7},
	
	'Sexual activity': {'sexual':0.9, 'sex':0.96,'activity': 0.1, 'physical':0.2 ,'intimacy': 0.4, 'fulfillment': 0.2,'expression': 0.1,'drive': 0.1,'desire': 0.25},
	
	'Sleep and Rest': {'sleep': 1.0,'waking':0.5 ,'up': 0.3, 'parasomnia': 0.8,'hypersomnia': 0.8,'yawning':0.66, 'nightmare':0.4, 'restless':0.3, 'leg':0.1 ,'syndrome': 0.1,'apnea': 0.8,'insomnia': 0.8,'lack':0.1, 'refreshment': 0.4,'rest': 0.97},
	
	'Social support': {'social':0.95, 'support': 0.90, 'encouragement': 0.8,'asking':0.72, 'share': 0.7,'talking': 0.8,'teaching': 0.85,'companionship':0.9,'empathy':0.9,'sympathy':0.9,'esteem':0.8,'solve': 0.4,'relationship': 0.95,
					'handshake':0.69,'roommate': 0.95, 'thanks': 0.75,'inclusive':0.7, 'help': 0.9,'chill': 0.5,'dude': 0.67,'best':0.3,'friend': 0.9,'physical':0.1,'abuse': 0.4,
					'verbal': 0.12,'personal': 0.8,'crisis': 0.58,'responsability': 0.8,'love':0.3, 'trust':0.5, 'caring':0.8, 'group':0.7,'community':0.7,'suggestions':0.73, 'encourage':0.8, 'advice':0.82, 'appraisal':0.55, 'information':0.55, 
					'useful':0.6,'assistance': 0.85,'together':0.7,'approval': 0.5,'kiss': 0.5,'commitment': 0.5,'family': 0.87},
	
	'Thinking': {'think': 1.0,'aware': 0.8,'awake': 0.8,'cognitive': 0.8,'reminds':0.5,'concentration':0.5,'memory':0.4,'learning':0.4,'clang': 0.8,'disorder': 0.2,'echolalia': 0.4,'distractible':0.2, 'speech': 0.5,'alogia': 0.4,'intelligent': 0.7,
				'idea': 0.4,'thought': 0.7,'decision': 0.55},

	#'Thinking, learning, memory and concentration': {'thinking': 1.0, 'aware': 1.0,'awake': 1.0,'alert': 1.0,'cognitive': 1.0,'thought': 1.0,'decisions': 1.0,'forget': 1.0, 'learning': 1.0, 'memory': 1.0, 'concentration': 1.0},
		
}











