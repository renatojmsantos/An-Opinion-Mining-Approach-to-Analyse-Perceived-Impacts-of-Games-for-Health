
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
		
	'Efficiency': {'efficiency': 1.0, 'perfect': 0.65,'speed':0.7, 'load':0.8,'useful':0.7,'performance':0.7, 'experience':0.65,'difficult':0.75,'lock':0.56,'prompt':0.8,'slow':0.9,'limit':0.7, 'fast':0.9, 'ability':0.7,'works': 0.7, 'well':0.58}, 
	
	'Errors/Effectiveness': {'error': 1.0,'effectiveness':1.0, 'difficult': 0.9, 'waste':0.9, 'problem':0.9,'miss':0.7,'crash':0.85,'mistake':0.8,'freeze':0.8,'trouble':0.8,'wrong':0.9,'fix': 0.9, 'incompetent': 0.7, 
							'broken': 0.8,'camera': 0.75, 'glitch': 0.95,'instability':0.8, 'issue': 0.9,'imprecise':0.8, 'lag': 0.9,'bug': 0.95, 'delay':0.9,  'load':0.75, 'responsive':0.7, 'resolute':0.8, 
							'confuse':0.8, 'poor':0.65, 
							'suffer':0.65, 'lack': 0.75, 'laggy':0.8, 'defect':0.79,'suck':0.65,'horrible':0.70,'awful':0.8, 'annoy':0.77, 'flaw':0.7, 
							'inconsistent': 0.8},
	
	'Learnability': {'learn': 1.0, 'intuit': 0.9, 'ability':0.65,'easy': 0.7,'straightforward': 0.75,'foreword': 0.75, 'applet':0.8,'smooth':0.56, 'master':0.56, 
					'experiment':0.56, 'simple':0.7, 'practice': 0.65}, 
	
	'Memorability': {'memorability':0.8,'memory': 1.0, 'forgot': 0.8, 'remind':0.8,'remember': 0.9}, 
	
	'Satisfaction': {'satisfaction':1.0,'happy': 0.8, 'fun': 0.9, 'great': 0.7, 'excellent':0.9,'good':0.6, 'disgust':0.65, 'love': 0.56, 'pleasure':0.6,'awesome':0.9,'wonderful':0.9,'worth': 0.8, 'recommend': 0.6, 
					'favorite': 0.8, 'cool': 0.6, 'reliable':0.8,'perfect': 0.9,'disappoint': 0.7,'bad': 0.8, 'quality': 0.7,
					'unfortunate': 0.7,'fantastic': 0.8,'grin':0.70,'smile':0.65},


	'Aesthetics and Appeal': {'aesthetic': 1.0, 'interface': 0.9,'semblance':0.75, 'attractive':0.6,'colour':0.65,'layout':0.75,'visual':0.75,'pretty':0.8,'wonderful':0.8,
						'beauty': 0.9,'appreciation': 0.65,
						'appeal': 1.0, 'graphic':0.9, 'sound':0.9, 'song': 0.9, 'voice':0.8, 'playlist':0.9, 'lyric':0.75,'music':0.9, 'soundtrack':0.9, 'effect':0.6, 'look':0.65, 'bright':0.65,'realism':0.7,
						'detail':0.65,'speaker':0.7,'environment':0.6,'animation':0.7,'render': 0.75, 'pixel': 0.75},
	
	'Affect and Emotion': {'affect': 1.0, 'emotion': 1.0, 'fearless':0.7, 'scarier':0.8, 'cry': 0.8,'sadness':0.7, 'hate': 0.8,'trust': 0.75,'surprise': 0.8,'fear': 0.8,'disgust': 0.8,'frustration': 0.8,'anger': 0.8,
						'fun': 0.8, 'enjoy': 0.8, 'addict': 0.7,
						'excit': 0.7,'laugh': 0.65, 'annoy': 0.8, 'nostalgia': 0.65,'hilarious': 0.65,'engagement': 0.7,'truliant': 0.6,
						'laugh':0.7,'sooth': 0.7,'humor': 0.7,'grin':0.70,'love': 0.8},
	
	'Anticipation': {'anticipation': 1.0, 'expectation': 0.9, 'hope':0.8,'pre-order':0.90,'pre-purchase':0.8,'soon':0.75,'presale':0.8},
	
	'Comfort': {'comfort': 1.0, 'problem':0.65,'physical': 0.7, 'workout': 0.65, 'fits':0.56, 'ergonomic': 0.85, 
				'comfy':0.9, 'cozy':0.9, 'pleasure':0.65, 'body':0.75, 'care':0.6, 'active':0.65},
	
	'Detailed Usability': {'usability': 1.0, 'problem': 0.95, 'reliable':0.7,'convenient':0.7,'viewable':0.7,'awkward':0.8,'useful':0.8,'efficient':0.8,'effective':0.8, 'broken': 0.8,'camera': 0.75, 
					'lag': 0.9,'bug': 0.9, 'delay':0.9, 'glitch': 0.8,'performance':0.96, 'latencies':0.8, 
					'great': 0.65, 'detail': 0.95, 'function': 0.9, 'satisfaction': 0.95,'quality': 0.6,'perfect': 0.6,
					'interest': 0.6,'improve': 0.6,'memorability': 0.9,'effectiveness':0.9,'error': 0.8,'efficiency': 0.9,'memory': 0.6,'learnability': 0.9,
					'sound': 0.75,'fun': 0.7,'disappoint': 0.65, 'bad': 0.65,'lack': 0.75,'prettier': 0.6,'issue': 0.7,
					'recommend': 0.8,'easy': 0.6,'graphic': 0.8,'choreography':0.9,'playlist':0.9, 'music':0.9, 'soundtrack':0.9,'overall': 0.6,'worth': 0.65},
	
	'Enchantment': {'enchantment': 1.0, 'concentration': 0.9,'love': 0.8,'clap':0.6,'attention': 0.9,'hearts':0.6,'liveliness': 0.7,'pleasure': 0.85,'disorientation': 0.7,'experience': 0.6},
	
	'Engagement': {'engagement': 1.0, 'enjoyable':0.9,'experience':0.7,'challenge': 0.95, 'flow': 1.0,'skill': 0.95,'forget': 0.7,
				'addict': 0.9, 'addition': 1.0, 'replay':0.8,'fun':0.8, 'dance':0.56, 'nonstop': 0.9, 'lyric':0.85,'soundtrack':0.9,'sing':0.85,'hardest':0.6,
				'easy':0.6,'hearts':0.7,'difficult':0.7,'stars':0.7},
	
	'Enjoyment and Fun': {'enjoyment': 1.0, 'awesome':0.6,'grin':0.70,'happy':0.7,'hedonic': 0.9,'emotion': 0.7,'affect': 0.7,'fun': 1.0,  
						'entertain': 0.9, 'grin':0.7,'humor': 0.7,'excit':0.7,'hilarious': 0.6,'laugh':0.75,'love':0.75},
	
	'Frustration': {'frustration': 1.0, 'irritate':0.8,'wtf':0.65,'terrible':0.8,'harmful':0.7,'hate':0.9,'shit':0.9,'fuck':0.9,'suck':0.9,'horrible':0.9,'awful':0.9,'waste':0.8,'disappoint':0.6,'hardship': 0.6,'boring': 0.9, 
					'grrrr': 0.65,'anger': 1.0,'hard': 0.7, 'disadvantage': 0.8, 'insane':0.8,'heck':0.7,'gasp':0.7,'cheat':0.7,
					'injury':0.8,'insult':0.8,'tension': 0.8,'disgust':0.7,'sadness':0.8,'angry':0.8,'pout': 0.7,'nervous': 0.8, 'unfair':0.8, 'annoy':0.9},
	
	'Hedonic': {'hedonic': 1.0, 'fun': 0.9, 'superb':0.8,'enjoy': 0.8, 'social':0.7,'memories':0.9,'beauty':0.9,'excitement':0.9, 'love':0.6,'awesome':0.8,'friend':0.65,'ergonomic': 0.7, 
				'pleasure':0.9, 'frustration':0.9, 'entertain': 0.8, 'multiplayer': 0.7,'gameplay': 0.9, 'happy':0.75,'stimulation':0.65,
				'nostalgia': 0.7,'boredom': 0.6},
	
	'Impact': {'impact': 1.0, 'pattern': 0.6, 'wow':0.56,'surprise': 0.8,'gameplay': 0.9, 'change': 0.6},
	
	'Likeability': {'likeability': 1.0, 'good':0.9, 'cool':0.8, 'satisfaction':0.9,'happy': 0.75,'disgust':0.65, 'clap':0.70,'smile': 0.7,'useful':0.8,'joy': 0.60,'grin':0.70,'nice':0.65}, 
	
	'Motivation': {'motivation': 1.0, 'dance':0.56, 'inspiring':0.7,'workout':0.7, 'exercise':0.8,'curiosity': 0.65,'competition': 0.6,'joy': 0.56,'pleasure':0.65},
	
	'Overall Usability': {'usability': 1.0, 'update':0.8,'experience':0.75, 'retention':0.8, 'expectation':0.8, 'anticipation':0.65, 'old':0.65, 
						'satisfaction':0.9, 'effectiveness':0.9, 'feature':0.8,'new': 0.8, 'release':0.75, 'version':0.7, 'nostalgia':0.65, 'upgrade':0.8, 'edition': 0.8, 'previous':0.65},
	
	'Pleasure': {'pleasure': 1.0, 'fun': 0.8, 'enjoy': 0.7,'wonderful':0.9,'worth': 0.8, 'perfect':0.8, 'beautiful':0.7,'nice':0.65,'attractive':0.7, 'love': 0.75, 'entertain': 0.7, 'awesome': 0.9, 'addict': 0.7, 
				'grin': 0.7, 'laugh':0.7,'nostalgia': 0.65},
	
	'Support': {'support':1.0, 'help':0.85, 'service':0.7,'customer':0.6,'FAQ':0.6,'contact':0.8,'correct':0.7,'how':0.95, 
				'request':0.75,'improve':0.65,'add':0.8,'lack': 0.7,'please':0.6,'want':0.65,'should':0.63,'wish': 0.75,'software': 0.7},
	
	'Trust': {'trust': 0.95, 'behavior': 0.7, 'disappoint':0.8, 'quality':0.7, 'belief':0.8, 'reliance':0.8,'reliability':0.8,'reliable':0.8,'secure':0.8},
	
	'User Differences': {'user':0.75, 'social':0.63,'group': 0.6,'head-to-head':0.8,'beginner':0.9, 'experience':0.8, 'multiplayer':0.65, 'devices':0.8,'country':0.8,'consoles':0.8,'platforms':0.7,
						'previous':0.8,'veteran':0.9,'pro':0.8, 'features':0.8,'player':0.7, 'amateur':0.9,
						'professional':0.9, 'finalist':0.65, 'dancers':0.7,'buyer': 0.7,'target': 0.7, 'difference': 0.8, 'if': 0.56},


	'Bodily image and Appearance': {'bodily':1.0, 'image': 0.6, 'appearance': 1.0, 'hair':0.75, 'anorexia':0.8, 'anorexic':0.8, 'handicapped': 0.75,'physical': 0.9,'self-concept': 0.9,'body': 0.95,'limb': 0.6,
									'clothes': 0.8,'boots':0.75,'dress':0.8,'workout':0.65, 'eat':0.7, 'outfit':0.75,'muscles':0.75,'healthy':0.8,'make-up': 0.7,'impairment': 0.65,'acne':0.8,'ugly':0.8,'beautiful':0.8,
									'fat':0.9,'beard':0.70 ,'skinny':0.9, 'exercise':0.6, 'weight':0.8},
	
	'Concentration': {'aware': 0.8,'awake': 0.75,'alert': 0.8,'performance': 0.6,'think':0.56,'memory':0.56,'distractible':0.7,'learn':0.56,'focus': 0.75,'pressure': 0.65,'insomnia': 0.8,'epilepsy': 0.8,'dementia': 0.8,
					'alcohol': 0.7,'attention': 0.75, 'cognitive': 0.7, 'synchronized':0.65,'choreography':0.7,'concentration': 1.0},
	
	'Energy': {'energy': 1.0, 'alive': 0.6, 'endurance': 0.8, 'sweat':0.75, 'hyperactivy':0.8,'choreography':0.7,'calorie':0.9, 'stamina':0.85, 'vitality':0.8, 'animation':0.75,'exercise':0.8, 'strong':0.75,'enthusiasm': 0.75, 'dance':0.76, 'workout':0.9},
	
	'Fatigue': {'fatigue': 1.0, 'overexertion': 0.8, 'depression': 0.8, 'cramps':0.75, 'vomit':0.75, 'panic':0.65,'weariness': 0.8, 'anorexia':0.8, 'disorder':0.7,'anxiety': 0.8,'sedentary':0.65,'stress': 0.75, 'disease': 0.95, 'illness': 0.8,'tire': 0.56,
				'tired': 0.9, 'exhaustion': 0.8},
	
	'Learning': {'cognitive': 0.6, 'school': 0.6,'knowledge': 0.56,'teach': 0.70,'concentration':0.56,'memory':0.56,'think':0.56, 'dyscalculia': 0.7,
				'dysgraphia': 0.6,'dyslexia': 0.6,'pedagogy': 0.56, 'learn': 1.0},
	
	'Memory': {'forget': 0.8, 'alzheimer': 0.8, 'old': 0.75, 'remind': 0.85, 'dementia': 0.8,'parkinson': 0.8,'korsakoff': 0.8,'huntington': 0.8,'autism': 0.8,'nostalgia':0.9, 'remember':0.85, 'memory': 1.0, 'cognitive': 0.7},
	
	'Negative feelings': {'negative':0.6, 'feeling': 0.6, 'regardless': 0.56,'despair': 0.8,'apathy': 0.8,'regret': 0.8, 'disapproval': 0.8,'agressiveness': 0.8,'remorse': 0.8,'contempt': 0.8,'disgust': 0.8,'annoy': 0.8,'shame': 0.8,'sad': 0.8,
						'cry': 0.8,'depression': 0.9,'distress': 0.9,'frustration': 0.9, 
						'antidepressant': 0.8,'suicide': 0.8,'nauseated':0.65,'lonely': 0.8,'hopeless': 0.8,'fear': 0.8,'pout': 0.75, 'boring':0.7, 'lack': 0.56,'angry':0.85, 'sucks': 0.7,'humiliation':0.8, 'anger': 0.8,
						'anxiety': 0.8,'nervousness': 0.8,'tearfulness': 0.8,'sadness': 0.8,'guilt': 0.8,'despondency': 0.8},
	
	'Pain and Discomfort': {'pain': 1.0, 'discomfort': 1.0,'worthlessness': 0.7,'depression': 0.77,'vomit':0.7, 'sad': 0.8,'grief': 0.8,'distress': 0.9,'panic': 0.8,'sore':0.75, 'sneeze':0.7, 'nauseated':0.7,
						'fracture': 0.65,'cramp': 0.75,'injury': 0.8,'toothache': 0.9,'binge':0.7,'bulimarexia':0.7,'headache': 0.9,'ache': 0.9,'disorder':0.75,'stiffness': 0.9,'drug': 0.75,
						'unpleasant': 0.8}, 
	
	'Personal relationships': {'personal': 1.0, 'homosexual': 0.7,'relationship': 0.85,'talk': 0.8,'heterosexual': 0.7,'marriage': 0.7,'friendship': 0.8,'hug': 0.8,
							'intimate': 0.7,'love': 0.56,'support': 0.65,'people': 0.65,'who':0.65,'kiss':0.65,'everybody':0.65, 'partner':0.8, 'partnership': 0.8,'share':0.7 ,'companionship': 0.75,'friend': 0.9, 'family': 0.9, 'alone': 0.9},
	
	'Positive feelings': {'positive': 0.6, 'feeling': 0.6,'optimism': 0.8,'contentment': 0.7,'euphoria': 0.8,'enthusiastic': 0.7,'admiration': 0.7,'confidence': 0.8,'affection': 0.7,'relief': 0.8,
						'satisfaction': 0.8,'altruism': 0.75,'beautiful':0.7, 'awesome':0.8, 'amusement': 0.8,'pride': 0.75,'gratitude': 0.75,'serenity': 0.75,'interest': 0.7,'inspiration': 0.7,'romance': 0.7,'hope': 0.7,
						'love': 0.8,'fun': 0.8,'enjoyment': 0.8,'relax':0.7,'calm':0.7, 'grin':0.70,'happy': 0.8,'peace': 0.75},
	
	'Self-esteem': {'self':1.2, 'esteem': 0.98, 'self-esteem':1.0,'meaningful': 0.9,'anxiety': 0.8,'guilt': 0.8,'despondency': 0.8,'depression': 0.9,'tearfulness': 0.8, 'regret': 0.8, 'appearance':0.85,'shame': 0.8,'enthusiastic':0.78,
				'inspired':0.75,'distressed': 0.86,'strong': 0.85,'proud': 0.9,'confidence': 0.85,'narcissisism': 0.9,
				'superiority': 0.8,'honour': 0.8,'egoism': 0.9,'pride': 0.8,'arrogance': 0.9,
				'admiration': 0.8,'prestige': 0.8, 'wellbeing': 0.9,'ashamed': 0.9,'guilty': 0.9,'fat':0.73,'ugly':0.75,'worthless': 0.8,'think':0.56,'regard': 0.8,'alone':0.7, 'respect': 0.75, 'competence': 0.65,'belong': 0.65,'identity': 0.65,'security': 0.6,
				'acceptance': 0.75,'worth': 0.7,'appraisal': 0.9,'dignity': 0.95,'grin':0.65,'disgust':0.70,'fear':0.75,'sadness':0.75,
				'family': 0.7,'embarrassment':0.9, 'unloved':0.75,'achievement':0.7,
				'win':0.8,'lose':0.8,'love':0.56, 'awe': 0.7,'happy':0.7,'morality':0.7, 'creativity':0.65, 'spontaneity':0.7, 'prejudice':0.7,
				'integrity':0.7,'triumph':0.8, 'despair':0.8,'worthy':0.7,'oneself': 0.8,'healthy':0.7,'satisfaction': 0.7},
	
	'Sexual activity': {'sexual':0.95, 'sex':1.0,'intimacy': 0.6},
	
	'Sleep and Rest': {'sleep': 1.0,'wake':0.85, 'parasomnia': 0.8,'hypersomnia': 0.8,'yawn':0.7, 'nightmare':0.8, 'restless':0.65, 'apnea': 0.8,'insomnia': 0.8,'refreshment': 0.6,'rest': 1.0},
	
	'Social support': {'social':1.0, 'support': 0.90, 'ask':0.75, 'share': 0.7,'talk': 0.7,'teach': 0.85,'companionship':0.9,'empathy':0.9,'sympathy':0.9,'esteem':0.8,'solve': 0.65,'relationship': 0.95,
					'handshake':0.7,'roommate': 0.95, 'thanks': 0.75,'inclusive':0.7, 'help': 0.9,'chill': 0.6,'dude': 0.67,'friend': 0.9,'abuse': 0.6,
					'personal': 0.8,'crisis': 0.6, 'trust':0.5, 'care':0.6, 'group':0.7,'collab':0.7,'community':0.75,'suggestions':0.75, 'encourage':0.75, 'advice':0.85, 
					'assistance': 0.85,'together':0.8,'kiss': 0.65,'family': 0.9},
	
	'Thinking': {'think': 1.0,'aware': 0.8,'awake': 0.8,'cognitive': 0.7,'remind':0.56,'concentration':0.56,'memory':0.5,'learn':0.6,'echolalia': 0.7,'distractible':0.7, 'speech': 0.7,'alogia': 0.75,
				'idea': 0.65,'decision': 0.6, 'choreography':0.7},

	#'Thinking, learning, memory and concentration': {'thinking': 1.0, 'aware': 1.0,'awake': 1.0,'alert': 1.0,'cognitive': 1.0,'thought': 1.0,'decisions': 1.0,'forget': 1.0, 'learning': 1.0, 'memory': 1.0, 'concentration': 1.0},
		
}











