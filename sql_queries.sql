# dimensions presents on comments

select field as Field, count(distinct comment_commentid) as count
from (
    select comment_commentid, field
    from annotation 
) as fi
group by field;

#vocabulary
SELECT "public"."annotation"."concept" AS "concept", count(*) AS "count"
FROM "public"."annotation"
LEFT JOIN "public"."comment" "Comment - Comment Comment" ON "public"."annotation"."comment_commentid" = "Comment - Comment Comment"."commentid"
GROUP BY "public"."annotation"."concept"
ORDER BY "public"."annotation"."concept" ASC

# tentativa...
SELECT concept, count(distinct comment_commentid)
from annotation
where concept LIKE 'Motivation%'
group by concept
having count(distinct comment_commentid) > 2
order by count (distinct comment_commentid) desc

#vocabulary sql
SELECT annotation.concept, count(distinct comment_commentid) 
FROM annotation
LEFT JOIN comment ON annotation.comment_commentid = comment.commentid
where {{concept}}
GROUP BY annotation.concept
ORDER BY annotation.concept ASC

# tentativa...
select concept, count(*)
from annotation
where exists (select 1
              from annotation
              where 1=1 [[AND {{concept}} ]][[AND annotation.concept LIKE CONCAT('%',{{concept}},'%')]]
             )
group by concept;

# WORKS!!!
select concept, count(*)
from annotation
where exists (select 1
              from annotation a2
              where a2.comment_commentid = annotation.comment_commentid and a2.concept = 'Fatigue'
             )
group by concept;

#... mb discusse.. WORKS
select a1.concept, count(*) from annotation a1 where exists (select 1 from annotation where annotation.comment_commentid = a1.comment_commentid and {{concept}} ) group by a1.concept;

#corrigido vocabulario
SELECT a1.concept, count(distinct comment_commentid) 
FROM annotation a1
LEFT JOIN comment ON comment.commentid = a1.comment_commentid
left join game on game.game_id = a1.game_game_id
left join video on video.videoid = a1.video_videoid
where exists (select 1
              from annotation
              where {{concept}} and {{polarity}} and {{field}} and {{dateComment}} and {{edition}} and {{platform}} and {{channel}}
              and annotation.comment_commentid= a1.comment_commentid
             )
GROUP BY a1.concept
ORDER BY a1.concept ASC

# DIMENSIONS
SELECT a1.field, count(distinct comment_commentid) 
FROM annotation a1
JOIN comment ON comment.commentid = a1.comment_commentid
join game on game.game_id = a1.game_game_id
join video on video.videoid = a1.video_videoid
where exists (select 1
              from annotation
              where {{concept}} and {{polarity}} and {{field}} and {{dateComment}} and {{edition}} and {{platform}} and {{channel}}
              and annotation.comment_commentid= a1.comment_commentid
             )
GROUP BY a1.field
ORDER BY a1.field DESC


# usability analysis
select concept, count(distinct comment_commentid)
from annotation 
join comment on comment.commentid = annotation.comment_commentid
join game on game.game_id = annotation.game_game_id
left join video on video.videoid = annotation.video_videoid
where field = 'Usability' and {{concept}} and {{polarity}} and {{dateComment}} and {{edition}} and {{platform}} and {{field}} and {{channel}}
group by concept
# fix to...
SELECT a1.concept, count(distinct comment_commentid) 
FROM annotation a1
JOIN comment ON comment.commentid = a1.comment_commentid
join game on game.game_id = a1.game_game_id
join video on video.videoid = a1.video_videoid
where exists (select 1
              from annotation
              where {{concept}} and {{polarity}} and a1.field = 'Usability' and {{dateComment}} and {{edition}} and {{platform}} and {{channel}}
              and annotation.comment_commentid= a1.comment_commentid
             )
GROUP BY a1.concept
ORDER BY a1.concept ASC



# likes dislikes on videos
SELECT date_trunc('year', video.datevideo) as "Date", max(video.likesvideo) as "Likes", max(video.dislikesvideo) as "Dislikes"
FROM video
join annotation on video.videoid = annotation.video_videoid
join game on game.game_id = annotation.game_game_id
join comment on comment.commentid = annotation.comment_commentid
where {{polarity}} and {{field}} and {{concept}} and {{dateVideo}} and {{edition}} and {{platform}} and {{channel}}
GROUP BY date_trunc('year', video.datevideo)
ORDER BY date_trunc('year', video.datevideo) ASC


SELECT polarity, count(distinct commentid)
FROM comment
left join annotation on annotation.comment_commentid = comment.commentid 
left join game on game.game_id = annotation.game_game_id
left join video on video.videoid = annotation.video_videoid
where {{polarity}} and {{field}} and {{concept}} and {{dateComment}} and {{edition}} and {{platform}} and {{channel}}
GROUP BY comment.polarity
ORDER BY count(distinct commentid) DESC

#sentiment over time
SELECT date_trunc('year', comment.datecomment) as "Date", 
    count(*) filter (where polarity = 'Positive') as positive,
    count(*) filter (where polarity = 'Neutral') as neutral,
    count(*) filter (where polarity = 'Negative') as negative,
FROM comment
left join annotation on annotation.comment_commentid = comment.commentid 
left join game on game.game_id = annotation.game_game_id
left join video on video.videoid = annotation.video_videoid
GROUP BY date_trunc('year', comment.datecomment)
ORDER BY date_trunc('year', comment.datecomment) ASC

# likes on comments
SELECT date_trunc('year', comment.datecomment) as "Date", max(likes) as "Likes"
FROM comment
join annotation on comment.commentid = annotation.comment_commentid
join game on game.game_id = annotation.game_game_id
join video on video.videoid = annotation.video_videoid
GROUP BY date_trunc('year', comment.datecomment)
ORDER BY date_trunc('year', comment.datecomment) ASC





















