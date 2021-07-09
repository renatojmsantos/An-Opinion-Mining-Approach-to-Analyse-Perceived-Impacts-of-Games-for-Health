import pandas as pd
import time
import csv


from connectDB import *



def getFeatures():
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		#query = "SELECT * FROM annotation join comment on comment.commentid = annotation.comment_commentid join game on game.game_id = annotation.game_game_id join video on video.videoid = annotation.video_videoid"

		query = "SELECT annotationid,field,concept,comment_commentid,originaltext, processedtext,polarity,likes, dateComment, mainComment, game_game_id, edition, platform, channelID, channelTitle, video_videoid, videoTitle, dateVideo, viewsVideo, likesVideo,dislikesvideo, totalcommentsvideo,description FROM annotation join comment on comment.commentid = annotation.comment_commentid join game on game.game_id = annotation.game_game_id join video on video.videoid = annotation.video_videoid"

		cur.itersize = 10000
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
	
		#f = open('../justDance','w')
		#write = csv.writer(f)

	print("yes0")
	with open('../justDance.csv', 'w', encoding='utf-8', newline='') as f:

		header = ['annotationID','dimension','concept','commentID', 'originalText','expandedText','sentiment','likes','dateComment','mainComment',
			'gameID','edition','platform','channelID','channelTitle','videoID','videoTitle','dateVideo','viewsVideo','likesVideo','dislikesVideo','totalCommentsVideo','descriptionVideo']

		print("yes1")
		writer = csv.writer(f)
		print("yes2")
		writer.writerow(header)
		print("yes3")
		cols = getFeatures()
		print("yes")
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
			gameID = col[10]
			edition = col[11]
			platform = col[12]
			channelID = col[13]
			channelTitle = col[14]
			videoID = col[15]
			videoTitle = col[16]
			dateVideo = col[17]
			viewsVideo = col[18]
			likesVideo = col[19]
			dislikesVideo = col[20]
			totalCommentsVideo = col[21]
			descriptionVideo = col[22]

			#print(commentID,originalText)
			data.extend([annotationID,dimension,concept,commentID,originalText,expandedText,sentiment,likes,dateComment,mainComment,gameID,edition,platform,channelID,channelTitle,videoID,videoTitle,dateVideo,viewsVideo, likesVideo,dislikesVideo,totalCommentsVideo,descriptionVideo])
			#print(data)
			writer.writerow(data)
			#time.sleep(0.5)
			


export()

