import pandas as pd
import time
import csv
import unidecode
import json
import configparser
import random
import sys

from preprocessing import *
from annotation import * 
from selectGame import *
from datetime import datetime, date, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langdetect import detect
from connectDB import *

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

listaKeys = []


def insertToTable(query):
	idBack = None
	conn = None
	
	try:
		params = config()
		conn = psycopg2.connect(**params)
		conn.autocommit = True
		cur = conn.cursor()

		query = query + " returning 1;" 
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


def readKeys(filename='dev_keys.txt'):
	with open(filename) as file:
		for line in file:
			listaKeys.append(line.strip())
	
readKeys()


def checkVideoID(videoid): 
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()

		query = "SELECT videoid FROM video WHERE videoid = '"+ videoid +"' "
		cur.execute(query)

		idBack = cur.fetchone()		
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			conn.close()
	return idBack is not None 

def checkCommentID(commentid):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()

		query = "SELECT commentid FROM comment WHERE commentid = '"+ commentid +"' "
		cur.execute(query)

		idBack = cur.fetchone()		
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			conn.close()
	return idBack is not None 

def checkAnnotatedComment(commentid):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()

		query = "SELECT comment_commentid FROM annotation WHERE comment_commentid = '"+ commentid +"' "
		cur.execute(query)

		idBack = cur.fetchone()		
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			conn.close()
	return idBack is not None 

def countRowsTable(tableName):
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()

		query = "SELECT count(*) FROM "+tableName+""

		cur.execute(query)
		idBack = cur.fetchone() 
		
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			conn.close()
	return idBack

def getLastAnnotationID():
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()

		query = "select annotationid from annotation order by annotationid desc;"

		cur.execute(query)
		idBack = cur.fetchone() 
		
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			conn.close()
	return idBack

def getLastGameID():
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()

		query = "select game_id from game order by game_id desc;"

		cur.execute(query)
		idBack = cur.fetchone()
		
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			conn.close()
	return idBack

def getGameID(videoid):
	
	try:
		idBack = None
		conn = None
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()

		query = "SELECT game_game_id  FROM annotation where video_videoid='"+videoid+"'"
		cur.execute(query)

		idBack = cur.fetchone()
		
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO! get comments", error)
	finally:
		if conn is not None:
			conn.close()
	return idBack

gameid = getLastGameID()
annotationid = getLastAnnotationID()

game_id = int(gameid[0])
annotation_id = int(annotationid[0])

giveDate = sys.argv[1]
interval = sys.argv[2]
sleepTime = sys.argv[3]
checkNewComments = sys.argv[4]

searchGame = sys.argv[5]

beginHour = int(sys.argv[6])
endHour = int(sys.argv[7])

print(beginHour, endHour)


games = ['Just Dance 2', 'Just Dance 3', 'Just Dance 4', 'Just Dance 2014', 'Just Dance 2015', 'Just Dance 2016', 'Just Dance 2017', 'Just Dance 2018', 'Just Dance 2019', 'Just Dance 2020', 'Just Dance 2021', 'Just Dance 2022',
				'Just Dance Wii', 'Just Dance Wii 2', 'Just Dance Wii U', 'Yo-kai Watch Dance: Just Dance Special Version',
				'Just Dance Kids', 'Just Dance Kids 2', 'Just Dance Kids 2014',
				'Just Dance: Disney Party', 'Just Dance: Disney Party 2',
				'Just Dance: Greatest Hits',
				'Just Dance: Summer Party', 'Just Dance Now', 'Just Dance Unlimited']

giveDate = giveDate.split("-")

startDate = date(int(giveDate[0]),int(giveDate[1]),int(giveDate[2]))

endYear = datetime.today().strftime('%Y')
endMonth = datetime.today().strftime('%m')
endDay = datetime.today().strftime('%d')
endDate = date(int(endYear),int(endMonth),int(endDay))

delta = endDate - startDate

before = ''
after = ''


