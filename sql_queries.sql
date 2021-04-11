# dimensions presents on comments

select field as Field, count(distinct comment_commentid) as count
from (
    select comment_commentid, field
    from annotation 
) as fi
group by field;


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
GROUP BY edition
ORDER BY edition ASC

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