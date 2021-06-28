from connectDB import *

#from preprocessing import *

def deleteRow(query):
	idBack = None
	conn = None
	
	try:
		params = config()
		conn = psycopg2.connect(**params)
		conn.autocommit = True
		cur = conn.cursor()

		query = query + " returning *;" 
		#print(query)
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

def deleteRows(query):
	idBack = None
	conn = None
	
	try:
		params = config()
		conn = psycopg2.connect(**params)
		conn.autocommit = True
		cur = conn.cursor()

		query = query + " returning *;" 
		#print(query)
		cur.execute(query)
		idBack = cur.fetchall()
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

def getCommentsID():
	
	try:
		idBack = None
		conn = None
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		query = "select comment_commentid from annotation group by comment_commentid;"
		#print(query)
		cur.execute(query)

		idBack = cur.fetchall()
		
		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO! get comments", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

def getCommentsCaracteres():
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()
		#processedtext, originaltext
		query = "SELECT commentid FROM comment where length(originaltext) < 4"
		#query = "SELECT originaltext,commentid, (array_length(regexp_split_to_array(originaltext, '\s+'),1)) as pals FROM comment join annotation on annotation.comment_commentid = comment.commentid group by originaltext, commentid order by pals"
		#print(query)
		cur.execute(query)
		idBack = cur.fetchall()

		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO get annotation!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

def getComments():
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()
		#processedtext, originaltext
		query = "SELECT originaltext,commentid, (array_length(regexp_split_to_array(originaltext, '\s+'),1)) as pals FROM comment join annotation on annotation.comment_commentid = comment.commentid group by originaltext, commentid order by pals asc"
		#query = "SELECT originaltext,commentid, (array_length(regexp_split_to_array(originaltext, '\s+'),1)) as pals FROM comment join annotation on annotation.comment_commentid = comment.commentid group by originaltext, commentid order by pals"
		#print(query)
		cur.execute(query)
		idBack = cur.fetchall()

		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO get annotation!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

def getIDs(commentid):
	
	try:
		idBack = None
		conn = None
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		#query = "SELECT annotationid, comment_commentid FROM annotationid where comment_commentid='"+commentid+"' group by annotationid, comment_commentid"
		
		query = "select annotation.*from (select annotation.*, min(annotationid) over (partition by comment_commentid) as min_id, row_number() over (partition by comment_commentid order by annotationid) as seqnum from annotation) annotation where annotationid - seqnum != min_id - 1 and comment_commentid='"+str(commentid)+"' order by annotationid asc"

		#print(query)
		cur.execute(query)

		idBack = cur.fetchall()
		
		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO! get comments", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

def getDupAnnotationID():
	
	try:
		idBack = None
		conn = None
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		#query = "SELECT annotationid, comment_commentid FROM annotationid where comment_commentid='"+commentid+"' group by annotationid, comment_commentid"
		
		query = "select annotation.*from (select annotation.*, min(annotationid) over (partition by comment_commentid) as min_id, row_number() over (partition by comment_commentid order by annotationid) as seqnum from annotation) annotation where annotationid - seqnum != min_id - 1 order by annotationid asc"

		#print(query)
		cur.execute(query)

		idBack = cur.fetchall()
		
		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO! get comments", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack

def getTopAnnotation():
	
	try:
		idBack = None
		conn = None
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()

		#query = "SELECT annotationid, comment_commentid FROM annotationid where comment_commentid='"+commentid+"' group by annotationid, comment_commentid"
		"""
		SELECT annotation.comment_commentid, count(concept) as total, (array_length(regexp_split_to_array(originaltext, '\s+'),1)) as pals, comment.originaltext
		FROM annotation
		join comment on comment.commentid = annotation.comment_commentid
		where (array_length(regexp_split_to_array(originaltext, '\s+'),1)) < 25 
		group by annotation.comment_commentid, comment.originaltext
		having count(concept) > 12
		order by count(concept) desc
		"""
		#3,8
		query = "SELECT annotation.comment_commentid, count(concept) as total, (array_length(regexp_split_to_array(originaltext, '\s+'),1)) as pals, comment.originaltext FROM annotation join comment on comment.commentid = annotation.comment_commentid where (array_length(regexp_split_to_array(originaltext, '\s+'),1)) < 4  group by annotation.comment_commentid, comment.originaltext having count(concept) > 4 order by count(concept) desc"

		#print(query)
		cur.execute(query)

		idBack = cur.fetchall()
		
		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO! get comments", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack



