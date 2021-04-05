
from vocabulary import *
from connectDB import *


def insertToTable(query):
	idBack = None
	conn = None
	
	try:
		params = config()
		conn = psycopg2.connect(**params)
		conn.autocommit = True
		cur = conn.cursor()

		#cur.execute('SELECT version()')
		#db_version = cur.fetchone()
		#print(db_version)

		#print("tables")
		#query="SELECT * FROM opinion"
		#cur.execute(query)
		#print(cur.fetchone())

		#cur.execute("select * from usability")
		#print(cur.fetchone())
		query = query + " returning 1;" # duplicados deste id = 1 ????
		print(query)
		#print(tableName)
		#cur.execute(query, (tableName,))
		cur.execute(query)
		idBack = cur.fetchone()
		#print(idBack)
		conn.commit()
		#print("inserted!")
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack


def insertTablesConceitos():
	for items in dict.items():
		chave = items[0]
		conceitos = items[1]
		#print("\n",chave,conceitos)
		#print("\n>> ",chave)
		for vocabulario in conceitos.items():
			termo = vocabulario[0]
			#pals = vocabulario[1]
			#print(termo,pals)
			#print(" #", termo)
			if(chave=="Usability"):
				#insert into usability values('Satisfaction');
				query = "insert into usability values('"+termo+"')"
				#print(query)
				#tableName = "usability"
				insertToTable(query)
			elif(chave=="UX"):
				#print("ux")
				query = "insert into ux values('"+termo+"')"
				insertToTable(query)
			elif(chave == "Health"):
				#print("health")
				query = "insert into health values('"+termo+"')"
				insertToTable(query)


def insertSentiments():
	senti = ['Positive', 'Negative', 'Neutral']
	for s in senti:
		query = "insert into sentiment values('"+s+"')"
		insertToTable(query)

def insertGames():
	games = ['Just Dance','Just Dance 2', 'Just Dance 3', 'Just Dance 4', 'Just Dance 2014', 'Just Dance 2015', 'Just Dance 2016', 'Just Dance 2017', 'Just Dance 2018', 'Just Dance 2019', 'Just Dance 2020', 'Just Dance 2021',
								'Just Dance Wii', 'Just Dance Wii 2', 'Just Dance Wii U', 'Yo-kai Watch Dance: Just Dance Special Version',
								'Just Dance Kids', 'Just Dance Kids 2', 'Just Dance Kids 2014',
								'Just Dance: Disney Party', 'Just Dance: Disney Party 2',
								'Just Dance: Greatest Hits',
								'Just Dance: Summer Party', 'Just Dance Now', 'Just Dance Unlimited']

	plataforms = ['Wii', 'Wii U', 'PlayStation 3', 'PlayStation 4', 'PlayStation 5', 'Xbox 360', 'Xbox One', 'Xbox Series X', 'Xbox Series S','iOS', 'Android', 'Nintendo Switch', 'Microsoft Windows', 'Stadia']


	for game in games:
		for plataform in plataforms:
			query = "insert into game values('"+game+"', '"+plataform+"')"
			insertToTable(query)


insertSentiments()
insertTablesConceitos()
insertGames()






