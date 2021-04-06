
from vocabulary import *
from connectDB import *

#CREATE DATABASE dbname;

def createTable(table, sql):
    idBack = None
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        #conn.autocommit = True
        cur = conn.cursor()

        #query = "SELECT videoid FROM youtube WHERE videoid = '"+ videoid +"' "
        query = "DROP TABLE IF EXISTS "+table+" CASCADE;"
        print(query)
        cur.execute(query)

        
        print(sql)
        cur.execute(sql)
        print("Table created !! ")
        
        #idBack = cur.fetchone()
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("ERRO!", error)
    finally:
        if conn is not None:
            #print("closing connection...")
            conn.close()
    return idBack is not None #idBack

def createTables():
	sql = '''CREATE TABLE youtube (
	channelid		 VARCHAR(512),
	channeltitle	 VARCHAR(512),
	videoid		 VARCHAR(512) NOT NULL,
	videotitle	 VARCHAR(512) NOT NULL,
	datevideo		 DATE,
	viewsvideo	 BIGINT,
	likesvideo	 INTEGER,
	dislikesvideo	 INTEGER,
	totalcommentsvideo BIGINT,
	description	 VARCHAR(10000),
	PRIMARY KEY(videoid)
	)'''
	table = 'youtube'
	createTable(str(table),sql)

	sql = '''CREATE TABLE opinion (
	commentid		 VARCHAR(512),
	comment		 VARCHAR(4096) NOT NULL,
	likes		 NUMERIC(8,2) NOT NULL,
	datecomment	 DATE NOT NULL,
	maincomment	 BOOL,
	game_name		 VARCHAR(512) NOT NULL,
	game_platform	 VARCHAR(512) NOT NULL,
	sentiment_polarity VARCHAR(512) NOT NULL,
	youtube_videoid	 VARCHAR(512) NOT NULL,
	PRIMARY KEY(commentid)
	)'''
	table = 'opinion'
	createTable(str(table),sql)

	sql = '''CREATE TABLE sentiment (
	polarity VARCHAR(512),
	PRIMARY KEY(polarity)
	)'''
	table = 'sentiment'
	createTable(str(table),sql)

	sql = '''CREATE TABLE usability (
	uconcept VARCHAR(512),
	PRIMARY KEY(uconcept)
	)'''
	table = 'usability'
	createTable(str(table),sql)


	sql = '''CREATE TABLE ux (
	uxconcept VARCHAR(512),
	PRIMARY KEY(uxconcept)
	)'''
	table = 'ux'
	createTable(str(table),sql)

	sql = '''CREATE TABLE health (
	hconcept VARCHAR(512),
	PRIMARY KEY(hconcept)
	)'''
	table = 'health'
	createTable(str(table),sql)

	sql = '''CREATE TABLE game (
	name	 VARCHAR(512),
	platform VARCHAR(512),
	PRIMARY KEY(name,platform)
	)'''
	table = 'game'
	createTable(str(table),sql)

	sql = '''CREATE TABLE opinion_ux (
		opinion_commentid VARCHAR(512),
		ux_uxconcept	 VARCHAR(512),
		PRIMARY KEY(opinion_commentid,ux_uxconcept)
	)'''
	table = 'opinion_ux'
	createTable(str(table),sql)


	sql = '''CREATE TABLE opinion_health (
		opinion_commentid VARCHAR(512),
		health_hconcept	 VARCHAR(512),
		PRIMARY KEY(opinion_commentid,health_hconcept)
	)'''
	table = 'opinion_health'
	createTable(str(table),sql)


	sql = '''CREATE TABLE opinion_usability (
		opinion_commentid	 VARCHAR(512),
		usability_uconcept VARCHAR(512),
		PRIMARY KEY(opinion_commentid,usability_uconcept)
	)'''
	table = 'opinion_usability'
	createTable(str(table),sql)


