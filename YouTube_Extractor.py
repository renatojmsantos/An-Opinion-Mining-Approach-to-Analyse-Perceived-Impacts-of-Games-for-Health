#import os
#from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
#from langdetect import detect
import time
import csv
import unidecode

#CLIENT_SECRETS_FILE = "client_secret.json"

#DEVELOPER_KEY = "AIzaSyAP6m_Icjnn2npBnwM4sSVK4VT5kKoOe7o" #original 1a

DEVELOPER_KEY = "AIzaSyAiRA5AVSnnaCzpHsfMhUbK3Z7z5zzR3_w" #2a

#DEVELOPER_KEY = "AIzaSyAilu0HwaDQlvkDZEsKxQ6POFMdyvKiU4E" #3a

#DEVELOPER_KEY = "AIzaSyAL0ChC4DB6Su9C6X3YVDJMMzly0o_Mq_4"

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# 4/1AY0e-g6HsBRDn9XtgpQsehXcHdI3JU-F3uOkTkI1otQJGU0oyDj4euolBg8
# 4/1AY0e-g6Ekmgnu-HotcSKXh8ESlFsQLMT-ML8TGO7jVjN1cLKsJR4EAk-Jc0

# publishedAfter and before... para ir buscar antes e depois da data X
before = '2010-01-01T00:00:00Z'
after = "2021-01-01T00:00:00Z"

nameCSV = "../CSV/YT_09_03_2021_v5.csv"

# colocar a data e hora temporariamente e depois sleep ... e atual parametro -> pra tempo real

lista_videoID=[]

comments=[]
likes=[]
commentsID = []
data = []
conta = 0
nrComentarios = 0

