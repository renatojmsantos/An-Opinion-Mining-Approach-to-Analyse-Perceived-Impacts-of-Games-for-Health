
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


"""
--> TER  DOIS DICTS :
		-> um com os conceitos e palavras associadas: este é que percorre os comentários
		-> outro com os fields e conceitos: este é só no final com os resultados obtidos !!!!!

"""

dict={	
		'Usability':{
			'Memorability': {'memory': 1.0, 'forgot': 0.6, 'remember': 0.8}, 
			'Learnability': {'learnability': 1.0, 'learn': 1.0, 'intuit': 1.0, 'easier': 1.0,'figur': 0.8,'straightforward': 0.8,'foreword': 0.8, 'practic': 0.6}, 
			'Efficiency': {'efficiency': 1.0, 'perfect': 0.9, 'lock':1.0,'slow':1.0,'limit':1.0, 'fast':1.0, 'works well': 1.0}, 
			'Errors/Effectiveness': {'errors': 1.0,'effectiveness':1.0, 'difficult': 1.0, 'waste':1.0,'easy':1.0,'problem':1.0,'miss':1.0,'wrong':1.0,'fix': 0.8,'problem':0.5, 'incompetent': 0.2, 'broken': 0.7,'camera': 0.7, 'glitch': 0.8,'issu': 0.8, 'lag': 0.8,'bug': 0.8, 'inconsist': 0.8},
			'Satisfaction': {'happy': 1.0, 'fun': 1.0, 'great': 1.0, 'love': 1.0, 'worth': 1.0, 'best': 1.0, 'recommend': 1.0, 'good': 0.8, 'favorite': 0.8, 'cool': 0.8, 'reliable':1.0,'perfect': 1.0}
		},
		'UX':{
			'Aesthetics and Appeal': {'aesthetics': 1.0, 'interface': 1.0, 'taste': 1.0,'beauty': 1.0,'appreciation': 1.0,'appeal': 1.0, 'graphic':0.9, 'sound':0.9, 'song': 0.9, 'voice':0.9, 'playlist':0.9, 'music':0.9, 'soundtrack':0.9, 'effect':0.8, 'look':0.8, 'color':0.8, 'visual': 0.8, 'detail': 0.6, 'render': 0.5, 'pixel': 0.5},
			'Affect and Emotion': {'affect': 1.0, 'emotion': 1.0, 'trust': 1.0,'surprise': 1.0,'fear': 1.0,'disgust': 1.0,'frustration': 0.7,'anger': 1.0,'fun': 0.8, 'enjoy': 0.8, 'addict': 0.7, 'workout': 0.7, 'excit': 0.8, 'cute': 0.8, 'nevertheless': 0.8, 'laugh': 0.8, 'annoy': 0.8},
			'Anticipation': {'anticipation': 1.0, 'expectation': 1.0},
			'Likeability': {'likeability': 1.0, 'like':0.9}, 
			'Pleasure': {'pleasure': 1.0, 'fun': 0.7, 'moneybag':0.7, 'enjoy': 0.7, 'love': 0.7, 'entertain': 0.7, 'awesome': 0.8, 'stimulation':0.7, 'felt': 0.7, 'sooth': 0.7, 'adict': 0.7, 'nostalgia': 0.7},
			'Comfort': {'comfort': 1.0, 'physical': 0.7, 'physical comfort': 0.8, 'workout': 0.8, 'physical needs': 0.9, 'well being':0.8, 'body care':0.3, 'active body':0.9},
			'Trust': {'trust': 1.0, 'behavior': 0.8},
			'Overall Usability': {'overall usability': 1.0, 'new version': 0.8, 'upgrade':0.8, 'edition': 0.8, 'previous edition':0.8},
			'Hedonic': {'hedonic': 1.0, 'fun': 0.8, 'enjoy': 0.8, 'frustrat': 0.8, 'fulfillment': 0.9, 'needs': 0.8, 'pleasure':0.7,'enjoyment':0.7,'frustration':0.7, 'annoy': 0.8, 'entertain': 0.8, 'game': 0.8,'multiplayer': 0.8, 'gaming': 0.8, 'gameplay': 0.8, 'play': 0.8, 'humor': 0.8, 'workout': 0.8, 'nostalgia': 0.6},
			'Detailed Usability': {'detailed usability': 1.0, 'great': 0.7, 'details': 0.9, 'functions': 0.9, 'satisfaction': 0.7,'usability': 0.7, 'best':0.7, 'problem': 0.7},
			'User Differences': {'user differences': 1.0,'user group': 0.7,'group': 0.7,'beginners':0.9, 'veterans':0.9,'pro player':0.9, 'amateur':0.9,'professional':0.9,'finalists':0.6, 'professional dancers':0.8,'buyers': 0.7,'target': 0.7,'features': 0.7, 'differences': 0.7, 'if you': 0.6},
			'Support': {'support':1.0, 'help':0.8, 'how':1.0, 'wish': 0.7,'software': 0.7,},
			'Impact': {'impact': 1.0, 'pattern': 0.7, 'surprise': 1.0,'fear': 1.0,'change gameplay': 0.9},
			'Enjoyment and Fun': {'joy':0.9, 'enjoyment': 1.0, 'hedonic': 1.0,'emotion': 1.0,'affect': 1.0,'fun': 1.0, 'younger': 0.7, 'entertain': 0.9},
			'Engagement': {'engagement': 1.0, 'challeng': 0.9, 'flow': 1.0,'skills': 1.0,'needs': 1.0,'forget': 1.0,'engaged': 1.0,'addict': 0.9, 'addition': 1.0, 'replay':0.7, 'nonstop': 0.9, 'interest':0.7},
			'Motivation': {'motivation': 1.0, 'task': 1.0, 'joy': 0.8},
			'Enchantment': {'enchantment': 1.0, 'concentration': 1.0,'attention': 1.0,'liveliness': 1.0,'fullness': 1.0,'pleasure': 1.0,'disorientation': 1.0,'experience': 1.0},
			'Frustration': {'frustration': 1.0, 'hardship': 1.0,'boring': 0.8, 'anger': 1.0,'hardest': 0.7, 'dissadvantag': 0.8, 'insult': 0.7, 'injuri': 0.7, 'nerv': 0.7, 'unfair':0.7, 'cheat':0.7, 'annoy':0.7, 'incompatibilit':0.7},
		},
		'Health':{
			'Pain and discomfort': {'pain': 1.0, 'distressing': 1.0,'unpleasant': 1.0,'discomfort': 1.0}, 
			'Energy': {'energy': 1.0, 'alive': 1.0, 'endurance': 1.0,'enthusiasm': 0.9, 'workout':0.9},
			'Fatigue': {'fatigue': 1.0, 'exhaustion': 0.9},
			'Sleep and rest': {'sleep': 1.0,'waking up': 1.0, 'refreshment': 1.0,'rest': 1.0},
			'Positive feelings': {'positive feelings': 1.0, 'enjoyment': 1.0,'joy': 1.0,'hopefulness': 1.0,'happiness': 1.0,'peace': 1.0,'balance': 1.0,'contentment': 1.0},
			#'Thinking, learning, memory and concentration': {'thinking': 1.0, 'aware': 1.0,'awake': 1.0,'alert': 1.0,'cognitive': 1.0,'thought': 1.0,'decisions': 1.0,'forget': 1.0, 'learning': 1.0, 'memory': 1.0, 'concentration': 1.0},
			'Thinking': {'thinking': 1.0, 'aware': 1.0,'awake': 1.0,'cognitive': 1.0,'intelligent': 1.0,'idea': 1.0,'thought': 1.0,'decisions': 1.0},
			'Learning': {'cognitive': 1.0, 'education': 1.0,'knowledge': 1.0,'pedagogy': 1.0, 'learning': 1.0,  'learn': 1.0},
			'Memory': {'forget': 1.0, 'alzheimer': 0.7, 'dementia': 0.8,'nostalgia':0.9, 'remember':0.5, 'memory': 1.0, 'cognitive': 0.8},
			'Concentration': {'aware': 1.0,'awake': 1.0,'alert': 1.0,'attention': 0.9, 'cognitive': 0.8, 'concentration': 1.0},
			'Self-esteem': {'self-esteem': 1.0, 'meaningful': 1.0,'self-acceptance': 1.0,'dignity': 1.0,'family': 1.0,'people': 1.0,'education': 1.0,'control': 1.0,'oneself': 1.0,'satisfaction': 1.0},
			'Bodily image and appearance': {'bodily image': 1.0, 'handicapped': 1.0,'physical handicapped': 1.0,'physical': 1.0,'body image': 1.0,'limbs': 1.0,'artificial limbs': 1.0,'clothing': 1.0,'make-up': 1.0,'impairments': 1.0,'looks': 1.0,'appearance': 0.9, 'body': 0.8},
			'Negative feelings': {'negative feelings': 1.0, 'disgust': 1.0, 'fear': 1.0,'lack': 1.0,'anger': 1.0,'anxiety': 1.0,'nervousness': 1.0,'despair': 1.0,'tearfulness': 1.0,'sadness': 1.0,'guilt': 1.0,'despondency': 1.0},
			'Personal relationships': {'personal relationships': 1.0, 'homosexual': 1.0,'heterosexual': 1.0,'marriage': 1.0,'friendship': 1.0,'satisfaction': 1.0,'hug': 1.0,'happy': 1.0,'emotionally': 1.0,'relationships': 1.0,'intimate': 1.0,'love': 1.0,'support': 1.0,'companionship': 1.0,'friends': 1.0, 'family': 1.0, 'alone': 1.0},
			'Social support': {'Social support': 1.0, 'encouragement': 1.0,'solve': 1.0,'personal': 1.0,'responsability': 1.0,'assistance': 1.0,'approval': 1.0,'commitment': 1.0,'friends': 1.0,'family': 1.0},
			'Sexual activity': {'Sexual activity': 1.0, 'physical intimacy': 1.0,'sexual': 1.0,'desire for sex': 1.0,'sex': 0.9}
		}
	}