def alterTable(query):
	idBack = None
	conn = None
	
	try:
		params = config()
		conn = psycopg2.connect(**params)
		conn.autocommit = True
		cur = conn.cursor()

		#query = query + " returning 1;" # duplicados deste id = 1 ????
		print(query)
		#print(tableName)
		#cur.execute(query, (tableName,))
		cur.execute(query)
		#idBack = cur.fetchone()
		#print(idBack)
		conn.commit()
		print("alter table!")
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO! ", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack

def alterTables():
	sql = "ALTER TABLE opinion ADD CONSTRAINT opinion_fk3 FOREIGN KEY (sentiment_polarity) REFERENCES sentiment(polarity);"
	alterTable(sql)
	sql = "ALTER TABLE opinion ADD CONSTRAINT opinion_fk4 FOREIGN KEY (youtube_videoid) REFERENCES youtube(videoid);"
	alterTable(sql)
	sql = "ALTER TABLE opinion_ux ADD CONSTRAINT opinion_ux_fk1 FOREIGN KEY (opinion_commentid) REFERENCES opinion(commentid);"
	alterTable(sql)
	sql = "ALTER TABLE opinion_ux ADD CONSTRAINT opinion_ux_fk2 FOREIGN KEY (ux_uxconcept) REFERENCES ux(uxconcept);"
	alterTable(sql)
	sql = "ALTER TABLE opinion_health ADD CONSTRAINT opinion_health_fk1 FOREIGN KEY (opinion_commentid) REFERENCES opinion(commentid);"
	alterTable(sql)
	sql = "ALTER TABLE opinion_health ADD CONSTRAINT opinion_health_fk2 FOREIGN KEY (health_hconcept) REFERENCES health(hconcept);"
	alterTable(sql)
	sql = "ALTER TABLE opinion_usability ADD CONSTRAINT opinion_usability_fk1 FOREIGN KEY (opinion_commentid) REFERENCES opinion(commentid);"
	alterTable(sql)
	sql = "ALTER TABLE opinion_usability ADD CONSTRAINT opinion_usability_fk2 FOREIGN KEY (usability_uconcept) REFERENCES usability(uconcept);"
	alterTable(sql)

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
	dimension_id =0
	for items in dict.items():
		chave = items[0]
		conceitos = items[1]
		#print("\n",chave,conceitos)
		#print("\n>> ",chave)
		for vocabulario in conceitos.items():
			dimension_id+=1
			termo = vocabulario[0]
			#pals = vocabulario[1]
			#print(termo,pals)
			#print(" #", termo)
			if(chave=="Usability"):
				#insert into usability values('Satisfaction');
				#query = "insert into usability values('"+termo+"')"
				query = "insert into dimension values('"+str(dimension_id)+"', '"+chave+"', '"+termo+"')"
				#print(query)
				#tableName = "usability"
				insertToTable(query)
			elif(chave=="UX"):
				#print("ux")
				#query = "insert into ux values('"+termo+"')"
				query = "insert into dimension values('"+str(dimension_id)+"', '"+chave+"', '"+termo+"')"
				insertToTable(query)
			elif(chave == "Health"):
				#print("health")
				#query = "insert into health values('"+termo+"')"
				query = "insert into dimension values('"+str(dimension_id)+"', '"+chave+"', '"+termo+"')"
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

	plataforms = ['Unknown','Wii', 'Wii U', 'PlayStation 3', 'PlayStation 4', 'PlayStation 5', 'Xbox 360', 'Xbox One', 'Xbox Series X', 'Xbox Series S','iOS', 'Android', 'Nintendo Switch', 'Microsoft Windows', 'Stadia']

	game_id = 0
	for game in games:
		for plataform in plataforms:
			game_id += 1
			#query = "insert into game values('"+game+"', '"+plataform+"')"
			query = "insert into game values('"+str(game_id)+"', '"+game+"', '"+plataform+"')"
			insertToTable(query)



#createTables()
#alterTables()

#insertSentiments()
insertTablesConceitos()
insertGames()






