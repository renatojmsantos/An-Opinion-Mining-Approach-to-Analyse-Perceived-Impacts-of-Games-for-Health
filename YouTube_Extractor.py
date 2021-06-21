#import os
#from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

from langdetect import detect

import time
import csv
import unidecode
#import requests

#import httplib2
import json

import configparser
import random

from connectDB import *

import sys

from preprocessing import *
from annotation import * 

from datetime import datetime, date, timedelta


YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

listaKeys = []

etlID = 0


def insertToTable(query):
	idBack = None
	conn = None
	
	try:
		params = config()
		conn = psycopg2.connect(**params)
		conn.autocommit = True
		cur = conn.cursor()

		
		query = query + " returning 1;" # duplicados deste id = 1 ????
		#print(query)
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


def readKeys(filename='dev_keys.txt'):
	with open(filename) as file:
		for line in file:
			listaKeys.append(line.strip())
	
readKeys()


def checkVideoID(videoid): # CHECK VIDEO ID DA OPINION ....
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT videoid FROM video WHERE videoid = '"+ videoid +"' "
		#print(query)
		cur.execute(query)

		idBack = cur.fetchone()		
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack is not None #idBack

def checkCommentID(commentid):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT commentid FROM comment WHERE commentid = '"+ commentid +"' "
		#print(query)
		cur.execute(query)

		idBack = cur.fetchone()		
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack is not None #idBack

def checkAnnotatedComment(commentid):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT comment_commentid FROM annotation WHERE comment_commentid = '"+ commentid +"' "
		#print(query)
		cur.execute(query)

		idBack = cur.fetchone()		
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack is not None #idBack

def countRowsTable(tableName):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT count(*) FROM "+tableName+""

		#print(query)
		cur.execute(query)
		idBack = cur.fetchone() # TUPLO
		
		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

def getLastAnnotationID():
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "select annotationid from annotation order by annotationid desc;"

		#print(query)
		cur.execute(query)
		idBack = cur.fetchone() # TUPLO
		
		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

def getLastGameID():
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "select game_id from game order by game_id desc;"

		#print(query)
		cur.execute(query)
		idBack = cur.fetchone() # TUPLO
		
		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack



def getGameID(videoid):
	
	try:
		idBack = None
		conn = None
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT game_game_id  FROM annotation where video_videoid='"+videoid+"'"
		#print(query)
		cur.execute(query)

		idBack = cur.fetchone()
		#print(idBack)
		#for row in idBack:
		#	if (row is not None):
		#		print(row)
				#idBack=row
				#return idBack 
		#print(idBack)
		#conn.commit()
		#print("inserted!")
		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO! get comments", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack
#========================================================================================================================================================================
#========================================================================================================================================================================

#gameid = countRowsTable(str('game'))# + 1
#annotationid = countRowsTable(str('annotation'))# + 1

gameid = getLastGameID()
annotationid = getLastAnnotationID()

game_id = int(gameid[0])
annotation_id = int(annotationid[0])

print("IDS = ",game_id, annotation_id)

giveDate = sys.argv[1]
interval = sys.argv[2]
sleepTime = sys.argv[3]
checkNewComments = sys.argv[4]

searchGame = sys.argv[5]

#print(searchGame)


games = ['Just Dance 2', 'Just Dance 3', 'Just Dance 4', 'Just Dance 2014', 'Just Dance 2015', 'Just Dance 2016', 'Just Dance 2017', 'Just Dance 2018', 'Just Dance 2019', 'Just Dance 2020', 'Just Dance 2021',
				'Just Dance Wii', 'Just Dance Wii 2', 'Just Dance Wii U', 'Yo-kai Watch Dance: Just Dance Special Version',
				'Just Dance Kids', 'Just Dance Kids 2', 'Just Dance Kids 2014',
				'Just Dance: Disney Party', 'Just Dance: Disney Party 2',
				'Just Dance: Greatest Hits',
				'Just Dance: Summer Party', 'Just Dance Now', 'Just Dance Unlimited']

#print(sys.argv[4])
#print(type(checkNewComments), checkNewComments)

#initialDate = str(giveDate)+'T00:00:00Z'

giveDate = giveDate.split("-")

startDate = date(int(giveDate[0]),int(giveDate[1]),int(giveDate[2]))

endYear = datetime.today().strftime('%Y')
endMonth = datetime.today().strftime('%m')
endDay = datetime.today().strftime('%d')
endDate = date(int(endYear),int(endMonth),int(endDay))

