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
        conn = psycopg2.connect(**params)
        """
        conn = psycopg2.connect(
                                host="localhost",
                                port="4321",
                                database="AnalysisJustDance",
                                user="postgres",
                                password="123")
		"""
        # create a cursor
        cur = conn.cursor()
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        #cur.execute('SELECT * FROM opinion')
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        #testDB()
        
        """
        insert into game values('Just Dance');
        insert into sentiment values ('Positive','0.3');
        insert into youtube values ('YouTube', 1, 'channel Ubisoft', 1,'Titulo video just dance 2020', '2020-01-02', 320321, 125, 10, 430);
        insert into opinion values (1,'just dance the best game',1,'2020-01-02','Just Dance', 'Positive', '1', True);
        select * from opinion;
        select * from sentiment;
        select * from game;
        select * from youtube;
        insert into usability values('Satisfaction');
        insert into usability values('Errors');
        insert into ux values('Trust');
        insert into opinion_usability values (1,'Errors');
        insert into opinion_ux values (1,'Trust');
        select * from usability;
        select * from opinion_usability;
        select * from opinion_ux;
        select * from health;
        select * from ux;
        """

        print("tables")
        query="SELECT * FROM opinion"
        cur.execute(query)
        print(cur.fetchone())

        #t = pd.read_sql_query(query,conn)
        #print(t)
        

	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

#if __name__ == '__main__':
#    connect()