#as text
select concept, count(*)
from annotation
where exists (select 1
              from annotation a2
              where a2.comment_commentid = annotation.comment_commentid and a2.concept = {{searchConcept}}
             )
group by concept;


#...
DECLARE @parm NVARCHAR(50);
SET @parm = (SELECT concept from annotation where {{concept}} LIMIT 1);


#work + 1 filtro
SELECT annotation.concept, count(distinct comment_commentid) 
FROM annotation
LEFT JOIN comment ON annotation.comment_commentid = comment.commentid
left join game on game.game_id = annotation.game_game_id
left join video on video.videoid = annotation.video_videoid
where exists (select 1
              from annotation a2
              where {{concept}} and {{polarity}} and {{field}} and {{dateComment}} and {{edition}} and {{platform}}
              and a2.comment_commentid = annotation.comment_commentid [[and a2.concept = {{searchConcept}}]]
             )
GROUP BY annotation.concept
ORDER BY annotation.concept ASC

#...
select value, count(*)
from t
where exists (select 1
              from t t2
              where t2.textid = t.textid and t2.value = 'Hedonic'
             )
group by value;


# u analysis
select concept, count(*) as count from annotation where field = 'Usability' group by concept

#ux
select concept, count(*) as total from annotation where field = 'UX' group by concept


# WORKS!!!
select field, count(distinct comment_commentid)
from annotation 
join comment on comment.commentid = annotation.comment_commentid
join game on game.game_id = annotation.game_game_id
where {{field}} and {{concept}} and {{polarity}} and {{date}} and {{edition}} and {{platform}}
group by field;

# ----
select concept, count(distinct comment_commentid)
from annotation 
join comment on comment.commentid = annotation.comment_commentid
join game on game.game_id = annotation.game_game_id
where field = 'Usability' and {{concept}} and {{polarity}} and {{dateComment}} and {{edition}} and {{platform}}
group by concept
# ----
SELECT polarity, count(distinct commentid)
FROM comment
left join annotation on comment.commentid = annotation.comment_commentid
left join game on game.game_id = annotation.game_game_id
where {{polarity}} and {{field}} and {{concept}} and {{dateComment}} and {{edition}} and {{platform}}
GROUP BY comment.polarity
ORDER BY comment.polarity ASC

# date comment
SELECT date_trunc('month', comment.datecomment), count(distinct commentid) 
FROM comment
left join annotation on comment.commentid = annotation.comment_commentid
left join game on game.game_id = annotation.game_game_id
where {{polarity}} and {{field}} and {{concept}} and {{dateComment}} and {{edition}} and {{platform}}
GROUP BY date_trunc('month', comment.datecomment)
ORDER BY date_trunc('month', comment.datecomment) ASC

#video data
SELECT date_trunc('month', video.datevideo), count(distinct videoid) 
FROM video
left join annotation on video.videoid = annotation.video_videoid
left join game on game.game_id = annotation.game_game_id
left join comment on comment.commentid = annotation.comment_commentid
where {{polarity}} and {{field}} and {{concept}} and {{dateVideo}} and {{edition}} and {{platform}}
GROUP BY date_trunc('month', video.datevideo)
ORDER BY date_trunc('month', video.datevideo) ASC



#game
SELECT edition, count(distinct game_id)
FROM game
left join annotation on game.game_id = annotation.game_game_id
left join video on video.videoid = annotation.video_videoid
left join comment on comment.commentid = annotation.comment_commentid
where {{polarity}} and {{field}} and {{concept}} and {{dateVideo}} and {{edition}} and {{platform}}
GROUP BY edition
ORDER BY edition ASC

# channel
SELECT video.channeltitle, count(distinct videoid) 
FROM video
left join annotation on video.videoid = annotation.video_videoid
left join game on game.game_id = annotation.game_game_id
left join comment on comment.commentid = annotation.comment_commentid
where {{polarity}} and {{field}} and {{concept}} and {{dateVideo}} and {{edition}} and {{platform}} and {{channel}}
GROUP BY video.channeltitle
ORDER BY video.channeltitle ASC

# comments
SELECT distinct originaltext, polarity, likes, maincomment
FROM comment
left join annotation on comment.commentid = annotation.comment_commentid
left join game on game.game_id = annotation.game_game_id
where {{polarity}} and {{field}} and {{concept}} and {{dateComment}} and {{edition}} and {{platform}}
order by likes desc
LIMIT 2000

# original date comment
SELECT date_trunc('month', CAST("public"."comment"."datecomment" AS timestamp)) AS "datecomment", count(*) AS "count"
FROM "public"."comment"
GROUP BY date_trunc('month', CAST("public"."comment"."datecomment" AS timestamp))
ORDER BY date_trunc('month', CAST("public"."comment"."datecomment" AS timestamp)) ASC


# example 
SELECT * FROM 
   table1 
JOIN table2 ON table2.t1_id = table1.id
WHERE {{dateFieldWidget}}
#...
SELECT * FROM table1 t1
JOIN table2 t2 ON t2.t1_id = t1.id
WHERE t2.received_at >= (SELECT DATE_TRUNC('day', received_at) FROM table2 WHERE {{dateFieldFilter}} ORDER BY received_at ASC LIMIT 1) AND
    t2.received_at <= (SELECT DATE_TRUNC('day', received_at) FROM table2 WHERE {{dateFieldFilter}} ORDER BY received_at DESC LIMIT 1)
#...
SELECT
   alias1.column1 AS alias1_column1,
   alias2.column1 AS alias2_column1
FROM sometable AS alias1
INNER JOIN sometable AS alias2 ON (alias1.join_id = alias2.id)
[[ WHERE {{alias1.my_variable}} ]]