def deleteDuplicated():

	try:
		"""
		commentids = getCommentsID() # É preciso ? 

		for cids in commentids:
			cid = cids[0]
			try:
				a = getIDs(cid)
				for i in a:
					aid = i[0]
					query = "delete from annotation where annotationid = "+str(aid)+""
					deleteRow(query)

			except Exception as e:
				print(e)
		"""

		a = getDupAnnotationID()
		try:
			for i in a:
				aid = i[0]
				query = "delete from annotation where annotationid = "+str(aid)+""
				deleteRow(query)

		except Exception as e:
			print(e)
	except Exception as e:
		print(e)
	
def deleteNonEnglish():
	try:
		comments = getComments() 
		for c in comments:
			original = c[0]
			#print("\n",original)
			cid = c[1]
			try:
				if(isEnglish(str(original.lower())) is False):
					if(isEnglish(str(original.lower())) is False):
						print(len(original.split())," DELETE... ", original)
						query = "delete from annotation where comment_commentid = '"+str(cid)+"'"
						deleteRows(query)
						query = "delete from comment where commentid = '"+str(cid)+"'"
						deleteRow(query)
			except Exception as e:
				print(e)
	except Exception as e:
		print(e)

def menor3caracteres():

	try:
		c = getCommentsCaracteres()
		for i in c:
			cid = i[0]
			query = "delete from annotation where comment_commentid = '"+str(cid)+"'"
			deleteRows(query)
			query = "delete from comment where commentid = '"+str(cid)+"'"
			deleteRow(query)
	except Exception as e:
		print(e)

def removeNon(cid):
	query = "delete from annotation where comment_commentid = '"+str(cid)+"'"
	deleteRows(query)
	query = "delete from comment where commentid = '"+str(cid)+"'"
	deleteRow(query)


def deleteTops():
	try:
		c = getTopAnnotation()
		for i in c:
			cid = i[0]
			query = "delete from annotation where comment_commentid = '"+str(cid)+"'"
			deleteRows(query)
			#query = "delete from comment where commentid = '"+str(cid)+"'"
			#deleteRow(query)
	except Exception as e:
		print(e)


# ===================================================================

def getCommentsSentiment():
	idBack = None
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		#conn.autocommit = True
		cur = conn.cursor()
		#query = "SELECT commentid from comment where polarity = 'Neutral' order by commentid limit 25000"
		
		query = "SELECT annotationid from comment join annotation on annotation.comment_commentid = comment.commentid where polarity = 'Neutral' and concept = 'Hedonic'"

		cur.execute(query)
		idBack = cur.fetchall()

		cur.close()
		#return idBack
	except (Exception, psycopg2.DatabaseError) as error:
		print("ERRO get annotation!", error)
	finally:
		if conn is not None:
			#print("closing connection...")
			conn.close()
	return idBack# is not None #idBack


def removeSentiment():
	try:
		c = getCommentsSentiment()
		for i in c:
			cid = i[0]
			
			query = "delete from annotation where annotationid = '"+str(cid)+"'"
			deleteRow(query)

			#query = "delete from annotation where comment_commentid = '"+str(cid)+"'"
			#deleteRows(query)
			#query = "delete from comment where commentid = '"+str(cid)+"'"
			#deleteRow(query)
			
	except Exception as e:
		print(e)


removeSentiment()

#menor3caracteres()

#deleteNonEnglish()

#deleteTops()
#deleteDuplicated()

