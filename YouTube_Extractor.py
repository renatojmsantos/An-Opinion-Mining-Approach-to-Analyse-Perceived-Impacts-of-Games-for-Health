#import os
#from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

from langdetect import detect

import time
import csv
import unidecode
import requests

import httplib2
import json

#e.reason
from urllib.request import urlopen, build_opener, install_opener, ProxyHandler # Python 3
import signal

import sys

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


# opcao de run raiz ou run de atualizacao constemente ... fazer .. vindo do input terminal
# run raiz -> atual
# run atualizacao -> checka novos comentarios a partir da data X... 
#                 guardar uma data temporaria, fazer sleep X e depois verificar de novo com uma data + recente
#                 ... assim monitoriza todos os videos, e caso hajam novos comentarios adiciona


# for para incrementar isto e fazer tudo automatico
writedComments = 0
conta = 0
lista_videoID=[]
newyear20=0

for i in range (-1,12): #(-1,12)
    change = 0 
    #text = '201'+str(i)+'ss'
    #before = '2010-01-01T00:00:00Z'
    #after = '2011-01-01T00:00:00Z'
    #print(j)
    if(i==-1): #jd lancado em nov de 2009
        #before = '2009-06-01T00:00:00Z'
        #after = '2010-01-01T00:00:00Z'
        before = '2014-06-01T00:00:00Z'
        after = '2015-01-01T00:00:00Z'

    for j in range(2):
        #time.sleep(60*4) #86400 = 1 dia sleep, 3600s = 1h
        print(" .... NOVO INTERVALO DE TEMPO")
        if(j%2==0):
            #mes 1
            j=1
        else: 
            #mes 6
            j=6
        if(i<10 and i>=5 or i<=-1): #i<10 and i>=4 or i<=-1 ... 4 a partir de 06/2013
            if (i == -1):
                if (j%2==0): # ir buscar os ultimos 6 meses de 2009
                    pass
                else:
                    continue
            else:
                time.sleep(60) #86400 = 1 dia sleep, 3600s = 1h
                if(j==1):
                    a = 6
                else:
                    a = 1
                #print("$ ",change)
                before = '201'+str(i)+'-0'+str(j)+'-01T00:00:00Z'
                if((i+1) == 10): #2020
                    if(change==1):
                        #after = '2020-0'+str(a)+'-01T00:00:00Z'
                        after = '2020-0'+str(a)+'-01T00:00:00Z'
                    else:
                        after = '2019-0'+str(a)+'-01T00:00:00Z'
                else: #2010 - 2019
                    print(change)
                    if(change==1):
                        after = '201'+str(i+1)+'-0'+str(a)+'-01T00:00:00Z'
                    else:
                        after = '201'+str(i)+'-0'+str(a)+'-01T00:00:00Z' 
        elif(i>=10): #2021
            time.sleep(60) #86400 = 1 dia sleep, 3600s = 1h
            i=20
            #ano=[20,20,21,21]
            if(j==1):
                a = 6
            else:
                a = 1
            #print("#",change)
            #print(i)
            #print(ano[change])

            newyear20+=1
            if(newyear20 <= 2):
                print("False")
                before = '20'+str(i)+'-0'+str(j)+'-01T00:00:00Z'
                #before = '20'+str(ano[change])+'-0'+str(j)+'-01T00:00:00Z'
                if(change==1):
                    after = '20'+str(i+1)+'-0'+str(a)+'-01T00:00:00Z'
                    
                else:
                    after = '20'+str(i)+'-0'+str(a)+'-01T00:00:00Z'

            if(newyear20 > 2):
                print("True")
                y=21
                before = '20'+str(y)+'-0'+str(j)+'-01T00:00:00Z'
                #before = '20'+str(ano[change])+'-0'+str(j)+'-01T00:00:00Z'
                if(change==1):
                    newyear20+=1
                    after = '20'+str(y+1)+'-0'+str(a)+'-01T00:00:00Z'
                else:
                    after = '20'+str(y)+'-0'+str(a)+'-01T00:00:00Z'
        else:
            continue
            
        change+=1

        print(before)
        print(after)

        beginDate = before
        endDate = after

        print("=================================================================================")
        print("\n ================== FROM: ",beginDate)
        print(" ================== TO: ",endDate+"\n")
        print("=================================================================================")

        #nameCSV = "../CSV/YT_08_03_2021_v1.csv"
        nameCSV = "../CSV/"+sys.argv[1]+".csv"

        # colocar a data e hora temporariamente e depois sleep ... e atual parametro -> pra tempo real


        #nrComentarios = 0
        #contaStatsComments = 0

        #print(search_response.get("nextPageToken"))
        nextPage_token = None
        while 1:
            try:
                time.sleep(2)
                youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
                print("a ir buscar...")
                search_response = youtube.search().list(
                    publishedBefore=endDate, publishedAfter=beginDate, q="Just Dance", part="id,snippet", order='relevance', type='video', relevanceLanguage='en', maxResults=100, 
                    pageToken=nextPage_token).execute()

                print(search_response.get("nextPageToken"))

                nextPage_token = search_response.get("nextPageToken")
                for search_result in search_response.get("items", []):
                    #print("\n###########\n")
                    #print(search_result)
                    
                    if search_result["id"]["kind"] == "youtube#video":
                        #print(search_result["snippet"])
                        titulo = search_result["snippet"]["title"]
                        #titulo = unidecode.unidecode(titulo)
                        print(" >> NEW: ", titulo)
                        videoName = titulo.lower()
                        if ( ("lady gaga" not in videoName) and ("official music video" not in videoName) and ("lyrics" not in videoName)
                            and (("just dance" in videoName) or ("justdance" in videoName))):
                            
                            tituloChannel=search_result["snippet"]["channelTitle"]
                            tituloChannel = unidecode.unidecode(tituloChannel)

                            idChannel=search_result["snippet"]["channelId"]
                            videoPublishedAt=search_result["snippet"]["publishedAt"] #2017-02-13T02:52:38Z
                            
                            print("######################")
                            #print("#############################################")
                            print("Titulo: ", search_result["snippet"]["title"])
                            print("Video ID: ",search_result["id"]["videoId"])
                            print("Published at: ",search_result["snippet"]["publishedAt"])

                            videoID = search_result["id"]["videoId"]
                            if videoID not in lista_videoID:
                                lista_videoID.append(videoID)

                                # get stats of video ...
                                try:
                                    time.sleep(1)
                                    DEVELOPER_KEY = "AIzaSyAL0ChC4DB6Su9C6X3YVDJMMzly0o_Mq_4"
                                    yt = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
                                    requestStats = yt.videos().list(
                                            part='id,statistics', id=videoID, maxResults=100
                                    ).execute()
                                    #if search_result["items"]["kind"] == "youtube#video":
                                    #print(requestStats)
                                    print(">>>>>>> stats video >>>>>>>>")
                                    #print(requestStats["items"])
                                    print("VIEWS = "+requestStats["items"][0]["statistics"]["viewCount"])
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
                                    print("Total comments video = ",nrCommentsV)
                                    print(">>>>>>>>>>>>>>>>>>>>>>>>>\n")


                                    if(int(nrCommentsV) > 0):
                                        print("getting comments of video ...")
                                        comments=[]
                                        likes=[]
                                        commentsID = []
                                        data = []

                                        nextPT = None
                                        while 1: #comentarios do videoID
                                            try:
                                                time.sleep(0.4)
                                                #print("get main comments ...")
                                                #DEVELOPER_KEY = "AIzaSyAP6m_Icjnn2npBnwM4sSVK4VT5kKoOe7o" renato 1a
                                                #DEVELOPER_KEY = "AIzaSyAWq5YNDdZRc0cdh__4iQh2E-qJp7mcvNQ" #new renato
                                                #DEVELOPER_KEY = "AIzaSyAilu0HwaDQlvkDZEsKxQ6POFMdyvKiU4E" #me quota
                                                #DEVELOPER_KEY = "AIzaSyBiRFpFQdLOgPWfMFTaklcq2twvQESDQZ0" #coimvivio
                                                DEVELOPER_KEY ="AIzaSyDXIzN7IV034Isli8V6Od-c7IyxUahQ4tc" #manel
                                                yt_c = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

                                                comment_response = yt_c.commentThreads().list(
                                                    part='snippet,replies', videoId=videoID, maxResults=100,
                                                    order='relevance', textFormat='plainText',pageToken=nextPT).execute()
                                                nextPT = comment_response.get('nextPageToken')
                                                for comment_result in comment_response.get("items",[]):

                                                    #while (nrComentarios < nrComentariosStats): ... parecido ao dos replies

                                                    #print(comment_result)
                                                    #print(comment_result['snippet']['topLevelComment']['snippet']['textDisplay'])
                                                    comentario = comment_result['snippet']['topLevelComment']['snippet']['textDisplay']

                                                    # if commentario not in english: break , else: do it

                                                    #comentario = unidecode.unidecode(comentario)
                                                    #nrComentarios+=1

                                                    nr_likes = comment_result['snippet']['topLevelComment']['snippet']['likeCount']
                                                    commentID = comment_result['snippet']['topLevelComment']['id']
                                                    #print(comment_result['snippet']['topLevelComment']['snippet']['updatedAt'])
                                                    publishTime = comment_result['snippet']['topLevelComment']['snippet']['updatedAt']
                                                    # updatedAt pq pode incluir possiveis correcoes, ao inves do comment original com "publishedAt"
                                                    
                                                    data.append(publishTime)
                                                    commentsID.append(commentID)
                                                    comments.append(comentario)
                                                    likes.append(nr_likes)

                                                    # add to db ... check if is JD or JD now by video title

                                                    nr_replies = comment_result['snippet']['totalReplyCount']
                                                    #print(" . . . replies stats = ", nr_replies)
                                                    countReplies = 0

                                                    nextPTreply = None #page token
                                                    if (nr_replies > 0):
                                                        try:
                                                            time.sleep(0.2)
                                                            #DEVELOPER_KEY = "AIzaSyAP6m_Icjnn2npBnwM4sSVK4VT5kKoOe7o" renato 1a
                                                            DEVELOPER_KEY = "AIzaSyBiRFpFQdLOgPWfMFTaklcq2twvQESDQZ0" #coimvivio
                                                            #DEVELOPER_KEY ="AIzaSyDXIzN7IV034Isli8V6Od-c7IyxUahQ4tc" #manel nos comments
                                                            #DEVELOPER_KEY = "AIzaSyBptCUsM32WTIHs8TfLg7I8EFELkUCXcic" #new 2
                                                            yt_r = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

                                                            while (countReplies <= nr_replies):
                                                                commentsReplies = yt_r.comments().list(
                                                                    parentId = commentID, part='id,snippet', maxResults=100, pageToken=nextPTreply).execute()
                                                                nextPTreply = commentsReplies.get('nextPageToken')
                                                                for r in commentsReplies.get("items",[]):
                                                                    #print(r)
                                                                    replyID = r['id']
                                                                    textReply = r['snippet']['textDisplay']
                                                                    likesReply = r['snippet']['likeCount']
                                                                    publishedAtReply = r['snippet']['updatedAt']

                                                                    #print(r['snippet']['textDisplay'])
                                                                    #nrComentarios+=1
                                                                    countReplies+=1

                                                                    data.append(publishedAtReply)
                                                                    commentsID.append(replyID)
                                                                    comments.append(textReply)
                                                                    likes.append(likesReply)

                                                                    # add to db ... check if is JD or JD now by video title

                                                                    #print(" ...... replies lidos = # ",countReplies)

                                                                if ((nextPTreply is None)):
                                                                    #print("$$ fim replies")
                                                                    #print("replies lidos = ",countReplies)
                                                                    break
                                                        
                                                        except HttpError as e:
                                                            print("comments() - replies — An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
                                                            if("quotaExceeded" in str(e.content)):
                                                                time.sleep(60*60*2)
                                                        #except (ConnectionError, ReadTimeout):
                                                            #print("ERROR! Connection or TIME OUT!")
                                                        except:
                                                            print("comments() - replies — something wrong ...")

                                                    #print(" . . . replies lidos = ",countReplies)
                                                
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
                                                    time.sleep(60*60*2)
                                                if("commentsDisabled" in str(e.content)):
                                                    print("COMENTARIOS DESATIVADOS...")
                                                    break
                                            #except (ConnectionError, ReadTimeout):
                                                #print("ERROR! Connection or TIME OUT!")
                                            except:
                                                print("commentThreads() - something wrong ...")

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
                                        #print(dict)
                                        #print("\n")
                                        #print(out_df)
                                        conta += 1
                                        print("—————————————————————————————————————————————————————————————————————")
                                        print("Writing csv ...")
                                        print(">>>   VIDEO # ", conta)
                                        #print(". . . nr comentarios total = ",nrComentarios)
                                        writedComments+=len(comments)
                                        print(" . . writed comments = ",writedComments)
                                        print("—————————————————————————————————————————————————————————————————————")

                                        #print(". . . stats total comentarios = ", contaStatsComments)
                                        #first time
                                        #if(conta==1):
                                        #    out_df.to_csv(nameCSV, mode='a', header=True,index=False)
                                        #else: #sem header
                                        #    out_df.to_csv(nameCSV, mode='a', header=False,index=False)

                                        #atualiza dados
                                        out_df.to_csv(nameCSV, mode='a', header=False,index=False)   
                                        time.sleep(0.6)
                                    else:
                                        print("NO COMMENTS!")
                                        #break
                                        continue        
                                except HttpError as e:
                                    print("videos (stats) — An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
                                    if("quotaExceeded" in str(e.content)):
                                        time.sleep(60*60*2) #6h
                                #except (ConnectionError, ReadTimeout):
                                    #print("ERROR! Connection or TIME OUT!")
                                except:
                                    print("videos (stats) - something wrong ...")
                                #print("\n")
                                #print(comments, commentsID)
                                #print(len(comments))
                                
                            else:
                                print(" X REJECT! Video repetido\n")
                                break
                        else:
                            print(" X REJECT! lady gaga or something else\n")
                            continue
                time.sleep(0.25)
                if nextPage_token is None:
                    print("\n~~~~ nr de videos atual: ", conta)
                    #time.sleep(20)
                    break #sem break, começa tudo de novo
            except HttpError as e:
                print("search() — An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
                if("quotaExceeded" in str(e.content)):
                    time.sleep(60*60*2)
            #except (ConnectionError, ReadTimeout):
                #print("ERROR! Connection or TIME OUT!")
            except:
                print("search () - something wrong ...")
                #DEVELOPER_KEY = "AIzaSyAL0ChC4DB6Su9C6X3YVDJMMzly0o_Mq_4" #backup
                #DEVELOPER_KEY = "AIzaSyAilu0HwaDQlvkDZEsKxQ6POFMdyvKiU4E" #3a
                #youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

        #print("Videos:\n", "\n".join(videos), "\n")
        #lista_videoID
        print("--- fim ---\n nr de videos: ",conta)
        #print("nr comentarios: ",nrComentarios)

