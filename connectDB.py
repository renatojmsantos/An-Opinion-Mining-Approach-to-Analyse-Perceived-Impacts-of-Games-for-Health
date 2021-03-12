import psycopg2
#from config import config
from configparser import ConfigParser
import pandas as pd

def config(filename='db_credentials.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        #conn = psycopg2.connect(**params)

        """
        conn = psycopg2.connect(
                                host="127.0.0.1",
                                port="5432",
                                database="AnalysisJustDance",
                                user="postgres",
                                password="123")
        """
        conn = psycopg2.connect(
                                host="localhost",
                                port="4321",
                                database="AnalysisJustDance",
                                user="postgres",
                                password="123")
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        #cur.execute('SELECT * FROM opinion')
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        

        print("tables")
        query="SELECT * FROM opinion"
        
        t = pd.read_sql_query(query,conn)
        print(t)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()