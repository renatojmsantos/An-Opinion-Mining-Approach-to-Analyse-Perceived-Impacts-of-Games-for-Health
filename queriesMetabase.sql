
# left join -> tudo
# join -> só anotados

https://justdance.dei.uc.pt/public/dashboard/c218930a-9dea-4126-8212-9b9f4e662eb8?dimension={{column:dimension}}

# stacked chart - annotation of each edition
SELECT concept as "Concept", count(distinct comment_commentid) as "Total", game.edition as "Edition"
FROM annotation
join game on game.game_id = annotation.game_game_id
join comment on comment.commentid = annotation.comment_commentid
join video on video.videoid = annotation.video_videoid
where {{concept}} and {{dimension}} and {{polarity}} and {{datecomment}} and {{edition}} and {{platform}}
GROUP BY concept, game.edition
ORDER BY count(distinct comment_commentid) desc

# channels
SELECT video.channeltitle, count(distinct video.videoid) 
FROM video
left join annotation on video.videoid = annotation.video_videoid
left join game on game.game_id = annotation.game_game_id
left join comment on comment.commentid = annotation.comment_commentid
where {{polarity}} and {{field}} and {{concept}} and {{dateComment}} and {{edition}} and {{platform}} and {{channel}}
GROUP BY video.channeltitle
ORDER BY count(distinct video.videoid) desc


#comment annotated of over time
SELECT date_trunc('year', comment.datecomment) as "Year", count(distinct comment.commentid) as "Total"
FROM comment
join annotation on comment.commentid = annotation.comment_commentid
join game on game.game_id = annotation.game_game_id
join video on video.videoid = annotation.video_videoid
where {{polarity}} and {{field}} and {{concept}} and {{dateComment}} and {{edition}} and {{platform}} 
GROUP BY date_trunc('year', comment.datecomment)
ORDER BY date_trunc('year', comment.datecomment) ASC

# comments over time
SELECT date_trunc('year', comment.datecomment) as "Year", count(distinct comment.commentid) as "Total"
FROM comment
left join annotation on comment.commentid = annotation.comment_commentid
left join game on game.game_id = annotation.game_game_id
left join video on video.videoid = annotation.video_videoid
where {{polarity}} and {{field}} and {{concept}} and {{dateComment}} and {{edition}} and {{platform}} and {{channel}}
GROUP BY date_trunc('year', comment.datecomment)
ORDER BY date_trunc('year', comment.datecomment) ASC

# dimensions on comments
SELECT a1.field, count(distinct comment_commentid) 
FROM annotation a1
join comment ON comment.commentid = a1.comment_commentid
join game on game.game_id = a1.game_game_id
join video on video.videoid = a1.video_videoid
where exists (select 1
              from annotation
              where {{concept}} and {{polarity}} and {{field}} and {{dateComment}} and {{edition}} and {{platform}} and {{channel}}
              and annotation.comment_commentid= a1.comment_commentid
             )
GROUP BY a1.field
ORDER BY a1.field DESC

#editions
SELECT edition, count(distinct game_id)
FROM game
left join annotation on game.game_id = annotation.game_game_id
left join video on video.videoid = annotation.video_videoid
left join comment on comment.commentid = annotation.comment_commentid
where {{polarity}} and {{field}} and {{concept}} and {{datecomment}} and {{edition}} and {{platform}} and {{channel}} 
GROUP BY game.edition
ORDER BY count(distinct game.game_id) desc

# edidions all
SELECT edition, count(distinct game_id)
FROM game
join annotation on game.game_id = annotation.game_game_id
join video on video.videoid = annotation.video_videoid
join comment on comment.commentid = annotation.comment_commentid
where {{polarity}} and {{field}} and {{concept}} and {{datecomment}} and {{edition}} and {{platform}} and {{channel}} 
GROUP BY game.edition
ORDER BY count(distinct game.game_id) desc

# likes on comments
SELECT date_trunc('year', comment.datecomment) as "Date", sum(comment.likes) as "Likes"
FROM comment
left join annotation on comment.commentid = annotation.comment_commentid
left join game on game.game_id = annotation.game_game_id
left join video on video.videoid = annotation.video_videoid
where {{polarity}} and {{field}} and {{concept}} and {{dateComment}} and {{edition}} and {{platform}} and {{channel}}
GROUP BY date_trunc('year', comment.datecomment)
ORDER BY date_trunc('year', comment.datecomment) ASC

