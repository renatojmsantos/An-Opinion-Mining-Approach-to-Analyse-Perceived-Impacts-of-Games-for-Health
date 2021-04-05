
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
		print("inserted!")
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


insertTablesConceitos()





