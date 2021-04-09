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

from datetime import datetime



YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# 4/1AY0e-g6HsBRDn9XtgpQsehXcHdI3JU-F3uOkTkI1otQJGU0oyDj4euolBg8
# 4/1AY0e-g6Ekmgnu-HotcSKXh8ESlFsQLMT-ML8TGO7jVjN1cLKsJR4EAk-Jc0

# publishedAfter and before... para ir buscar antes e depois da data X


# opcao de run raiz ou run de atualizacao constemente ... fazer .. vindo do input terminal
# run raiz -> atual
# run atualizacao -> checka novos comentarios a partir da data X... 
#                 guardar uma data temporaria, fazer sleep X e depois verificar de novo com uma data + recente
#                 ... assim monitoriza todos os videos, e caso hajam novos comentarios adiciona


listaKeys = []

def readKeys(filename='dev_keys.txt'):
	with open(filename) as file:
		#l = 0
		for line in file:
			#print(line)
			listaKeys.append(line.strip()) #without \n
	
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

def checkCommentID(commentid):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT commentid FROM opinion WHERE commentid = '"+ commentid +"' "
		#print(query)
		cur.execute(query)

		idBack = cur.fetchone()
		print(idBack)
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
	return idBack[0]# is not None #idBack


#print(countRowsTable('game'))
game_id = int(countRowsTable('game'))# + 1
opinion_id = int(countRowsTable('opinion'))# + 1
dimension_id = int(countRowsTable('dimension'))# + 1

print(".... id's --> ",game_id, opinion_id, dimension_id)


# INICIALIZAR ID'S... COUNT DA TABLE + 1
# DIMENSION_ID, OPINION_ID, GAME_ID
# ...


#writedComments = 0
#conta = 0
lista_videoID=[]


# mes a mes
newyear20=0

#before = '2009-08-01T00:00:00Z'
#after = '2010-01-01T00:00:00Z'
before = ''
after = ''

