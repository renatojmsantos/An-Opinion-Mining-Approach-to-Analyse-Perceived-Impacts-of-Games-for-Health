import pandas as pd
import time
import csv
import unidecode
import json
import configparser
import random
import sys
import re   # regular expression
import regex

from datetime import datetime, date, timedelta
from langdetect import detect
from connectDB import *


def editionAndPlataform(title, descript):
	try:
		title = re.sub('&quot;+','',title)
		title = title.lower().strip()

		# substituir JD por Just Dance .... no titulo do video ....
		title = re.sub('jd','just dance',title)
		title = re.sub('justdance','just dance',title)
		title = re.sub('wiiu','wii u',title)
		#title = re.sub('ps2','PlayStation 2',title)
		title = re.sub('ps3','PlayStation 3',title)
		title = re.sub('ps4','PlayStation 4',title)
		title = re.sub('ps5','PlayStation 5',title)
		#title = re.sub('playstation2','PlayStation 2',title)
		title = re.sub('playstation3','PlayStation 3',title)
		title = re.sub('playstation4','PlayStation 4',title)
		title = re.sub('playstation5','PlayStation 5',title)
		title = re.sub('x360','Xbox 360',title)
		title = re.sub('xbox sx','Xbox Series X',title)
		title = re.sub('xbox ss','Xbox Series S',title)
		title = re.sub('xbox360','Xbox 360',title)
		title = re.sub('xboxone','Xbox One',title)
		title = re.sub('switch','Nintendo Switch',title)
		title = re.sub('nintendoswitch','Nintendo Switch',title)
		title = re.sub('nintendo','Nintendo Switch',title)
		title = re.sub('windows','Microsoft Windows',title)
		title = re.sub('pc','Microsoft Windows',title)
		title = re.sub('iphone','iOS',title)
		title = re.sub('apple','iOS',title)

		title = re.sub('yo-kai watch dance just dance special version','yo-kai watch dance: jd sv', title)
		title = re.sub('yo-kai watch dance just dance','yo-kai watch dance: jd sv', title)
		title = re.sub('yo-kai watch dance: just dance','yo-kai watch dance: jd sv', title)
		title = re.sub('just dance disney party','just dance: disney party',title)
		title = re.sub('just dance disney party 2','just dance: disney party 2',title)
		title = re.sub('just dance greatest hits','just dance: greatest hits',title)
		title = re.sub('just dance summer party','just dance: summer party',title)

		title = title.lower()

		#https://en.wikipedia.org/wiki/Just_Dance_(video_game_series)
		games = ['Just Dance 2', 'Just Dance 3', 'Just Dance 4', 'Just Dance 2014', 'Just Dance 2015', 'Just Dance 2016', 'Just Dance 2017', 'Just Dance 2018', 'Just Dance 2019', 'Just Dance 2020', 'Just Dance 2021','Just Dance 2022','Just Dance 2023',
				'Just Dance Wii', 'Just Dance Wii 2', 'Just Dance Wii U', 'Yo-kai Watch Dance: JD SV',
				'Just Dance Kids', 'Just Dance Kids 2', 'Just Dance Kids 2014',
				'Just Dance: Disney Party', 'Just Dance: Disney Party 2',
				'Just Dance: Greatest Hits',
				'Just Dance: Summer Party', 'Just Dance Now', 'Just Dance Unlimited']
		
		# detetar o nome do jogo no titulo do video ...
		edition=""
		serie=""
		
		for game in games:
			serie = game.lower()

			if(serie in title.lower()):
				edition=game
				#print(edition)
				if (edition == "Just Dance 2"):
					continue
				if (edition == "Just Dance Wii"):
					continue
				if (edition == "Just Dance Kids"):
					continue
				if (edition == "Just Dance Kids 2"):
					continue
				if (edition == "Just Dance: Disney Party"):
					continue
			
		if(edition == ""): 
			serie = "Just Dance"
			if(serie.lower() in title.lower()):
				edition = "Just Dance"


		platforms = ['Wii', 'Wii U', 'PlayStation 3', 'PlayStation 4', 'PlayStation 5', 'Xbox 360', 'Xbox One', 'Xbox Series X', 'Xbox Series S','iOS', 'Android', 'Nintendo Switch', 'Microsoft Windows', 'Stadia']
		platform = ""
		for p in platforms:
			c = p.lower()
			if(c in title.lower()):
				if (c == 'android' or platform == 'ios'):
					if(edition != "Just Dance Now"):
						continue
					else:
						pass
				platform = p
				if (platform == "Wii"):
					continue
				if (platform == "Xbox Series X"):
					continue
				
		if(platform == 'Android' or platform == 'iOS'):
			if (edition != "Just Dance Now"):
				platform="Unknown"
			else:
				pass

		if(platform==""):
			platform="Unknown"

		print("-> ",edition," -> ", platform)
		
		return edition,platform
	except Exception as e:
		print("get game and console ->", e)

def selectIdGame(title, descript):
	idBack = None
	conn = None
	
	try:
		idgame = editionAndPlataform(title,descript)
		edition = idgame[0]
		platform = idgame[1]

		params = config()
		conn = psycopg2.connect(**params)
		conn.autocommit = True
		cur = conn.cursor()

		query = "select game_id from game where edition='"+str(edition)+"' and platform='"+str(platform)+"'" 
		cur.execute(query)
		idBack = cur.fetchone()
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			conn.close()
	return idBack