nrTotal = 0
nrValidos = 0
c=0

while 1: 
	if (int(datetime.now().hour) > int(beginHour) and int(datetime.now().hour) < int(endHour)):
		print("\n getting data ... ")
		for d in range(delta.days + 2):
			day = startDate + timedelta(days = d)
			if(d>(1-int(interval))):
				dayBefore = startDate + timedelta(days = d-int(interval))
			c+=1
			if (c<int(interval)):
				continue
			elif (c==int(interval)):
				day = str(day) 
				newdate = day.split("-")
				newdate = str(newdate[0])+'-'+str(newdate[1])+'-'+str(newdate[2])+'T00:00:00Z'

				if(d>0 and int(datetime.now().hour) > int(beginHour) and int(datetime.now().hour) < int(endHour)):
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
						try:
							random.shuffle(listaKeys)
							DEVELOPER_KEY = str(listaKeys[0])
							youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

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
								
								if search_result["id"]["kind"] == "youtube#video":
									titulo = search_result["snippet"]["title"]
									description = search_result["snippet"]["description"]
									
									videoName = titulo.lower()
									if ( ("lady gaga" not in videoName) and ("ladygaga" not in videoName) and ("lyric" not in videoName) and ("school" not in videoName) and ("dialysis" not in videoName) and ("fuck it" not in videoName) and ("maristela" not in videoName) and ("killebom" not in videoName) and ("ladies free" not in videoName) and ("brand new band" not in videoName) and ("ivi adamou" not in videoName) and ("talent show" not in videoName) and ("effy" not in videoName) and ("music video" not in videoName) and ("the nanny" not in videoName) and ("josh turner" not in videoName) and ("karaoke" not in videoName) and ("quadriphonix" not in videoName) and ("acoustic" not in videoName) and ("cover" not in videoName) and ("Jerónimo de Sousa" not in videoName) and ("paul johnson" not in videoName) and ("remix" not in videoName) and ("flashmob" not in videoName) and ("ps22 chorus" not in videoName) and ("alvin" not in videoName) and ("chipettes" not in videoName) and ("chipmunk" not in videoName) and ("chipmunks" not in videoName) and ("just dance india" not in videoName) and ("official music video" not in videoName) and ("lyrics" not in videoName)
										and ("covers" not in description) and ("maristela" not in description) and ("killebom" not in description)
										and ("ivi adamou" not in description) and ("talent show" not in description) and ("music video" not in description) 
										and ("the nanny" not in description) and ("josh turner" not in description) and ("karaoke" not in description) and ("quadriphonix" not in description) and ("acoustic" not in description)
										and ("Jerónimo de Sousa" not in description) and ("paul johnson" not in description) and ("remix" not in description) and ("flashmob" not in description) and ("ps22 chorus" not in description)
										and ("chipettes" not in description) and ("chipmunk" not in description) and ("chipmunks" not in description) and ("just dance india" not in description) and ("official music video" not in description)
										and (("just dance" in videoName) or ("justdance" in videoName))):
										
										tituloChannel=search_result["snippet"]["channelTitle"]
										tituloChannel = unidecode.unidecode(tituloChannel) 
										
										tituloChannel = tituloChannel.replace("'"," ")
										description = description.replace("'"," ")

										idChannel=search_result["snippet"]["channelId"]
										videoPublishedAt=search_result["snippet"]["publishedAt"] 

										# it was on this format: 2017-02-13T02:52:38Z
										try:
											dateVideo = re.sub('T[0-9:Z]+','',videoPublishedAt)
										except Exception as e:
											print("something wrong on convert dates...", e)
										
										videoID = search_result["id"]["videoId"]

										print("\nTitulo: ", search_result["snippet"]["title"])
										print("Video ID: ",search_result["id"]["videoId"])
										print("Published at: ",search_result["snippet"]["publishedAt"])

										if (checkVideoID(str(videoID)) is False and int(datetime.now().hour) > int(beginHour) and int(datetime.now().hour) < int(endHour)): 

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
													likesV = requestStats["items"][0]["statistics"]["likeCount"]
													dislikesV = requestStats["items"][0]["statistics"]["dislikeCount"]
													nrCommentsV = requestStats["items"][0]["statistics"]["commentCount"]
												else:
													nrCommentsV=0
													likesV=0
													dislikesV=0
											
												query = "insert into video values('"+str(idChannel)+"', '"+str(tituloChannel)+"', '"+str(videoID)+"','"+titulo+"','"+str(dateVideo)+"', '"+str(views)+"', '"+str(likesV)+"', '"+str(dislikesV)+"', '"+str(nrCommentsV)+"', '"+str(description)+"')"
												insertToTable(query)
												print(game_id)
												game_id = getEditionAndPlataform(game_id, titulo, description)
												
												if(int(nrCommentsV) > 0 and int(datetime.now().hour) > int(beginHour) and int(datetime.now().hour) < int(endHour)):
													nextPT = None
													while 1: 
														try:
															if (int(datetime.now().hour) > int(beginHour) and int(datetime.now().hour) < int(endHour)):
																random.shuffle(listaKeys)
																DEVELOPER_KEY = str(listaKeys[0])
																yt_c = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

																comment_response = yt_c.commentThreads().list(
																	part='snippet,replies', videoId=videoID, maxResults=100,
																	order='relevance', textFormat='plainText',pageToken=nextPT).execute()
																nextPT = comment_response.get('nextPageToken')
																for comment_result in comment_response.get("items",[]):

																	comentario = comment_result['snippet']['topLevelComment']['snippet']['textDisplay']

																	nr_likes = comment_result['snippet']['topLevelComment']['snippet']['likeCount']
																	commentID = comment_result['snippet']['topLevelComment']['id']
																	publishTime = comment_result['snippet']['topLevelComment']['snippet']['updatedAt']

																	try:
																		dateComment = re.sub('T[0-9:Z]+','',publishTime)
																	except Exception as e:
																		print("something wrong on convert dates...", e)
																	
																	try:
																		comment = runPreprocessing(comentario)
																		if (comment != "None" and comment != "none" and comment is not None):
																			isMain = "Main"
																			if(checkAnnotatedComment(str(commentID)) is False):
																				annotation_id = executeAnnotation(game_id, annotation_id, videoID, comment, comentario, commentID, nr_likes, dateComment, isMain)
																			
																			nr_replies = comment_result['snippet']['totalReplyCount']
																			countReplies = 0

																			nextPTreply = None 
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
																							replyID = r['id']
																							textReply = r['snippet']['textDisplay']
																							likesReply = r['snippet']['likeCount']
																							publishedAtReply = r['snippet']['updatedAt']

																							try:
																								dateReply = re.sub('T[0-9:Z]+','',publishedAtReply)
																							except Exception as e:
																								print("something wrong on convert dates...", e)
																						
																							countReplies+=1
																							
																							try:
																								commentReply = runPreprocessing(textReply)
																								if (commentReply != "None" and commentReply != "none" and commentReply is not None):
																									
																									isMain = "Reply"
																									if(checkAnnotatedComment(str(replyID)) is False):
																										annotation_id = executeAnnotation(game_id, annotation_id, videoID, commentReply, textReply, replyID, likesReply, dateReply, isMain)
																									
																							except Exception as e:
																								print("replys -", e)	
																				except HttpError as e:
																					print("comments() - replies — An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
																					if("quotaExceeded" in str(e.content)):
																						time.sleep(0.1)
																				
																				except Exception as e:
																					print("get replys - ", e)
																			else:
																				continue
																		
																		else:
																			continue
																	except Exception as e:
																		print("comments -", e)
															else:
																break

															if nextPT is None:
																
																break

														except HttpError as e:
															print("commentThreads() — An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
															if("quotaExceeded" in str(e.content)):
																print("SEM QUOTA")
																time.sleep(0.1)
															if("commentsDisabled" in str(e.content)):
																print("COMENTARIOS DESATIVADOS...")
																break
														
														except Exception as ex:
															print("commentThreads() - ", ex)
												else:
													continue
											except HttpError as e:
												print("videos (stats) — An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
												if("quotaExceeded" in str(e.content)):
													time.sleep(0.1) 
											except Exception as e:
												print("videos (stats) ", e)
										else:
											print("	 >>> video já inserido na BD...")
											
											if (checkNewComments == "True" and int(datetime.now().hour) > int(beginHour) and int(datetime.now().hour) < int(endHour)):
												
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
													else:
														nrCommentsV=0
													
													if(int(nrCommentsV) > 0):
														g = selectIdGame(titulo, description)
														print(g)
														game_id = g[0]

														nextPT = None
														while 1: 
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
																	
																	if (checkCommentID(str(commentID)) is False):
																		comentario = comment_result['snippet']['topLevelComment']['snippet']['textDisplay']
																		nr_likes = comment_result['snippet']['topLevelComment']['snippet']['likeCount']
																		publishTime = comment_result['snippet']['topLevelComment']['snippet']['updatedAt']
																		
																		try:
																			dateComment = re.sub('T[0-9:Z]+','',publishTime)
																		except Exception as e:
																			print("something wrong on convert dates...", e)

																		try:
																			comment = runPreprocessing(comentario)

																			if (comment != "None" and comment != "none" and comment is not None):
																				print("new comment ! ")

																				isMain = "Main"
																				if(checkAnnotatedComment(str(commentID)) is False):
																					annotation_id = executeAnnotation(game_id, annotation_id, videoID, comment, comentario, commentID, nr_likes, dateComment, isMain)
																				
																				nr_replies = comment_result['snippet']['totalReplyCount']
																				countReplies = 0

																				nextPTreply = None 
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
																								replyID = r['id']
																								textReply = r['snippet']['textDisplay']
																								likesReply = r['snippet']['likeCount']
																								publishedAtReply = r['snippet']['updatedAt']

																								try:
																									dateReply = re.sub('T[0-9:Z]+','',publishedAtReply)
																								except Exception as e:
																									print("something wrong on convert dates...", e)
																							
																								countReplies+=1
																								
																								try:
																									commentReply = runPreprocessing(textReply)

																									if (commentReply != "None" and commentReply != "none" and commentReply is not None):
																										isMain = "Reply"
																										if(checkAnnotatedComment(str(replyID)) is False):
																											annotation_id = executeAnnotation(game_id, annotation_id, videoID, commentReply, textReply, replyID, likesReply, dateReply, isMain)
																										
																								except Exception as e:
																									print("replys -", e)	
																					except HttpError as e:
																						print("comments() - replies — An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
																						if("quotaExceeded" in str(e.content)):
																							time.sleep(0.1)
																					
																					except Exception as e:
																						print("get replys - ", e)
																						
																				else:
																					continue
																			
																			else:
																				
																				continue
																		except Exception as e:
																			print("comments -", e)
																	else:
																		
																		continue

																if nextPT is None:
																	
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
															except Exception as ex:
																print("commentThreads() - ", ex)
													else:
														#no comments
														continue

												except Exception as e:
													print("new comments total - ", e)
											else:
												#print("dont check new comments")
												continue

									else:
										#print(" X REJECT! not just dance\n")
										continue
							if nextPage_token is None:
								break 
						except HttpError as e:
							print("search() — An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
							if("quotaExceeded" in str(e.content)):
								time.sleep(0.1) 
						except Exception as e:
							print("search () -", e)
							
					print("--- fim ---\n ")
				c = 0

		print("end...")
		print(datetime.now())
		time.sleep(int(sleepTime))
		print("again...")
	else:
		#print("Not this time")
		time.sleep(int(sleepTime))