"""
removeNon('UgwEd5Nq8riGYQGokUp4AaABAg')
removeNon('UgwNdMQQ7laOhp3CxHd4AaABAg')
removeNon('UgwQuSGcKWzEKyOV2rJ4AaABAg')
removeNon('Ugx0oVVBJdDW6TxSYoZ4AaABAg')
removeNon('UgwAz72KFJHYd56LbGh4AaABAg')
removeNon('Ugg164wF3FHDVXgCoAEC')
removeNon('UgxMfOKbsW4V9JTSlDt4AaABAg')
removeNon('UgjYVwM3DscabngCoAEC')
removeNon('UghALkP-M1vimngCoAEC')
removeNon('UgwjYYVXR0p_fDKFOGJ4AaABAg')
removeNon('UggmX20HOTXj1HgCoAEC')
removeNon('UghKSw08bnhxDngCoAEC')
removeNon('Ugi-OisBADM_NHgCoAEC')
removeNon('UgiRxy5YpjMVOXgCoAEC')
removeNon('UgipAbpp7W22hHgCoAEC')
removeNon('UggGDnuLJfUrKXgCoAEC')
removeNon('UgjXPXH8rG_VAngCoAEC')
removeNon('UgjNJbIvGppyw3gCoAEC')
removeNon('UgiP-MgbxhH-u3gCoAEC')
removeNon('UggOvwqP7hPLWngCoAEC')
removeNon('Ugj5veEzu7O1UngCoAEC')
removeNon('UgwQeovvRJzvdLvlNER4AaABAg')
removeNon('UgwfU56pb1i3xZf8lOF4AaABAg')
removeNon('UgwiVlfUlvF_ynXezKV4AaABAg')
removeNon('Ugwmph_8D28QL_ojGMp4AaABAg')
removeNon('UgyX76KbL1PKbg6EzO94AaABAg')
removeNon('UgygbxZhcXGXbcddnhB4AaABAg')
removeNon('UgyLRu7dr6SPoFLAzUB4AaABAg')
removeNon('UginUBcKKm2LhHgCoAEC')
"""



"""

select annotation.*
from (select annotation.*,
             min(annotationid) over (partition by comment_commentid) as min_id,
             row_number() over (partition by comment_commentid order by annotationid) as seqnum
      from annotation
     ) annotation
where annotationid - seqnum != min_id - 1 
order by annotationid asc
"""

"""
select annotation.*
from (select annotation.*,
			 min(annotationid) over (partition by comment_commentid) as min_id,
			 row_number() over (partition by comment_commentid order by annotationid) as seqnum
	  from annotation
	 ) annotation
where annotationid - seqnum != min_id - 1 and comment_commentid='UgyXjn9CECevOIm8yQt4AaABAg'
order by annotationid asc
"""


# ver se comment_comment id está nas anotações a partir de 1 200 000 / 12000 e remover essas linhas

"""
SELECT distinct comment_commentid, comment.originaltext,  count(concept) as "total"
FROM annotation
join comment on comment.commentid = annotation.comment_commentid
join game on game.game_id = annotation.game_game_id
group by comment.originaltext, annotation.comment_commentid
order by count(concept) desc
LIMIT 50

select commentid, originaltext
from comment
where commentid = 'Ugyyd-GJKHkbitKi_yt4AaABAg'

select *
from annotation
where comment_commentid='Ugwc_gPl8w9OZCEoMVd4AaABAg'

SELECT annotationid, field, concept, comment_commentid
FROM annotation 
WHERE comment_commentid IN (SELECT comment_commentid 
               FROM annotation
               WHERE annotationid > 12000)
order by annotationid

select annotation.*
from (select annotation.*,
             count(*) over (partition by comment_commentid) as commentid_cnt,
             max(annotationid) over (partition by comment_commentid) as max_commentid_id,
             max(annotationid) over () as max_id
      from annotation
     ) annotation
where max_id = max_commentid_id and commentid_cnt > 1
order by annotationid;

select *
from annotation
order by annotationid desc
limit 100

select * from annotation where comment_commentid = 'Ugxuz1bq-Fg1COrb6xl4AaABAg'

select *
from video
where videoid='R91TENdjt2w'

select *
from annotation
where comment_commentid = 'Ugw7RK6vGYs91-p53Ql4AaABAg'

select *
from comment
where commentid = 'Ugw7RK6vGYs91-p53Ql4AaABAg'
"""