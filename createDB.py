from connectDB import *

#CREATE DATABASE dbname;

def checkVideoID(videoid):
    idBack = None
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        #conn.autocommit = True
        cur = conn.cursor()

        query = "SELECT videoid FROM youtube WHERE videoid = '"+ videoid +"' "
        #print(query)
        cur.execute(query)

        idBack = cur.fetchone()
        #print(idBack)
        #conn.commit()
        #print("inserted!")
        
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("ERRO!", error)
    finally:
        if conn is not None:
            #print("closing connection...")
            conn.close()
    return idBack is not None #idBack