#likes vs dislikes videos
SELECT date_trunc('year', video.datevideo) as "Date", sum(video.likesvideo) as "Likes", sum(video.dislikesvideo) as "Dislikes"
FROM video
join annotation on video.videoid = annotation.video_videoid
join game on game.game_id = annotation.game_game_id
join comment on comment.commentid = annotation.comment_commentid
where {{polarity}} and {{field}} and {{concept}} and {{dateComment}} and {{edition}} and {{platform}} and {{channel}}
GROUP BY date_trunc('year', video.datevideo)
ORDER BY date_trunc('year', video.datevideo) ASC

# new channels
SELECT date_trunc('month', video.datevideo) as "Date", count(distinct video.channelid)
FROM video
left join annotation on video.videoid = annotation.video_videoid
left join game on game.game_id = annotation.game_game_id
left join comment on comment.commentid = annotation.comment_commentid
where {{polarity}} and {{field}} and {{concept}} and {{edition}} and {{platform}} and {{channel}}  and {{datecomment}} 
GROUP BY date_trunc('month', video.datevideo)
ORDER BY date_trunc('month', video.datevideo) ASC

# new comments
SELECT date_trunc('month', comment.datecomment) as "Date", count(distinct comment.commentid)
FROM comment
left join annotation on comment.commentid = annotation.comment_commentid
left join game on game.game_id = annotation.game_game_id
left join video on video.videoid = annotation.video_videoid
where {{polarity}} and {{field}} and {{concept}} and {{dateComment}} and {{edition}} and {{platform}} and {{channel}}
GROUP BY date_trunc('month', comment.datecomment)
ORDER BY date_trunc('month', comment.datecomment) ASC

# new comments annotated
SELECT date_trunc('month', comment.datecomment) as "Date", count(distinct comment.commentid)
FROM comment
join annotation on comment.commentid = annotation.comment_commentid
join game on game.game_id = annotation.game_game_id
join video on video.videoid = annotation.video_videoid
where {{polarity}} and {{field}} and {{concept}} and {{dateComment}} and {{edition}} and {{platform}} 
GROUP BY date_trunc('month', comment.datecomment)
ORDER BY date_trunc('month', comment.datecomment) ASC

# new videos
SELECT date_trunc('month', video.datevideo) as "Date", count(distinct video.videoid)
FROM video
left join annotation on video.videoid = annotation.video_videoid
left join game on game.game_id = annotation.game_game_id
left join comment on comment.commentid = annotation.comment_commentid
where {{polarity}} and {{field}} and {{concept}} and {{dateComment}} and {{edition}} and {{platform}} and {{channel}}
GROUP BY date_trunc('month', video.datevideo)
ORDER BY date_trunc('month', video.datevideo) ASC

# health
SELECT a1.concept, count(distinct comment_commentid) 
FROM annotation a1
JOIN comment ON comment.commentid = a1.comment_commentid
join game on game.game_id = a1.game_game_id
join video on video.videoid = a1.video_videoid
where exists (select 1
              from annotation
              where {{concept}} and {{polarity}} and a1.field = 'Health' and {{dateComment}} and {{edition}} and {{platform}} and {{channel}} and {{field}}
              and annotation.comment_commentid= a1.comment_commentid
             )
GROUP BY a1.concept
ORDER BY a1.concept ASC

# plataform
SELECT platform, count(distinct game.game_id)
FROM game
join annotation on game.game_id = annotation.game_game_id
join video on video.videoid = annotation.video_videoid
join comment on comment.commentid = annotation.comment_commentid
where {{polarity}} and {{field}} and {{concept}} and {{datecomment}} and {{edition}} and {{platform}} and {{channel}} and platform!='Unknown'
GROUP BY platform
ORDER BY count(distinct game.game_id) desc

# sentiment analysis
SELECT polarity, count(distinct comment.commentid)
FROM comment
join annotation on annotation.comment_commentid = comment.commentid 
join game on game.game_id = annotation.game_game_id
join video on video.videoid = annotation.video_videoid
where {{polarity}} and {{field}} and {{concept}} and {{dateComment}} and {{edition}} and {{platform}} and {{channel}}
GROUP BY comment.polarity
ORDER BY count(distinct comment.commentid) DESC

# sentiment over time
SELECT date_trunc('year', comment.datecomment) as "Date", 
    count(distinct comment.commentid) filter (where polarity = 'Positive') as positive,
    count(distinct comment.commentid) filter (where polarity = 'Neutral') as neutral,
    count(distinct comment.commentid) filter (where polarity = 'Negative') as negative
FROM comment
left join annotation on annotation.comment_commentid = comment.commentid 
left join game on game.game_id = annotation.game_game_id
left join video on video.videoid = annotation.video_videoid
where {{polarity}} and {{field}} and {{concept}} and {{dateComment}} and {{edition}} and {{platform}} and {{channel}}
GROUP BY date_trunc('year', comment.datecomment)
ORDER BY date_trunc('year', comment.datecomment) ASC


