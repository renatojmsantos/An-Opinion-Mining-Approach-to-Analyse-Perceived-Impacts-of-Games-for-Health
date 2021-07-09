import pandas as pd
import time
import csv
import unidecode


from connectDB import *



def getFeatures():
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "SELECT * FROM comment left join annotation on annotation.comment_commentid = comment.commentid left join game on game.game_id = annotation.game_game_id left join video on video.videoid = annotation.video_videoid order by annotationid"

		#print(query)
		cur.execute(query)
		idBack = cur.fetchall() # TUPLO
		
		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack


def export():
	try:
		#f = open('../justDance','w')
		#write = csv.writer(f)

		header = ['annotationID','dimension','concept','commentID', 'originalText','expandedText','sentiment','likes','dateComment','mainComment',
				'gameID','edition','platform','channelID','channelTitle','videoID','videoTitle','dateVideo','viewsVideo','likesVideo','dislikesVideo','totalCommentsVideo','descriptionVideo']

		
		with open('../justDance.csv', 'w', encoding='UTF8', newline='') as f:
			writer = csv.writer(f)
			writer.writerow(header)

			cols = getFeatures()
			for col in cols:
				data = []
				commentID = col[0]
				originalText = col[1]
				expandedText = col[2]
				sentiment = col[3]
				likes = col[4]
				dateComment = col[5]
				mainComment = col[6]
				annotationID = col[7]
				dimension = col[8]
				concept = col[9]
				gameID = col[13]
				edition = col[14]
				platform = col[15]
				channelID = col[16]
				channelTitle = col[17]
				videoID = col[18]
				videoTitle = col[19]
				dateVideo = col[20]
				viewsVideo = col[21]
				likesVideo = col[22]
				dislikesVideo = col[23]
				totalCommentsVideo = col[24]
				descriptionVideo = col[25]

				#print(commentID,originalText)
				data.extend([annotationID,dimension,concept,commentID,originalText,expandedText,sentiment,likes,dateComment,mainComment,gameID,edition,platform,channelID,channelTitle,videoID,videoTitle,dateVideo,viewsVideo, likesVideo,dislikesVideo,totalCommentsVideo,descriptionVideo])
				#print(data)
				writer.writerow(data)
			
	except Exception as e:
		print(e)

export()

