
# ver artigo CHI 13, table 8

# https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8860063
"""
First of all, thank you for your availability to contribute to this validation. 
This work is performed in the scope of the dissertation of Renato Santos in the context of the Dissertation "Analysing Usability, User Experience, and Perceived Health Impacts of Games for Health based on Users Opinion Mining" of Master in Computer Science in University of Coimbra, under supervision of Professor Paula Alexandra Silva and Professor Joel Perdiz Arrais. 

In this work we intend to validate the WHOQOL-100 questionnaire, focusing on dimensions of physical ability, mental well-being, and social relationships, to annotate theese concepts in user's comments from YouTube videos related with Just Dance game, in order to analyse "perceived" Health impacts.

In this questionnaire, the aim is to understand what annotation would be made by a specialist in at least one of the three areas of action under study. 
For example, given the comment: "During this quarantine, Just Dance was my buddy. It helped me a lot to stay active and to strengthen friendships with my teammates.", it may annotate concepts like "energy", "self-esteem", "personal relationships".

We would like the honour of having at least 10 comments annoted, but if possible all 32 comments present here.

By proceeding, you agree to the collection of information requested for further analysis in this study.
"""


# ... First, you’d need to define a list of words, one for each topic (e.g for billing issues, words like price, charge, invoice, and transaction, and for app features, words like usability, bugs and performance). 
#  queries tagged with Bug Issues and Software, or containing expressions such as ‘strange glitch’ and ‘app isn’t working’ would be sent to the dev team.

# https://monkeylearn.com/blog/introduction-to-topic-modeling/



# rule based with lexicon aproach ... requer mais esforço humano e um conhecimento dos termos em estudo

# ML requer um data enorme anotado... o que é despendioso