delta = endDate - startDate

before = ''
after = ''

#nowDay = datetime.today().strftime('%Y-%m-%d')
#nowHour = datetime.today().strftime('%H:%M:%S')
#nowDate = nowDay+'T'+nowHour+'Z'
#print(nowDate)

c=0


while 1:

	print("\n getting data ... ")
	for d in range(delta.days + 2):
		day = startDate + timedelta(days = d)
		if(d>(1-int(interval))):
			dayBefore = startDate + timedelta(days = d-int(interval))
		c+=1
		#print(d) #d = 0,1,2...
		if (c<int(interval)):
			continue
		elif (c==int(interval)):
			day = str(day) 
			newdate = day.split("-")
			newdate = str(newdate[0])+'-'+str(newdate[1])+'-'+str(newdate[2])+'T00:00:00Z'

			if(d>0):
				dayBefore = str(dayBefore) 
				dateBefore = dayBefore.split("-")
				dateBefore = str(dateBefore[0])+'-'+str(dateBefore[1])+'-'+str(dateBefore[2])+'T00:00:00Z'

				before = dateBefore
				after = newdate

				beginDate = before
				endDate = after

				print("\n ================== FROM: ",beginDate)
				print(" ================== TO: ",endDate+"\n")

				nextPage_token = None
				while 1:
					#beginExtract = time.time()
					try:
						random.shuffle(listaKeys)
						DEVELOPER_KEY = str(listaKeys[0])
						youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
						#print("a ir buscar...") # regionCode

						if (searchGame == 'random'):
							random.shuffle(games)
							searchGame = str(games[0])
						
						print(searchGame)

						search_response = youtube.search().list(
							publishedBefore=endDate, publishedAfter=beginDate, q=str(searchGame), part="id,snippet", order='relevance', type='video', relevanceLanguage='en', maxResults=100, 
							pageToken=nextPage_token).execute()
						# search () -> custo de 100 units... o resto é de 1 units

						nextPage_token = search_response.get("nextPageToken")
						for search_result in search_response.get("items", []):
							#print("\n###########\n")
							#print(search_result)
							
							if search_result["id"]["kind"] == "youtube#video":
								#print(search_result["snippet"])
								titulo = search_result["snippet"]["title"]
								#titulo = unidecode.unidecode(titulo)
								description = search_result["snippet"]["description"]

								
								videoName = titulo.lower()
								if ( ("lady gaga" not in videoName) and ("ladygaga" not in videoName) and ("lyric" not in videoName) and ("dialysis" not in videoName) and ("fuck it" not in videoName) and ("maristela" not in videoName) and ("killebom" not in videoName) and ("ladies free" not in videoName) and ("brand new band" not in videoName) and ("ivi adamou" not in videoName) and ("talent show" not in videoName) and ("effy" not in videoName) and ("music video" not in videoName) and ("the nanny" not in videoName) and ("josh turner" not in videoName) and ("karaoke" not in videoName) and ("quadriphonix" not in videoName) and ("acoustic" not in videoName) and ("cover" not in videoName) and ("Jerónimo de Sousa" not in videoName) and ("paul johnson" not in videoName) and ("remix" not in videoName) and ("flashmob" not in videoName) and ("ps22 chorus" not in videoName) and ("alvin" not in videoName) and ("chipettes" not in videoName) and ("chipmunk" not in videoName) and ("chipmunks" not in videoName) and ("just dance india" not in videoName) and ("official music video" not in videoName) and ("lyrics" not in videoName)
									and ("covers" not in description) and ("maristela" not in description) and ("killebom" not in description)
									and ("ivi adamou" not in description) and ("talent show" not in description) and ("music video" not in description) 
									and ("the nanny" not in description) and ("josh turner" not in description) and ("karaoke" not in description) and ("quadriphonix" not in description) and ("acoustic" not in description)
									and ("Jerónimo de Sousa" not in description) and ("paul johnson" not in description) and ("remix" not in description) and ("flashmob" not in description) and ("ps22 chorus" not in description)
									and ("chipettes" not in description) and ("chipmunk" not in description) and ("chipmunks" not in description) and ("just dance india" not in description) and ("official music video" not in description)
									and (("just dance" in videoName) or ("justdance" in videoName))):
									
									tituloChannel=search_result["snippet"]["channelTitle"]
									tituloChannel = unidecode.unidecode(tituloChannel) # tira aqui numeros????????


									idChannel=search_result["snippet"]["channelId"]
									videoPublishedAt=search_result["snippet"]["publishedAt"] #2017-02-13T02:52:38Z
									try:
										dateVideo = re.sub('T[0-9:Z]+','',videoPublishedAt)
									except Exception as e:
										#print(e)
										print("something wrong on convert dates...", e)

									#print("#############################################")
									

									videoID = search_result["id"]["videoId"]
									#print(">>>",checkVideoID(str(videoID)))

									print("\nTitulo: ", search_result["snippet"]["title"])
									#print("Descricao: ", search_result["snippet"]["description"])
									print("Video ID: ",search_result["id"]["videoId"])
									print("Published at: ",search_result["snippet"]["publishedAt"])

									#game_id = getEditionAndPlataform(game_id, titulo, description)

									if (checkVideoID(str(videoID)) is False): # videoID nao está na BD ... vai buscar todos os comentarios
										
										#newVideo = True
										#getInfoVideo(newVideo, initialDate, game_id, opinion_id, dimension_id, titulo, tituloChannel, idChannel, description, dateVideo, videoID)
										try:
											random.shuffle(listaKeys)
											DEVELOPER_KEY = str(listaKeys[0])
											yt = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
											requestStats = yt.videos().list(
													part='id,statistics', id=videoID, maxResults=100
											).execute()
											
											views = requestStats["items"][0]["statistics"]["viewCount"]

											if( (('commentCount' in requestStats["items"][0]["statistics"]) == True) and
												(('likeCount' in requestStats["items"][0]["statistics"]) == True) and
												(('dislikeCount' in requestStats["items"][0]["statistics"]) == True)
												):
												#print("Total comments video = "+requestStats["items"][0]["statistics"]["commentCount"])
												likesV = requestStats["items"][0]["statistics"]["likeCount"]
												dislikesV = requestStats["items"][0]["statistics"]["dislikeCount"]
												nrCommentsV = requestStats["items"][0]["statistics"]["commentCount"]
												#contaStatsComments += int(nrCommentsV)
											else:
												nrCommentsV=0
												likesV=0
												dislikesV=0
											
											tituloChannel = tituloChannel.replace("'","")
											description = description.replace("'","")
											query = "insert into video values('"+str(idChannel)+"', '"+str(tituloChannel)+"', '"+str(videoID)+"','"+titulo+"','"+str(dateVideo)+"', '"+str(views)+"', '"+str(likesV)+"', '"+str(dislikesV)+"', '"+str(nrCommentsV)+"', '"+str(description)+"')"
											insertToTable(query)
											
											print(game_id)
											game_id = getEditionAndPlataform(game_id, titulo, description)
											
											if(int(nrCommentsV) > 0):
												#print("getting comments of video ...")
												nextPT = None
												while 1: #comentarios do videoID
													
													try:
														random.shuffle(listaKeys)
														DEVELOPER_KEY = str(listaKeys[0])
														yt_c = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

														comment_response = yt_c.commentThreads().list(
															part='snippet,replies', videoId=videoID, maxResults=100,
															order='relevance', textFormat='plainText',pageToken=nextPT).execute()
														nextPT = comment_response.get('nextPageToken')
														for comment_result in comment_response.get("items",[]):

															comentario = comment_result['snippet']['topLevelComment']['snippet']['textDisplay']

															#comentario = "OMG I don’t expect that JD brought me behavioral abnormalities to my body and affected my self-esteem 😡😡😡"
															
															#comentario = unidecode.unidecode(comentario)
															#nrComentarios+=1
															nr_likes = comment_result['snippet']['topLevelComment']['snippet']['likeCount']
															commentID = comment_result['snippet']['topLevelComment']['id']
															#print(comment_result['snippet']['topLevelComment']['snippet']['updatedAt'])
															publishTime = comment_result['snippet']['topLevelComment']['snippet']['updatedAt']
															#print(publishTime)
															# updatedAt pq pode incluir possiveis correcoes, ao inves do comment original com "publishedAt"
															try:
																dateComment = re.sub('T[0-9:Z]+','',publishTime)
															except Exception as e:
																#print(e)
																print("something wrong on convert dates...", e)
															
															
															try:
																
																tamanhoComentario = len(comentario.split())
																#query = "INSERT into etl values("
																beginTratamento = time.time()

																comment = runPreprocessing(comentario)
																#comment = runPreprocessing("OMG I don’t expect that JD brought me behavioral abnormalities to my body and affected my self-esteem")
																#print(type(comment))
																if (comment != "None" and comment != "none" and comment is not None):
																	#print(comentario)
																	#print(comment)

																	endTratamento = time.time()
																	tempoT = endTratamento-beginTratamento
																	#query = "INSERT INTO ETL VALUES('"+str(etlID)+",'"+str(tamanhoComentario)+"NULL,'"+str(tempoT)+"', NULL, NULL,NULL"
																	#insertToTable(query)

																	#def executeAnnotation(game_id, dimension_id, opinion_id, videoID, comment, commentID, likes, dateComment, isMain):
																	isMain = "Main"
																	if(checkAnnotatedComment(str(commentID)) is False):
																		beginAnotacao = time.time()
																		annotation_id = executeAnnotation(game_id, annotation_id, videoID, comment, comentario, commentID, nr_likes, dateComment, isMain)
																		endAnotacao = time.time()

																		tempoA = endAnotacao - beginAnotacao
																		#query = "INSERT INTO ETL VALUES('"+str(etlID)+",'"+str(tamanhoComentario)+"NULL,NULL,'"+str(tempoA)+"', NULL,NULL"
																		#insertToTable(query)

																		etlID+=1
																		tempoTotal = endAnotacao - beginTratamento
																		query = "INSERT INTO ETL VALUES("+str(etlID)+","+str(tamanhoComentario)+",NULL,"+str(tempoT)+","+str(tempoA)+","+str(tempoTotal)+",NULL)"
																		insertToTable(query)

																	#print(".... id's --> ",opinion_id, dimension_id) # nao aumentam depois.... colocar aqui toda a anotacao do execute? ou return ID's ... em tuplo..? 

																	nr_replies = comment_result['snippet']['totalReplyCount']
																	#print(" . . . replies stats = ", nr_replies)
																	countReplies = 0

																	nextPTreply = None #page token
																	if (nr_replies > 0):
																		try:
																			random.shuffle(listaKeys)
																			DEVELOPER_KEY = str(listaKeys[0])
																			yt_r = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

																			while (countReplies <= nr_replies):
																				commentsReplies = yt_r.comments().list(
																					parentId = commentID, part='id,snippet', maxResults=100, pageToken=nextPTreply).execute()
																				nextPTreply = commentsReplies.get('nextPageToken')

																				if(nextPTreply is None):
																					break

																				for r in commentsReplies.get("items",[]):
																					#print(r)
																					replyID = r['id']
																					textReply = r['snippet']['textDisplay']
																					likesReply = r['snippet']['likeCount']
																					publishedAtReply = r['snippet']['updatedAt']

																					try:
																						dateReply = re.sub('T[0-9:Z]+','',publishedAtReply)
																					except Exception as e:
																						#print(e)
																						print("something wrong on convert dates...", e)
																				
																					countReplies+=1
																					
																					try:
																						commentReply = runPreprocessing(textReply)
																						if (commentReply != "None" and commentReply != "none" and commentReply is not None):
																							#game_id, dimension_id, opinion_id, title, videoID, comment, commentID, likes, dateComment, isMain, dateVideo, views, likesVideo, dislikesVideo,totalCommentsVideo, descript, channel, channelID
																							isMain = "Reply"
																							if(checkAnnotatedComment(str(replyID)) is False):
																								annotation_id = executeAnnotation(game_id, annotation_id, videoID, commentReply, textReply, replyID, likesReply, dateReply, isMain)
																							#opinion_id = ids[0]
																							#annotation_id = ids
																							#print(".... id's --> ", opinion_id, dimension_id)
																					except Exception as e:
																						print("replys -", e)	
																		except HttpError as e:
																			print("comments() - replies — An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
																			if("quotaExceeded" in str(e.content)):
																				time.sleep(0.1)
																		#except (ConnectionError, ReadTimeout):
																			#print("ERROR! Connection or TIME OUT!")
																		except Exception as e:
																			print("get replys - ", e)
																			#print("comments() - replies — something wrong ...")
																	else:
																		continue
																#print(" . . . replies lidos = ",countReplies)
																else:
																	#skip statements inside the loop
																	continue
															except Exception as e:
																print("comments -", e)

														if nextPT is None:
															#time.sleep(5)
															#print(". . . nr comentarios total = ",nrComentarios)
															#print(". . . stats total comentarios = ", contaStatsComments)
															break

													except HttpError as e:
														print("commentThreads() — An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
														#commentsDisabled
														if("quotaExceeded" in str(e.content)):
															print("SEM QUOTA")
															time.sleep(0.1)
														if("commentsDisabled" in str(e.content)):
															print("COMENTARIOS DESATIVADOS...")
															break
													#except (ConnectionError, ReadTimeout):
														#print("ERROR! Connection or TIME OUT!")
													except Exception as ex:
														print("commentThreads() - ", ex)
											else:
												#print("NO COMMENTS!")
												#break
												continue
												#pass        
										except HttpError as e:
											print("videos (stats) — An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
											if("quotaExceeded" in str(e.content)):
												time.sleep(0.1) #6h
										#except (ConnectionError, ReadTimeout):
											#print("ERROR! Connection or TIME OUT!")
										except Exception as e:
											print("videos (stats) ", e)
											#print("videos (stats) - something wrong ...")
									else:
										print("	 >>> video já inserido na BD...")
										
										#updateInfoGame()... get videoID do annotationid... to get gameid

										"""
										gameid = getGameID(videoID)
										print(gameid)
										if (gameid is not None):
											gameid = int(gameid[0])
											updateEditionAndPlataform(gameid, titulo, description)
										"""
										
										# update views, likes... ??

										if (checkNewComments == "True"):
											# vai atualizar os comentarios do video...

											#select game_id from game where titulo, description == XXXXX XXXX 
											#game_id = getEditionAndPlataform(game_id, titulo, description)
											try:
												random.shuffle(listaKeys)
												DEVELOPER_KEY = str(listaKeys[0])
												yt = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
												requestStats = yt.videos().list(
														part='id,statistics', id=videoID, maxResults=100
												).execute()
												
												views = requestStats["items"][0]["statistics"]["viewCount"]

												if(('commentCount' in requestStats["items"][0]["statistics"]) == True):
													nrCommentsV = requestStats["items"][0]["statistics"]["commentCount"]
													#contaStatsComments += int(nrCommentsV)
												else:
													nrCommentsV=0
												
												if(int(nrCommentsV) > 0):

													nextPT = None
													while 1: #comentarios do videoID
														try:
															random.shuffle(listaKeys)
															DEVELOPER_KEY = str(listaKeys[0])
															yt_c = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

															comment_response = yt_c.commentThreads().list(
																part='snippet,replies', videoId=videoID, maxResults=100,
																order='relevance', textFormat='plainText',pageToken=nextPT).execute()
															nextPT = comment_response.get('nextPageToken')
															for comment_result in comment_response.get("items",[]):

																commentID = comment_result['snippet']['topLevelComment']['id']
																
																if (checkCommentID(str(commentID)) is False): # FALSE ---> n está na bd... atualizar anotacoes TRUE e comentar insert comment no executeAnnotation... falta o getEditionsEPlataforms
																	

																	comentario = comment_result['snippet']['topLevelComment']['snippet']['textDisplay']

																	#comentario = unidecode.unidecode(comentario)
																	#nrComentarios+=1
																	nr_likes = comment_result['snippet']['topLevelComment']['snippet']['likeCount']

																	#print(comment_result['snippet']['topLevelComment']['snippet']['updatedAt'])
																	publishTime = comment_result['snippet']['topLevelComment']['snippet']['updatedAt']
																	#print(publishTime)
																	# updatedAt pq pode incluir possiveis correcoes, ao inves do comment original com "publishedAt"

																	try:
																		dateComment = re.sub('T[0-9:Z]+','',publishTime)
																	except Exception as e:
																		#print(e)
																		print("something wrong on convert dates...", e)
																	
																	
																	try:
																		comment = runPreprocessing(comentario)
																		#print(type(comment))
																		if (comment != "None" and comment != "none" and comment is not None):
																			print("new comment ! ")
																			#print(comentario)
																			#print(comment)

																			#def executeAnnotation(game_id, dimension_id, opinion_id, videoID, comment, commentID, likes, dateComment, isMain):
																			isMain = "Main"
																			if(checkAnnotatedComment(str(commentID)) is False):
																				annotation_id = executeAnnotation(game_id, annotation_id, videoID, comment, comentario, commentID, nr_likes, dateComment, isMain)
																			
																			#print(".... id's --> ",opinion_id, dimension_id) # nao aumentam depois.... colocar aqui toda a anotacao do execute? ou return ID's ... em tuplo..? 

																			nr_replies = comment_result['snippet']['totalReplyCount']
																			#print(" . . . replies stats = ", nr_replies)
																			countReplies = 0

																			nextPTreply = None #page token
																			if (nr_replies > 0):
																				try:
																					random.shuffle(listaKeys)
																					DEVELOPER_KEY = str(listaKeys[0])
																					yt_r = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

																					while (countReplies <= nr_replies):
																						commentsReplies = yt_r.comments().list(
																							parentId = commentID, part='id,snippet', maxResults=100, pageToken=nextPTreply).execute()
																						nextPTreply = commentsReplies.get('nextPageToken')

																						if(nextPTreply is None):
																							break

																						for r in commentsReplies.get("items",[]):
																							#print(r)
																							replyID = r['id']
																							textReply = r['snippet']['textDisplay']
																							likesReply = r['snippet']['likeCount']
																							publishedAtReply = r['snippet']['updatedAt']

																							try:
																								dateReply = re.sub('T[0-9:Z]+','',publishedAtReply)
																							except Exception as e:
																								#print(e)
																								print("something wrong on convert dates...", e)
																						
																							countReplies+=1
																							
																							try:
																								commentReply = runPreprocessing(textReply)
																								if (commentReply != "None" and commentReply != "none" and commentReply is not None):
																									#game_id, dimension_id, opinion_id, title, videoID, comment, commentID, likes, dateComment, isMain, dateVideo, views, likesVideo, dislikesVideo,totalCommentsVideo, descript, channel, channelID
																									isMain = "Reply"
																									if(checkAnnotatedComment(str(replyID)) is False):
																										annotation_id = executeAnnotation(game_id, annotation_id, videoID, commentReply, textReply, replyID, likesReply, dateReply, isMain)
																									#opinion_id = ids[0]
																									#annotation_id = ids
																									#print(".... id's --> ", opinion_id, dimension_id)
																							except Exception as e:
																								print("replys -", e)	
																				except HttpError as e:
																					print("comments() - replies — An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
																					if("quotaExceeded" in str(e.content)):
																						time.sleep(0.1)
																				#except (ConnectionError, ReadTimeout):
																					#print("ERROR! Connection or TIME OUT!")
																				except Exception as e:
																					print("get replys - ", e)
																					#print("comments() - replies — something wrong ...")
																			else:
																				continue
																		#print(" . . . replies lidos = ",countReplies)
																		else:
																			#skip statements inside the loop
																			continue
																	except Exception as e:
																		print("comments -", e)
																else:
																	#print("comentario ja guardado...")
																	continue

															if nextPT is None:
																#time.sleep(5)
																#print(". . . nr comentarios total = ",nrComentarios)
																#print(". . . stats total comentarios = ", contaStatsComments)
																break

														except HttpError as e:
															print("commentThreads() — An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
															#commentsDisabled
															if("quotaExceeded" in str(e.content)):
																print("SEM QUOTA")
																time.sleep(0.1)
															if("commentsDisabled" in str(e.content)):
																print("COMENTARIOS DESATIVADOS...")
																break
														#except (ConnectionError, ReadTimeout):
															#print("ERROR! Connection or TIME OUT!")
														except Exception as ex:
															print("commentThreads() - ", ex)
												else:
													#sem comentarios
													continue

											except Exception as e:
												print("new comments total - ", e)
										else:
											#print("dont check new comments")
											continue

								else:
									#print(" X REJECT! lady gaga or something else\n")
									continue
						#time.sleep(0.25)
						if nextPage_token is None:
							#print("\n~~~~ nr de videos atual: ", conta)
							#endExtract = time.time()
							#tempoE = endExtract-beginExtract
							#print(tempo)
							#query = "INSERT INTO ETL VALUES("+str(etlID)+",NULL,"+str(tempoE)+",NULL,NULL, NULL, NULL)"
							#insertToTable(query)
							break #sem break, começa tudo de novo
					except HttpError as e:
						print("search() — An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
						if("quotaExceeded" in str(e.content)):
							time.sleep(0.1) #72 minutos
					#except (ConnectionError, ReadTimeout):
						#print("ERROR! Connection or TIME OUT!")
					except Exception as e:
						print("search () -", e)
						
				print("--- fim ---\n ")
			c = 0

	#nowDay = datetime.today().strftime('%Y-%m-%d')
	#nowHour = datetime.today().strftime('%H:%M:%S')
	#nowDate = nowDay+'T'+nowHour+'Z'
	#print(nowDate)
	print("end...")
	time.sleep(int(sleepTime))
	print("again...")
	#break # termina
	continue