# top 100 comments
SELECT distinct originaltext as "Comment", likes as "Likes"
FROM comment
left join annotation on comment.commentid = annotation.comment_commentid
left join game on game.game_id = annotation.game_game_id
left join video on video.videoid = annotation.video_videoid
where {{polarity}} and {{field}} and {{concept}} and {{dateComment}} and {{edition}} and {{platform}} and {{channel}}
order by likes desc
LIMIT 100


# upload videos
SELECT date_trunc('year', video.datevideo) as "Date", count(distinct video.videoid) 
FROM video
left join annotation on video.videoid = annotation.video_videoid
left join game on game.game_id = annotation.game_game_id
left join comment on comment.commentid = annotation.comment_commentid
where {{polarity}} and {{field}} and {{concept}} and {{date}} and {{edition}} and {{platform}} and {{channel}}
GROUP BY date_trunc('year', video.datevideo)
ORDER BY date_trunc('year', video.datevideo) ASC

# usability 
SELECT a1.concept, count(distinct comment_commentid) 
FROM annotation a1
JOIN comment ON comment.commentid = a1.comment_commentid
join game on game.game_id = a1.game_game_id
join video on video.videoid = a1.video_videoid
where exists (select 1
              from annotation
              where {{concept}} and {{polarity}} and a1.field = 'Usability' and {{dateComment}} and {{edition}} and {{platform}} and {{channel}} and {{field}}
              and annotation.comment_commentid= a1.comment_commentid
             )
GROUP BY a1.concept
ORDER BY a1.concept ASC

# ux
SELECT a1.concept, count(distinct a1.comment_commentid) 
FROM annotation a1
join comment ON comment.commentid = a1.comment_commentid
join game on game.game_id = a1.game_game_id
join video on video.videoid = a1.video_videoid
where exists (select 1
              from annotation
              where {{concept}} and {{polarity}} and a1.field = 'UX' and {{dateComment}} and {{edition}} and {{platform}} and {{channel}} and {{field}}
              and annotation.comment_commentid= a1.comment_commentid
             )
GROUP BY a1.concept
ORDER BY a1.concept ASC

# views
SELECT date_trunc('year', video.datevideo), sum(video.viewsvideo)
FROM video
left join annotation on annotation.video_videoid = video.videoid
left join game on game.game_id = annotation.game_game_id
left join comment on comment.commentid = annotation.comment_commentid
where {{polarity}} and {{field}} and {{concept}} and {{dateComment}} and {{edition}} and {{platform}} and {{channel}}
GROUP BY date_trunc('year', video.datevideo)
ORDER BY date_trunc('year', video.datevideo) ASC

# vocabulary
SELECT a1.field, a1.concept, count(distinct comment_commentid)
FROM annotation a1
JOIN comment ON comment.commentid = a1.comment_commentid
join game on game.game_id = a1.game_game_id
where exists (select 1
              from annotation
              where {{concept}} and {{polarity}} and {{field}} and {{dateComment}} and {{edition}} and {{platform}}
              and annotation.comment_commentid= a1.comment_commentid
             )
GROUP BY a1.concept, a1.field
ORDER BY a1.field desc

# nr de letras
select length(originaltext)
from comment

#grafico
select length(originaltext) as l, count(originaltext) as lenght
from comment
where length(originaltext) < 500
group by l


# 11 pals em media
select avg(array_length(regexp_split_to_array(originaltext, '\s+'),1)) as pals
from comment
order by pals asc


# gif
 ![image description](https://media.giphy.com/media/3oKIPEqDGUULpEU0aQ/giphy.gif)

# most frequentes words
select word, nentry from ts_stat($$ select to_tsvector('english',processedtext) from comment join annotation on annotation.comment_commentid = comment.commentid where concept='Frustration' $$)
where word != 'face' and word != 'im' and word != 'one' and word != '2' and word != '3' and word != '1'
order by nentry desc
limit 30;

#presence of dimensions editions jd
SELECT field as "Dimension", count(distinct comment_commentid) as "Total", game.edition as "Edition"
FROM annotation
join game on game.game_id = annotation.game_game_id
join comment on comment.commentid = annotation.comment_commentid
join video on video.videoid = annotation.video_videoid
where {{concept}} and {{dimension}} and {{polarity}} and {{datecomment}} and {{edition}} and {{platform}}
GROUP BY field, game.edition
ORDER BY count(distinct comment_commentid) desc