for ano in range (-1,12): #(-1,12)
	for mes in range(1,13): #todos os meses ... 11 anos * 12 meses = 132 meses
		#print(" . . . NOVO INTERVALO DE TEMPO")
		#time.sleep(60*4) #86400 = 1 dia sleep, 3600s = 1h
		#print(ano,mes)
		if(ano<10):
			if (ano == -1 and mes >= 8):
				if (mes < 10):
					before = '2009-0'+str(mes)+'-01T00:00:00Z'
					if((mes+1) == 10):
						after = '2009-'+str((mes+1))+'-01T00:00:00Z'
					else:
						after = '2009-0'+str(mes+1)+'-01T00:00:00Z'
				else:
					before = '2009-'+str(mes)+'-01T00:00:00Z'
					if(mes < 12):
						after = '2009-'+str(mes+1)+'-01T00:00:00Z'
					else:
						after = '2010-01-01T00:00:00Z'
			elif (ano == -1 and mes < 8):
				continue
			elif(ano > -1):
				if (mes < 10):
					before = '201'+str(ano)+'-0'+str(mes)+'-01T00:00:00Z'
					if((mes+1) == 10):
						after = '201'+str(ano)+'-'+str((mes+1))+'-01T00:00:00Z'
					else:
						after = '201'+str(ano)+'-0'+str(mes+1)+'-01T00:00:00Z'
				else:
					before = '201'+str(ano)+'-'+str(mes)+'-01T00:00:00Z'
					if(mes < 12):
						after = '201'+str(ano)+'-'+str(mes+1)+'-01T00:00:00Z'
					else:
						if(ano<9):
							after = '201'+str(ano+1)+'-01-01T00:00:00Z'
						else:
							after = '20'+str(10+ano+1)+'-01-01T00:00:00Z'
		elif(ano>=10):
			#datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
			#print(datetime.today().strftime('%Y-%m-%d'))
			#print(datetime.today().strftime('%Y-%m-%d'))
			mesAtual = datetime.today().strftime('%m')
			anoAtual = datetime.today().strftime('%Y')
			
			if(int(mesAtual) < 10):
				mesAtual = mesAtual[1]

			#print(mesAtual, mes)
			year = 2000+ano+10
			#print(anoAtual,year)
						
			if (mes < 10):
				before = '20'+str(ano+10)+'-0'+str(mes)+'-01T00:00:00Z'
				if((mes+1) == 10):
					after = '20'+str(ano+10)+'-'+str((mes+1))+'-01T00:00:00Z'
				else:
					after = '20'+str(ano+10)+'-0'+str(mes+1)+'-01T00:00:00Z'
			else:
				before = '20'+str(ano+10)+'-'+str(mes)+'-01T00:00:00Z'
				if(mes < 12):
					after = '20'+str(ano+10)+'-'+str(mes+1)+'-01T00:00:00Z'
				else:
					if(ano<9):
						after = '20'+str(ano+1+10)+'-01-01T00:00:00Z'
					else:
						after = '20'+str(ano+1+10)+'-01-01T00:00:00Z'

			if(int(anoAtual)==year):
				if(int(mesAtual) < mes):
					break
		else:
			continue

		print(before)
		print(after)

		beginDate = before
		endDate = after

		#print("=================================================================================")
		print("\n ================== FROM: ",beginDate)
		print(" ================== TO: ",endDate+"\n")
		#print("=================================================================================")

		#nameCSV = "../CSV/YT_08_03_2021_v1.csv"
		#nameCSV = "../CSV/"+sys.argv[1]+".csv"


		# colocar a data e hora temporariamente e depois sleep ... e atual parametro -> pra tempo real


		#nrComentarios = 0
		#contaStatsComments = 0

		#print(search_response.get("nextPageToken"))
		nextPage_token = None
		while 1:
			try:
				#time.sleep(1)
				#trocar DEVELOPER_KEY alternadamente
				#DEVELOPER_KEY = "AIzaSyAiRA5AVSnnaCzpHsfMhUbK3Z7z5zzR3_w" #2a
				#listaKeys[0]
				random.shuffle(listaKeys)
				DEVELOPER_KEY = str(listaKeys[0])
				#print(DEVELOPER_KEY)
				#print("DEVELOPER_KEY = ", listaKeys[0])
				youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
				#print("a ir buscar...") # regionCode
				search_response = youtube.search().list(
					publishedBefore=endDate, publishedAfter=beginDate, q="Just Dance", part="id,snippet", order='relevance', type='video', relevanceLanguage='en', maxResults=100, 
					pageToken=nextPage_token).execute()
				# search () -> custo de 100 units... o resto é de 1 units

				#print(search_response.get("nextPageToken"))

				nextPage_token = search_response.get("nextPageToken")
				for search_result in search_response.get("items", []):
					#print("\n###########\n")
					#print(search_result)
					
					if search_result["id"]["kind"] == "youtube#video":
						#print(search_result["snippet"])
						titulo = search_result["snippet"]["title"]
						#titulo = unidecode.unidecode(titulo)
						#print(" >> NEW: ", titulo)

						# detect language of video title?? with preprocesing? 

						videoName = titulo.lower()
						if ( ("lady gaga" not in videoName) and ("Jerónimo de Sousa" not in videoName) and ("paul johnson" not in videoName) and ("remix" not in videoName) and ("flashmob" not in videoName) and ("ps22 chorus" not in videoName) and ("alvin" not in videoName) and ("chipettes" not in videoName) and ("chipmunk" not in videoName) and ("chipmunks" not in videoName) and ("just dance india" not in videoName) and ("official music video" not in videoName) and ("lyrics" not in videoName)
							and (("just dance" in videoName) or ("justdance" in videoName))):
							
							tituloChannel=search_result["snippet"]["channelTitle"]
							tituloChannel = unidecode.unidecode(tituloChannel)

							description = search_result["snippet"]["description"]

							idChannel=search_result["snippet"]["channelId"]
							videoPublishedAt=search_result["snippet"]["publishedAt"] #2017-02-13T02:52:38Z
							try:
								#dateComment = re.sub('T[0-9:Z]+','',dateComment)
								dateVideo = re.sub('T[0-9:Z]+','',videoPublishedAt)
							except Exception as e:
								#print(e)
								print("something wrong on convert dates...")

							#print("#############################################")
							print("Titulo: ", search_result["snippet"]["title"])
							#print("Descricao: ", search_result["snippet"]["description"])
							print("Video ID: ",search_result["id"]["videoId"])
							print("Published at: ",search_result["snippet"]["publishedAt"])

							videoID = search_result["id"]["videoId"]
							#print(">>>",checkVideoID(str(videoID)))
							if (checkVideoID(str(videoID)) is False): # videoID nao está na BD ... vai buscar todos os comentarios
								#print("a adicionar novo video...")
								if videoID not in lista_videoID: # é preciso???

									lista_videoID.append(videoID)
									# get stats of video ...
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
										#print("Total comments video = ",nrCommentsV)
										#print(">>>>>>>>>>>>>>>>>>>>>>>>>\n")

										#insert youtube video ... casos com ' dao erro ....... por causa da query .... 
										tituloChannel = tituloChannel.replace("'","")
										description = description.replace("'","")
										query = "insert into video values('"+str(idChannel)+"', '"+str(tituloChannel)+"', '"+str(videoID)+"','"+titulo+"','"+str(dateVideo)+"', '"+str(views)+"', '"+str(likesV)+"', '"+str(dislikesV)+"', '"+str(nrCommentsV)+"', '"+str(description)+"')"
										insertToTable(query)

										#insert edition and plataform of game ...
										game_id = getEditionAndPlataform(game_id, titulo, description)
										#print(".... id game --> ",game_id) # nao aumentam depois.... colocar aqui toda a anotacao do execute? ou return ID's ... em tuplo..? 


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

														#comentario = unidecode.unidecode(comentario)
														#nrComentarios+=1

														nr_likes = comment_result['snippet']['topLevelComment']['snippet']['likeCount']
														commentID = comment_result['snippet']['topLevelComment']['id']
														#print(comment_result['snippet']['topLevelComment']['snippet']['updatedAt'])
														publishTime = comment_result['snippet']['topLevelComment']['snippet']['updatedAt']
														# updatedAt pq pode incluir possiveis correcoes, ao inves do comment original com "publishedAt"
														try:
															dateComment = re.sub('T[0-9:Z]+','',publishTime)
														except Exception as e:
															#print(e)
															print("something wrong on convert dates...", e)
														
														isMain = "Main"
														try:
															comment = runPreprocessing(comentario)
															if (comment != "None"):
																#game_id, dimension_id, opinion_id, title, videoID, comment, commentID, likes, dateComment, isMain, dateVideo, views, likesVideo, dislikesVideo,totalCommentsVideo, descript, channel, channelID
																#def executeAnnotation(game_id, dimension_id, opinion_id, videoID, comment, commentID, likes, dateComment, isMain):
																ids = executeAnnotation(game_id, dimension_id, opinion_id, videoID, comment, commentID, nr_likes, dateComment, isMain)
																opinion_id = ids[0]
																dimension_id = ids[1]
																#print(".... id's --> ",opinion_id, dimension_id) # nao aumentam depois.... colocar aqui toda a anotacao do execute? ou return ID's ... em tuplo..? 

																nr_replies = comment_result['snippet']['totalReplyCount']
																#print(" . . . replies stats = ", nr_replies)
																countReplies = 0

																nextPTreply = None #page token
																if (nr_replies > 0):
																	try:
																		#time.sleep(0.2)
																		#DEVELOPER_KEY = "AIzaSyAP6m_Icjnn2npBnwM4sSVK4VT5kKoOe7o" renato 1a
																		#DEVELOPER_KEY = "AIzaSyBiRFpFQdLOgPWfMFTaklcq2twvQESDQZ0" #coimvivio
																		random.shuffle(listaKeys)
																		DEVELOPER_KEY = str(listaKeys[0])

																		#DEVELOPER_KEY ="AIzaSyDXIzN7IV034Isli8V6Od-c7IyxUahQ4tc" #manel nos comments
																		#DEVELOPER_KEY = "AIzaSyBptCUsM32WTIHs8TfLg7I8EFELkUCXcic" #new 2
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
																					print("something wrong on convert dates...")
																				#print(r['snippet']['textDisplay'])
																				#nrComentarios+=1
																				countReplies+=1
																				isMain = "Reply"
																				try:
																					commentReply = runPreprocessing(textReply)
																					if (commentReply != "None"):
																						#game_id, dimension_id, opinion_id, title, videoID, comment, commentID, likes, dateComment, isMain, dateVideo, views, likesVideo, dislikesVideo,totalCommentsVideo, descript, channel, channelID
																						ids = executeAnnotation(game_id, dimension_id, opinion_id, videoID, commentReply, replyID, likesReply, dateReply, isMain)
																						opinion_id = ids[0]
																						dimension_id = ids[1]
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
												except:
													print("commentThreads() - something wrong ...")
										else:
											#print("NO COMMENTS!")
											#break
											continue        
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
									# é preciso???
									print(" X REJECT! Video repetido\n")
									break
							else:
								print("		>>> video já inserido na BD...")
								# VAI BUSCAR OS COMENTÁRIOS SÓ A PARTIR DA DATA XXX
								#....
						else:
							#print(" X REJECT! lady gaga or something else\n")
							continue
				#time.sleep(0.25)
				if nextPage_token is None:
					#print("\n~~~~ nr de videos atual: ", conta)
					break #sem break, começa tudo de novo
			except HttpError as e:
				print("search() — An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
				if("quotaExceeded" in str(e.content)):
					time.sleep(0.1) #72 minutos
			#except (ConnectionError, ReadTimeout):
				#print("ERROR! Connection or TIME OUT!")
			except Exception as e:
				print("search () -", e)
				#print("search () - something wrong ...")
				#DEVELOPER_KEY = "AIzaSyAL0ChC4DB6Su9C6X3YVDJMMzly0o_Mq_4" #backup
				#DEVELOPER_KEY = "AIzaSyAilu0HwaDQlvkDZEsKxQ6POFMdyvKiU4E" #3a
				#youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

		#print("Videos:\n", "\n".join(videos), "\n")
		#lista_videoID
		print("--- fim ---\n ")
		#print("nr comentarios: ",nrComentarios)

