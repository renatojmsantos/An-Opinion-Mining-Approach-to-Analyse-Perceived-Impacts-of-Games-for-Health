

from vocabulary import *
import pandas as pd

def results():
	df = pd.read_csv('FORMS-WHOQOL100.csv')

	#print(df.head())
	#print(df.columns.values)
	#print(len(df.columns.values))
	
	dictQoLquestions = {}
	dictConcepts = {}


	#questions = ['q1', 'q2', 'q3', 'q6', 'q9', 'q11', 'q17', 'q20', 'q21', 'q23', 'q27', 'q28', 'q29', 'q30', 'q31', 'q32']

	# {1: {Energy: 3, Pain: 2}, 2: {} }
	# {q1: 7, q2: 8}
	for i in df.columns.values:
		#print(i)
		#print(i[:2].split())
		for nr in range(1,33):
			#print(nr)
			if ((str(nr) in i[:2].split())):
				q = "q"+str(nr)
				q_nr = q
				#print(q)
				q = df[i]

				#contaConceitos = 0
				count = 0
				person = 0
				
				#if (q_nr in questions):
					#print(q_nr)
				for res in q:
					person+=1
					#print(person)
					#print(type(res))
					if (isinstance(res, str)):
						#q1 = df['1']
						for d in dictFields.items():
							#field = d[0]
							conceitos = d[1]
							#print(d[1])
							#contaConceitos = 0
							for c in conceitos:
								c = c.lower()
								res = res.lower()
								contaConceitos = 0
								if (c in res):
									#print("oi")
									contaConceitos+=1
									#print(c,"-->",res)
									if q_nr not in dictQoLquestions.keys():
										dictQoLquestions[q_nr] = contaConceitos
									else:
										dictQoLquestions[q_nr] += contaConceitos
										
	return dictQoLquestions

def validate():
	questions = []
	d = results()
	print(d)
	count = 0
	for c,v in d.items():
		#print(v)
		if (v > 13): # 17 -> 16
			count+=1
			#print (c)
			questions.append(c)
	print(questions)
	print(count)

validate()