"""
--> TER  DOIS DICTS :
		-> um com os conceitos e palavras associadas: este é que percorre os comentários
		-> outro com os fields e conceitos: este é só no final com os resultados obtidos !!!!!

"""


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
			'Pain and discomfort', 
			'Energy',
			'Fatigue',
			'Sleep and rest',
			'Positive feelings',
			#'Thinking, learning, memory and concentration': {'thinking': 1.0, 'aware': 1.0,'awake': 1.0,'alert': 1.0,'cognitive': 1.0,'thought': 1.0,'decisions': 1.0,'forget': 1.0, 'learning': 1.0, 'memory': 1.0, 'concentration': 1.0},
			'Thinking',
			'Learning',
			'Memory',
			'Concentration',
			'Self-esteem',
			'Bodily image and appearance',
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
		
	'Efficiency': {'efficiency': 1.0, 'perfect': 0.9, 'delete':0.8,'load':0.8,'difficult':0.8,'lock':1.0,'slow':1.0,'limit':1.0, 'fast':1.0, 'ability':0.8,'works well': 1.0}, 
	'Errors/Effectiveness': {'errors': 1.0,'effectiveness':1.0, 'error':0.8,'excellent':0.8,'difficult': 1.0, 'waste':1.0,'easy':1.0,'problem':1.0,'miss':1.0,'crash':0.8,'mistake':0.8,'freeze':0.8,'trouble':0.8,'wrong':1.0,'fix': 0.8, 'incompetent': 0.2, 'broken': 0.7,'camera': 0.7, 'glitch': 0.8,'issu': 0.8, 'lag': 0.8,'bug': 0.8, 'inconsist': 0.8},
	'Learnability': {'learnability': 1.0, 'learn': 1.0, 'intuit': 1.0, 'ability':0.8,'easier': 1.0,'figur': 0.8,'straightforward': 0.8,'foreword': 0.8, 'practic': 0.6}, 
	'Memorability': {'memorability':0.8,'memory': 1.0, 'excellent':0.8,'i heard':0.9, 'forgot': 0.6, 'remember': 0.8}, 
	'Satisfaction': {'satisfaction':0.8,'happy': 1.0, 'fun': 1.0, 'great': 1.0, 'excellent':0.8,'very good':1.0, 'good':1.0, 'love': 1.0, 'awesome':0.8,'wonderful':0.8,'worth': 1.0, 'best': 1.0, 'recommend': 1.0, 'good': 0.8, 'favorite': 0.8, 'cool': 0.8, 'reliable':1.0,'perfect': 1.0},


	'Aesthetics and Appeal': {'aesthetics': 1.0, 'interface': 1.0, 'visualization':0.8,'visual':0.8,'nice':0.8,'pretty':0.8,'excellent':0.8,'awesome':0.8,'correct':0.8,'wonderful':0.8,'great':0.8,'taste': 1.0,'beauty': 1.0,'appreciation': 1.0,'appeal': 1.0, 'graphic':0.9, 'sound':0.9, 'song': 0.9, 'voice':0.9, 'playlist':0.9, 'music':0.9, 'soundtrack':0.9, 'effect':0.8, 'look':0.8, 'color':0.8, 'visual': 0.8, 'detail': 0.6, 'render': 0.5, 'pixel': 0.5},
	'Affect and Emotion': {'affect': 1.0, 'emotion': 1.0, 'fearless':0.7, 'hate': 1.0,'trust': 1.0,'surprise': 1.0,'fear': 1.0,'disgust': 1.0,'frustration': 0.7,'anger': 1.0,'fun': 0.8, 'enjoy': 0.8, 'addict': 0.7, 'workout': 0.7, 'excit': 0.8, 'cute': 0.8, 'nevertheless': 0.8, 'laugh': 0.8, 'annoy': 0.8},
	'Anticipation': {'anticipation': 1.0, 'expectation': 1.0},
	'Comfort': {'comfort': 1.0, 'problem':0.8,'worst':0.8,'mistake':0.8,'crash':0.8,'bad':0.8,'alert':0.8,'lock':0.8,'poor':0.8,'freeze':0.8,'slow':0.8,'physical': 0.7, 'physical comfort': 0.8, 'workout': 0.8, 'fits comfortably':0.8, 'comfy':0.8,'feeling':0.5, 'comfortably':0.8, 'cozy':0.8, 'pleasure':0.8, 'well-being':0.7, 'happy': 0.6, 'physical needs': 0.9, 'well being':0.8, 'body care':0.3, 'active body':0.9},
	'Detailed Usability': {'detailed usability': 1.0, 'great': 0.7, 'details': 0.9, 'functions': 0.9, 'satisfaction': 0.7,'usability': 0.7, 'best':0.7, 'problem': 0.7},
	'Enchantment': {'enchantment': 1.0, 'concentration': 1.0,'love': 1.0,'attention': 1.0,'liveliness': 1.0,'fullness': 1.0,'pleasure': 1.0,'disorientation': 1.0,'experience': 1.0},
	'Engagement': {'engagement': 1.0, 'free':0.8,'stop':0.8,'communicate':0.8,'correct':0.8,'connect':0.8,'improve':0.8,'challeng': 0.9, 'flow': 1.0,'skills': 1.0,'needs': 1.0,'forget': 1.0,'engaged': 1.0,'addict': 0.9, 'addition': 1.0, 'replay':0.7, 'nonstop': 0.9, 'interest':0.7},
	'Enjoyment and Fun': {'joy':0.9, 'enjoyment': 1.0, 'communicate':0.8,'easy':0.8,'cool':0.8,'happy':0.8,'hedonic': 1.0,'emotion': 1.0,'affect': 1.0,'fun': 1.0, 'younger': 0.7, 'entertain': 0.9},
	'Frustration': {'frustration': 1.0, 'irritating':0.8,'terrible':0.8,'frustrating':0.8,'harmful':0.8,'hate':0.8,'shit':0.8,'fuck this':0.8,'sucks':0.8,'horrible':0.8,'awful':0.8,'waste':0.8,'disappointed':0.8,'hardship': 1.0,'boring': 0.8, 'grrrr': 1.0,'anger': 1.0,'hardest': 0.7, 'dissadvantag': 0.8, 'insult': 0.7, 'injuri': 0.7, 'nerv': 0.7, 'unfair':0.7, 'cheat':0.7, 'annoy':0.7, 'incompatibilit':0.7},
	'Hedonic': {'hedonic': 1.0, 'fun': 0.8, 'superb':0.8,'enjoy': 0.8, 'love':0.8,'good':0.8,'super':0.8,'awesome':0.8,'happy':0.8,'friend':0.8,'communicate':0.8,'challenge':0.7, 'frustrat': 0.8, 'fulfillment': 0.9, 'needs': 0.8, 'pleasure':0.7,'enjoyment':0.7,'frustration':0.7, 'annoy': 0.8, 'entertain': 0.8, 'game': 0.8,'multiplayer': 0.8, 'gaming': 0.8, 'gameplay': 0.8, 'play': 0.8, 'humor': 0.8, 'workout': 0.8, 'nostalgia': 0.6},
	'Impact': {'impact': 1.0, 'pattern': 0.7, 'surprise': 1.0,'fear': 1.0,'change gameplay': 0.9},
	'Likeability': {'likeability': 1.0, 'like':0.9}, 
	'Motivation': {'motivation': 1.0, 'task': 1.0, 'loving':1.0, 'joy': 0.8},'pleasure':0.8,
	'Overall Usability': {'overall usability': 1.0, 'update':0.8,'feature':0.8,'new version': 0.8, 'upgrade':0.8, 'edition': 0.8, 'previous edition':0.8},
	'Pleasure': {'pleasure': 1.0, 'fun': 0.7, 'moneybag':0.7, 'enjoy': 0.7, 'love': 0.7, 'entertain': 0.7, 'awesome': 0.8, 'stimulation':0.7, 'felt': 0.7, 'sooth': 0.7, 'adict': 0.7, 'nostalgia': 0.7},
	'Support': {'support':1.0, 'help':0.8, 'service':0.8,'helpful':0.8,'team':0.8,'call':0.8,'contact':0.8,'correct':0.8,'how':1.0, 'how should':1.0, 'how can': 1.0,'how can i': 1.0,'wish': 0.7,'software': 0.7},
	'Trust': {'trust': 1.0, 'behavior': 0.8, 'disappointed':0.8,'easy':0.8,'quality':0.8,'reliable':0.8,'security':0.8,'secure':0.8,'pleasure': 0.5},
	'User Differences': {'user differences': 1.0,'user group': 0.7,'group': 0.7,'head-to-head':0.8,'beginners':0.9, 'veterans':0.9,'pro player':0.9, 'amateur':0.9,'professional':0.9,'finalists':0.6, 'professional dancers':0.8,'buyers': 0.7,'target': 0.7,'features': 0.7, 'differences': 0.7, 'if you': 0.6},


	'Bodily image and appearance': {'bodily image': 1.0, 'handicapped': 1.0,'physical handicapped': 1.0,'physical': 1.0,'body image': 1.0,'limbs': 1.0,'artificial limbs': 1.0,'clothing': 1.0,'make-up': 1.0,'impairments': 1.0,'looks': 1.0,'appearance': 0.9, 'body': 0.8},
	'Concentration': {'aware': 1.0,'awake': 1.0,'alert': 1.0,'attention': 0.9, 'cognitive': 0.8, 'concentration': 1.0},
	'Energy': {'energy': 1.0, 'alive': 1.0, 'endurance': 1.0,'enthusiasm': 0.9, 'workout':0.9},
	'Fatigue': {'fatigue': 1.0, 'overexertion': 1.0, 'depression': 1.0,'illness': 1.0,'tired': 1.0'exhaustion': 0.9},
	'Learning': {'cognitive': 1.0, 'education': 1.0,'knowledge': 1.0,'pedagogy': 1.0, 'learning': 1.0,  'learn': 1.0},
	'Memory': {'forget': 1.0, 'alzheimer': 0.7, 'dementia': 0.8,'nostalgia':0.9, 'remember':0.5, 'memory': 1.0, 'cognitive': 0.8},
	'Negative feelings': {'negative feelings': 1.0, 'disgust': 1.0, 'fear': 1.0,'lack': 1.0,'anger': 1.0,'anxiety': 1.0,'nervousness': 1.0,'despair': 1.0,'tearfulness': 1.0,'sadness': 1.0,'guilt': 1.0,'despondency': 1.0},
	'Pain and discomfort': {'pain': 1.0, 'discomfort': 1.0, 'drugs': 1.0'distressing': 1.0,'unpleasant': 1.0}, 
	'Personal relationships': {'personal relationships': 1.0, 'homosexual': 1.0,'heterosexual': 1.0,'marriage': 1.0,'friendship': 1.0,'satisfaction': 1.0,'hug': 1.0,'happy': 1.0,'emotionally': 1.0,'relationships': 1.0,'intimate': 1.0,'love': 1.0,'support': 1.0,'companionship': 1.0,'friends': 1.0, 'family': 1.0, 'alone': 1.0},
	'Positive feelings': {'positive feelings': 1.0, 'enjoyment': 1.0,'joy': 1.0,'hopefulness': 1.0,'happiness': 1.0,'peace': 1.0,'balance': 1.0,'contentment': 1.0},
	'Self-esteem': {'self-esteem': 1.0, 'meaningful': 1.0,'self-acceptance': 1.0,'dignity': 1.0,'family': 1.0,'people': 1.0,'education': 1.0,'control': 1.0,'oneself': 1.0,'satisfaction': 1.0},
	'Sexual activity': {'Sexual activity': 1.0, 'physical intimacy': 1.0,'sexual': 1.0,'desire for sex': 1.0,'sex': 0.9}
	'Sleep and rest': {'sleep': 1.0,'waking up': 1.0, 'refreshment': 1.0,'rest': 1.0},
	'Social support': {'Social support': 1.0, 'encouragement': 1.0,'solve': 1.0,'personal': 1.0,'responsability': 1.0,'assistance': 1.0,'approval': 1.0,'commitment': 1.0,'friends': 1.0,'family': 1.0},
	'Thinking': {'thinking': 1.0, 'aware': 1.0,'awake': 1.0,'cognitive': 1.0,'intelligent': 1.0,'idea': 1.0,'thought': 1.0,'decisions': 1.0},

	#'Thinking, learning, memory and concentration': {'thinking': 1.0, 'aware': 1.0,'awake': 1.0,'alert': 1.0,'cognitive': 1.0,'thought': 1.0,'decisions': 1.0,'forget': 1.0, 'learning': 1.0, 'memory': 1.0, 'concentration': 1.0},
		
}











