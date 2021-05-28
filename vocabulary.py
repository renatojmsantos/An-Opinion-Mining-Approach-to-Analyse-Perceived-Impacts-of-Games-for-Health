
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
	
	'Errors/Effectiveness': {'error': 1.0,'effectiveness':1.0, 'excellent':0.8,'difficult': 0.9, 'waste':0.9,'easy':0.7,'problem':0.9,'miss':0.6,'crash':0.85,'mistake':0.8,'freeze':0.8,'trouble':0.8,'wrong':0.9,'fix': 0.9, 'incompetent': 0.7, 
							'broken': 0.7,'camera': 0.7, 'glitch': 0.8,'issue': 0.9,'imprecise':0.8, 'lag': 0.9,'bug': 0.8, 'delay':0.8, 'primit':0.5, 'load':0.7, 'respons':0.8, 'resolute':0.8, 'prompt':0.8, 'technic':0.8, 'confuse':0.8, 'data':0.3,
							'suffer':0.5, 'matter':0.4, 'semblanc':0.3, 'ai':0.3, 'defect':0.76,'biowar':0.1, 'dodg':0.1, 'crowd':0.2, 'flaw':0.4, 'suspect':0.5, 'configure':0.5, 'bump':0.5, 'inconsistent': 0.8},
	
	'Learnability': {'learn': 1.0, 'intuit': 0.9, 'ability':0.6,'easy': 0.8,'figure': 0.5,'straightforward': 0.8,'foreword': 0.8, 'applet':0.6, 'casual':0.6, 'sensor':0.3, 'incred':0.3, 'nunchuk':0.1, 'smooth':0.3, 'master':0.4, 
					'minute':0.1, 'thus':0.05, 'password':0.1, 'experiment':0.5, 'steam':0.05, 'menu':0.1, 'simple':0.8, 'practice': 0.7}, 
	
	'Memorability': {'memorability':0.8,'memory': 1.0, 'excellent':0.2,'heard':0.3, 'forgot': 0.8, 'remember': 0.9}, 
	
	'Satisfaction': {'satisfaction':1.0,'happy': 0.8, 'fun': 0.9, 'great': 0.6, 'excellent':0.9,'good':0.5, 'love': 0.9, 'awesome':0.9,'wonderful':0.9,'worth': 0.8, 'best': 0.7, 'recommend': 0.7, 
					'favorite': 0.8, 'cool': 0.5, 'reliable':0.8,'perfect': 0.9,'realli': 0.03,'graphic': 0.2,'sound': 0.2,'music': 0.2,'overall': 0.2,'problem': 0.6,'disappoint': 0.7,'definit': 0.1,'bad': 0.8, 'quality': 0.6,'feel': 0.4,'pretti': 0.5,
					'lack': 0.7,'unfortunate': 0.7,'well': 0.6,'fantastic': 0.8,'improve': 0.3,'price': 0.2, 'grinning':0.70,'interest': 0.35,'fan': 0.2},


	'Aesthetics and Appeal': {'aesthetic': 1.0, 'interface': 0.9, 'semblanc':0.3, 'visual':0.6,'nice':0.15,'pretty':0.2,'excellent':0.3,'awesome':0.3,'correct':0.1,'wonderful':0.4,'great':0.1,'taste': 0.1,'beauty': 0.6,'appreciation': 0.6,
						'appeal': 1.0, 'graphic':0.9, 'sound':0.9, 'song': 0.9, 'nice': 0.15, 'voice':0.9, 'playlist':0.9, 'music':0.9, 'soundtrack':0.9, 'effect':0.6, 'look':0.6, 'color':0.7, 'hear':0.2,'creepiest':0.2,'stun':0.2,'bright':0.3,'realism':0.4,
						'detail':0.6,'cute':0.3,'model':0.1,'impress':0.3,'sprite':0.3,'sceneri':0.3,'atmosphere':0.4,'environment':0.4,'animation':0.5,'realist':0.4, 'render': 0.5, 'pixel': 0.7},
	
	'Affect and Emotion': {'affect': 1.0, 'emotion': 1.0, 'fearless':0.7, 'scarier':0.8, 'cry': 0.8,'hate': 0.8,'trust': 0.8,'surprise': 0.8,'fear': 0.8,'disgust': 0.8,'frustration': 0.8,'anger': 0.8,'fun': 0.8, 'enjoy': 0.8, 'addict': 0.7, 'workout': 0.6, 
						'excit': 0.7,'cute': 0.5, 'nevertheless': 0.5, 'laugh': 0.6, 'annoy': 0.8, 'nostalgia': 0.8,'creatur': 0.4,'hilarious': 0.6,'incompatibilit': 0.2,'kinda': 0.2,'tension': 0.5,'engagement': 0.7,'truliant': 0.6,
						'chore': 0.4,'lighter': 0.3,'grin': 0.4,'fell': 0.7,'felt': 0.7,'sooth': 0.7,'humor': 0.7,'scari': 0.7,'grinning':0.70,'amus': 0.7,'love': 0.8,'entertain': 0.7,'boredom':0.7},
	
	'Anticipation': {'anticipation': 1.0, 'expectation': 0.9, 'hope':0.7},
	
	'Comfort': {'comfort': 1.0, 'problem':0.7,'bad':0.3,'mistake':0.3,'crash':0.3,'alert':0.3,'lock':0.3,'poor':0.3,'freeze':0.3,'slow':0.3,'physical': 0.4, 'workout': 0.7, 'fits':0.25, 
				'comfy':0.9,'feel':0.6, 'cozy':0.9, 'pleasure':0.6, 'well':0.3, 'being':0.1, 'happy': 0.6, 'physical need': 0.9, 'body':0.4, 'care':0.2, 'active':0.2},
	
	'Detailed Usability': {'detailed usability': 1.0, 'problem': 0.7, 'great': 0.4, 'detail': 0.4, 'function': 0.7, 'satisfaction': 0.6,'usability': 0.9, 'quality': 0.6,'perfect': 0.6,'perfect': 0.6,'cool': 0.6,'interest': 0.6,'improve': 0.6,'price': 0.6,
					'feel': 0.6,'well': 0.4,'definite': 0.5,'memorability': 0.6,'error': 0.6,'efficiency': 0.6,'memory': 0.6,'favorite': 0.5,'learn': 0.6,'good': 0.5,'sound': 0.6,'fun': 0.6,'disappoint': 0.6,'bad': 0.6,'prettier': 0.6,'issue': 0.6,'recommend': 0.6,
					'easy': 0.6,'graphic': 0.6,'overall': 0.55,'love': 0.6,'worth': 0.6,'nice': 0.3,'really': 0.4,'best':0.5 },
	
	'Enchantment': {'enchantment': 1.0, 'concentration': 0.7,'love': 0.9,'attention': 0.8,'liveliness': 0.7,'grinning':0.70,'fullness': 0.8,'pleasure': 0.9,'disorientation': 0.7,'experience': 0.5},
	
	'Engagement': {'engagement': 1.0, 'enjoyable':0.8,'stop':0.1,'communicate':0.5,'correct':0.5,'connect':0.4,'improve':0.6,'experience':0.8,'challenge': 0.9, 'flow': 1.0,'skill': 1.0,'need': 1.0,'forget': 1.0,
				'addict': 0.9, 'addition': 1.0, 'replay':0.7, 'nonstop': 0.9, 'lyric':0.85,'sing':0.85,'most':0.5,'interest':0.6,'become':0.6,'gripper':0.6,'hardest':0.6,'painstaking':0.6,'intense':0.6,'hard':0.5,'tire':0.5,'engagement':0.6,'impossible':0.6,'keep':0.6,'therefore':0.6,
				'deep':0.6,'value':0.6,'tought':0.6,'easy':0.6,'complex':0.6,'moment':0.6,'harder':0.6,'depth':0.6,'hour':0.6,'difficult':0.6,'addict':0.6,'interest':0.7},
	
	'Enjoyment and Fun': {'enjoyment': 1.0, 'communicate':0.2,'easy':0.1,'cool':0.7,'wow':0.4,'awesome':0.6,'grinning':0.70,'hope':0.1,'spectacular':0.5,'happy':0.5,'hedonic': 0.9,'emotion': 0.9,'affect': 0.9,'fun': 1.0, 'young': 0.2, 
						'entertain': 0.7, 'boredom':0.3,'jeremi':0.2,'tedious':0.6,'queue':0.4,'cute':0.5, 'scare':0.4,'shatter':0.3,'intrigu':0.3,'nevertheless':0.3,'workout':0.6,'hilari':0.6,'fell':0.6,'kinda':0.3,
						'lighter':0.2,'grin':0.2,'sooth':0.3,'excit':0.7,'laugh':0.6,'humor':0.6,'amus':0.6,'love':0.6,'funniest':0.6},
	
	'Frustration': {'frustration': 1.0, 'irritate':0.8,'wtf':0.8,'terrible':0.8,'harmful':0.6,'hate':0.8,'shit':0.8,'fuck':0.8,'suck':0.8,'horrible':0.8,'awful':0.8,'waste':0.8,'disappointed':0.8,'hardship': 0.7,'boring': 0.8, 
					'grrrr': 0.4,'anger': 1.0,'hardest': 0.2, 'disadvantage': 0.1, 'flavor':0.3,'scaletta':0.3,'vito':0.2,'insane':0.4,'heck':0.3,'gasp':0.3,'habit':0.3,'melodramat':0.3,'cheat':0.3,'grow':0.2,'flat':0.4,'plain':0.4,
					'needle':0.1,'grin':0.2,'afterward':0.4,'fuel':0.2,'injury':0.6,'insult':0.6,'perpetu':0.6,'pouting': 0.75,'insult': 0.5, 'perpetu':0.3, 'nerv': 0.3, 'unfair':0.4, 'annoy':0.8, 'incompatibility':0.3},
	
	'Hedonic': {'hedonic': 1.0, 'fun': 0.8, 'superb':0.8,'enjoy': 0.8, 'love':0.8,'good':0.5,'super':0.4,'awesome':0.8,'happy':0.6,'friend':0.5,'communicate':0.3,'challenge':0.5, 'fulfillment': 0.6, 'need': 0.1, 'pleasure':0.7,
				'frustration':0.7, 'annoy': 0.8, 'entertain': 0.8, 'game': 0.7,'multiplayer': 0.7, 'lyric':0.8,'gameplay': 0.7, 'play': 0.7, 'humor': 0.8, 'workout': 0.8,'regret': 0.4, 'intrigu': 0.5,'stagger': 0.4,
				'nevertheless': 0.4,'nostalgia': 0.5,'afterward': 0.4,'fell': 0.7,'incompatibility': 0.2,'tension': 0.4,'chore': 0.4,'addict': 0.6,'catch': 0.2,'excit': 0.6,'grin': 0.4,'cute': 0.5,'lighter': 0.2,'felt': 0.3,'sooth': 0.3,'hate': 0.5,
				'funnier': 0.6,'boredom': 0.6},
	
	'Impact': {'impact': 1.0, 'pattern': 0.4, 'surprise': 0.8,'fear': 0.8,'wow':0.4, 'gameplay': 0.9, 'change': 0.38},
	
	'Likeability': {'likeability': 1.0, 'good':0.9, 'cool':0.85, 'happy': 0.75,'smiling': 0.65,'joy': 0.55,'grinning':0.70,'nice':0.7}, 
	
	'Motivation': {'motivation': 1.0, 'task': 0.5, 'dance':0.5,'love':0.8, 'joy': 0.8,'pleasure':0.8},
	
	'Overall Usability': {'overall usability': 1.0, 'update':0.8,'feature':0.8,'new': 0.25, 'version':0.6, 'upgrade':0.8, 'edition': 0.65, 'previous':0.6 ,'edition':0.3},
	
	'Pleasure': {'pleasure': 1.0, 'fun': 0.8, 'moneybag':0.4, 'enjoy': 0.7, 'love': 0.7, 'entertain': 0.7, 'awesome': 0.8, 'stimulation':0.5, 'felt': 0.6, 'sooth': 0.7, 'adict': 0.7, 'countless': 0.5,'everytim': 0.5,'perpetu': 0.5,
				'regardless': 0.5,'shatter': 0.5,'intrigu': 0.5,'afterward': 0.5,'laugh': 0.7,'nevertheless': 0.5,'fell': 0.6,'incompatibility': 0.3,'chore': 0.3,'humor': 0.7,'grin': 0.4,
				'workout': 0.6,'lighter': 0.4,'sooth': 0.3,'annoy': 0.7,'boredom': 0.7,'nostalgia': 0.7},
	
	'Support': {'support':1.0, 'help':0.8, 'service':0.8,'team':0.5,'call':0.8,'contact':0.8,'correct':0.8,'how':0.9, 'request':0.75,'improve':0.55,'please':0.6,'want':0.65,'should':0.23,'wish': 0.7,'software': 0.7},
	
	'Trust': {'trust': 1.0, 'behavior': 0.8, 'disappointed':0.8, 'handshake':0.4, 'easy':0.8, 'quality':0.8, 'exist':0.8, 'handhold':0.8, 'reliev':0.8, 'cute':0.8, 'sooth':0.8,'reliable':0.8,'secure':0.8,'pleasure': 0.5},
	
	'User Differences': {'user':0.8, 'group': 0.5,'head-to-head':0.8,'beginner':0.9, 'veteran':0.9,'pro':0.6 ,'player':0.7, 'amateur':0.9,'professional':0.9,'finalist':0.6, 'professional':0.65, 'dancers':0.65,
						'buyer': 0.7,'target': 0.7,'feature': 0.7, 'difference': 0.8, 'if': 0.55},



	'Bodily image and Appearance': {'bodily':1.0, 'image': 0.5, 'appearance': 1.0, 'handicapped': 0.6,'physical': 0.9,'self-concept': 0.8,'body': 0.7,'limb': 0.6,'artificial': 0.5,
									'clothing': 0.6,'make-up': 0.7,'impairment': 0.6,'look': 0.6, 'beard':0.25 ,'skinny':0.6, 'weight':0.25,'body': 0.7},
	
	'Concentration': {'aware': 0.8,'awake': 0.8,'alert': 0.8,'insomnia': 0.8,'epilepsy': 0.8,'dementia': 0.8,'concussion': 0.8,'attention deficit hyperactivy disorder': 0.8,'alcohol use disorder': 0.8,'attention': 0.8, 'cognitive': 0.8, 'concentration': 1.0},
	
	'Energy': {'energy': 1.0, 'alive': 0.8, 'endurance': 0.8,'sinchonized':0.4, 'enthusiasm': 0.8, 'sedentary':0.35, 'dance':0.65, 'workout':0.9},
	
	'Fatigue': {'fatigue': 1.0, 'overexertion': 0.8, 'depression': 0.8, 'cramps':0.71, 'weariness': 0.77, 'anxiety': 0.8,'stress': 0.75, 'disease': 0.97, 'illness': 0.7,'tire': 0.8, 'exhaustion': 0.8},
	
	'Learning': {'cognitive': 0.8, 'education': 0.8,'knowledge': 0.6,'processing deficits': 0.8,'auditory processing disorder': 0.75,'dyscalculia': 0.8,'dysgraphia': 0.8,'dyslexia': 0.8,'pedagogy': 0.7, 'learn': 1.0},
	
	'Memory': {'forget': 0.8, 'alzheimer': 0.8, 'old': 0.6, 'dementia': 0.8,'parkinson': 0.8,'korsakoff': 0.8,'huntington': 0.8,'autism': 0.8,'nostalgia':0.9, 'remember':0.8, 'memory': 1.0, 'cognitive': 0.8},
	
	'Negative feelings': {'negative':0.4, 'feeling': 0.2, 'disgust': 0.8,'panic attacks': 0.8,'cry': 0.8,'mania': 0.4,'depression': 0.9,'distress': 0.9,'lack': 0.2,'frustration': 0.9, 
						'antidepressant': 0.8,'suicide': 0.8,'lonely': 0.8,'hopeless': 0.8,'fear': 0.8,'pouting': 0.75, 'boring':0.7, 'lack': 0.4,'angry':0.85, 'sucks': 0.7,'disapproval':0.4, 'humiliation':0.8, 'anger': 0.8,'anxiety': 0.8,'nervousness': 0.8,'despair': 0.8,'tearfulness': 0.8,'sadness': 0.8,'guilt': 0.8,'despondency': 0.8},
	
	'Pain and Discomfort': {'pain': 1.0, 'discomfort': 1.0,'sore throat': 0.8,'cramp': 0.9,'bone fracture': 0.9,'muscle cramp': 0.9,'toothache': 0.9,'headache': 0.9,'ache': 0.9,'stiffness': 0.9,'drug': 0.8,'distress': 0.8,'unpleasant': 0.8}, 
	
	'Personal relationships': {'personal': 1.0, 'homosexual': 0.7,'relationship': 0.85,'heterosexual': 0.7,'marriage': 0.7,'friendship': 0.7,'satisfaction': 0.5,'hug': 0.7,'happy': 0.4,'emotionally': 0.4,
							'intimate': 0.6,'love': 0.5,'support': 0.5,'people': 0.5,'everybody':0.4, 'partnership': 0.7,'distress': 0.7,'share moments': 0.6,'companionship': 0.7,'friend': 0.9, 'family': 0.9, 'alone': 0.9},
	
	'Positive feelings': {'positive': 0.4, 'feelings': 0.2, 'enjoyment': 0.8,'hopefulness': 0.8,'grinning':0.70,'happiness': 0.8,'peace': 0.8,'balance': 0.3,'contentment': 0.5},
	
	'Self-esteem': {'self':1.0, 'esteem': 0.95, 'meaningful': 0.85,'confidence': 0.85,'regard': 0.7,'respect': 0.75, 'competence': 0.6,'belonging': 0.6,'identity': 0.7,'security': 0.6,'acceptance': 0.7,'worth': 0.7,'appraisal': 0.9,'dignity': 0.95,'family': 0.7,'embarrassment':0.85, 'people': 0.5,'education': 0.55,'efficacy': 0.45,'control': 0.45,'oneself': 0.6,'satisfaction': 0.6},
	
	'Sexual activity': {'sexual':1.0, 'activity': 0.1, 'physical':0.2 ,'intimacy': 0.4,'fulfillment': 0.2,'expression': 0.1,'drive': 0.1,'desire': 0.25},
	
	'Sleep and Rest': {'sleep': 1.0,'waking up': 0.8, 'parasomnia': 0.8,'hypersomnia': 0.8,'nightmare':0.4, 'restless leg syndrome': 0.4,'apnea': 0.8,'insomnia': 0.8,'lack of refreshment': 0.4,'rest': 0.97},
	
	'Social support': {'social':0.85, 'support': 0.85, 'encouragement': 0.8,'solve': 0.4,'relationship': 0.8,'roommate': 0.8,'thanks': 0.65, 'help': 0.8,'chill': 0.5,'dude': 0.5,'best':0.3,'friend': 0.7,'physical':0.1,'abuse': 0.4,'verbal': 0.12,'personal': 0.8,'crisis': 0.7,
					'responsability': 0.8,'assistance': 0.8,'approval': 0.5,'commitment': 0.5,'family': 0.8},
	
	'Thinking': {'think': 1.0,'aware': 0.8,'awake': 0.8,'cognitive': 0.8,'clang': 0.8,'thought disorder': 0.4,'echolalia': 0.4,'distractible speech': 0.4,'alogia': 0.4,'intelligent': 0.7,'idea': 0.4,'thought': 0.7,'decision': 0.55},

	#'Thinking, learning, memory and concentration': {'thinking': 1.0, 'aware': 1.0,'awake': 1.0,'alert': 1.0,'cognitive': 1.0,'thought': 1.0,'decisions': 1.0,'forget': 1.0, 'learning': 1.0, 'memory': 1.0, 'concentration': 1.0},
		
}