#print(search_response.get("nextPageToken"))
nextPage_token = None
while 1:
    try:
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
        print("a ir buscar...")
        search_response = youtube.search().list(
            publishedBefore=before, q="Just Dance", part="id,snippet", order='relevance', type='video', relevanceLanguage='en', maxResults=100, 
            pageToken=nextPage_token).execute()

        print(search_response.get("nextPageToken"))

        nextPage_token = search_response.get("nextPageToken")
        for search_result in search_response.get("items", []):
            #print("\n###########\n")
            #print(search_result)
            conta += 1
            if search_result["id"]["kind"] == "youtube#video":
                #print(search_result["snippet"])
                titulo = search_result["snippet"]["title"]
                #titulo = unidecode.unidecode(titulo)
                print(" >> NEW: ", titulo)
                videoName = titulo.lower()
                if (("lady gaga" not in videoName) and ("just dance" in videoName)):
                    tituloChannel=search_result["snippet"]["channelTitle"]
                    tituloChannel = unidecode.unidecode(tituloChannel)

                    idChannel=search_result["snippet"]["channelId"]
                    videoPublishedAt=search_result["snippet"]["publishedAt"] #2017-02-13T02:52:38Z
                    
                    print("##########################################################################################")
                    #print("#############################################")
                    print("Titulo: ", search_result["snippet"]["title"])
                    print("Video ID: ",search_result["id"]["videoId"])
                    print("Published at: ",search_result["snippet"]["publishedAt"])

                    videoID = search_result["id"]["videoId"]

                    # get stats of video ...
                    DEVELOPER_KEY = "AIzaSyAL0ChC4DB6Su9C6X3YVDJMMzly0o_Mq_4"
                    yt = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
                    requestStats = yt.videos().list(
                            part='id,statistics', id=videoID, maxResults=100
                    ).execute()
                    #if search_result["items"]["kind"] == "youtube#video":
                    #print(requestStats)
                    print(">>>>>>>>>>> stats video >>>>>>>>>>>>>>")
                    #print(requestStats["items"])
                    print("VIEWS = "+requestStats["items"][0]["statistics"]["viewCount"])
                    views = requestStats["items"][0]["statistics"]["viewCount"]

                    if( (('commentCount' in requestStats["items"][0]["statistics"]) == True) and
                        (('likeCount' in requestStats["items"][0]["statistics"]) == True) and
                        (('dislikeCount' in requestStats["items"][0]["statistics"]) == True)
                        ):
                        print("Total comments video = "+requestStats["items"][0]["statistics"]["commentCount"])
                        likesV = requestStats["items"][0]["statistics"]["likeCount"]
                        dislikesV = requestStats["items"][0]["statistics"]["dislikeCount"]
                        nrCommentsV = requestStats["items"][0]["statistics"]["commentCount"]
                    else:
                        nrCommentsV=0
                        likesV=0
                        dislikesV=0
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

                    # get comments of video ...
                    nextPT = None
                    while 1: #comentarios do videoID
                        DEVELOPER_KEY = "AIzaSyAilu0HwaDQlvkDZEsKxQ6POFMdyvKiU4E"
                        yt_c = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

                        comment_response = yt_c.commentThreads().list(
                            part='snippet,replies', videoId=videoID, maxResults=100,
                            order='relevance', textFormat='plainText',pageToken=nextPT).execute()
                        nextPT = comment_response.get('nextPageToken')
                        for comment_result in comment_response.get("items",[]):
                            #print(comment_result)
                            #print(comment_result['snippet']['topLevelComment']['snippet']['textDisplay'])
                            comentario = comment_result['snippet']['topLevelComment']['snippet']['textDisplay']
                            #comentario = unidecode.unidecode(comentario)
                            nrComentarios+=1

                            nr_likes = comment_result['snippet']['topLevelComment']['snippet']['likeCount']
                            commentID = comment_result['snippet']['topLevelComment']['id']
                            #print(comment_result['snippet']['topLevelComment']['snippet']['updatedAt'])
                            publishTime = comment_result['snippet']['topLevelComment']['snippet']['updatedAt']
                            # updatedAt pq pode incluir possiveis correcoes, ao inves do comment original com "publishedAt"
                            data.append(publishTime)
                            commentsID.append(commentID)
                            comments.append(comentario)
                            likes.append(nr_likes)

                            nr_replies = comment_result['snippet']['totalReplyCount']
                            #print("replies = ", nr_replies)
                            countReplies = 0

                            nextPTreply = None #page token
                            if (nr_replies > 0):
                                DEVELOPER_KEY = "AIzaSyAP6m_Icjnn2npBnwM4sSVK4VT5kKoOe7o"
                                yt_r = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

                                while (countReplies <= nr_replies):
                                    commentsReplies = yt_r.comments().list(
                                        parentId = commentID, part='id,snippet', maxResults=100).execute()
                                    nextPTreply = commentsReplies.get('nextPageToken')
                                    for r in commentsReplies.get("items",[]):
                                        #print(r)
                                        replyID = r['id']
                                        textReply = r['snippet']['textDisplay']
                                        likesReply = r['snippet']['likeCount']
                                        publishedAtReply = r['snippet']['updatedAt']

                                        #print(r['snippet']['textDisplay'])
                                        nrComentarios+=1
                                        #countReplies+=1

                                        data.append(publishedAtReply)
                                        commentsID.append(replyID)
                                        comments.append(textReply)
                                        likes.append(likesReply)
                                        #print(" ...... replies lidos = # ",countReplies)

                                    if ((nextPTreply is None)):
                                        #print("$$ fim replies")
                                        #print("replies lidos = ",countReplies)
                                        break

                            #print("replies lidos = ",countReplies)
                        
                        if nextPT is None:
                            #time.sleep(5)
                            print(". . . nr comentarios total = ",nrComentarios)
                            break

                    # export do csv
                    dict = {'Video Title': [titulo] * len(comments),'videoID': [videoID] * len(comments),
                            'Comment': comments, 'CommentID': commentsID,
                            'Likes': likes, 'TimeStampComment': data,
                            'Channel': [tituloChannel] * len(comments), 'ChannelID': [idChannel] * len(comments),
                            'VideoPublishedAt': [videoPublishedAt] * len(comments),
                            'ViewsVideo': [views] * len(comments), 'likesVideo':[likesV] * len(comments),
                            'dislikesVideo': [dislikesV] * len(comments), 'totalCommentsVideo': [nrCommentsV] * len(comments)
                            }
                    out_df = pd.DataFrame(dict)

                    if(conta==1):
                        out_df.to_csv(nameCSV, mode='a', header=True,index=False)
                    else: #sem header
                        out_df.to_csv(nameCSV, mode='a', header=False,index=False)
                    #out_df.to_csv(nameCSV, mode='a', header=False,index=False)    
                else:
                    print("REJECT! lady gaga")

            print("Video # ", conta)
            if nextPage_token is None:
                print("\n~~~~ nr de videos atual: ", conta)
                #time.sleep(20)
                break #sem break, começa tudo de novo

    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
        DEVELOPER_KEY = "AIzaSyAL0ChC4DB6Su9C6X3YVDJMMzly0o_Mq_4" #backup
        #DEVELOPER_KEY = "AIzaSyAilu0HwaDQlvkDZEsKxQ6POFMdyvKiU4E" #3a
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

#print("Videos:\n", "\n".join(videos), "\n")
#lista_videoID
print("--- fim ---\n nr de videos: ",conta)
print("nr comentarios: ",nrComentarios)

