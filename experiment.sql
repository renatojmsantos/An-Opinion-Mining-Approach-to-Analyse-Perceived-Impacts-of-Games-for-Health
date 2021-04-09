insert into game values('Just Dance');
insert into game values('Just Dance Now');
insert into sentiment values ('Positive','0.3');
insert into youtube values ('YouTube', 1, 'channel Ubisoft', 1,'Titulo video just dance 2020', '2020-01-02', 320321, 125, 10, 430);
insert into opinion values (1,'just dance the best game',1,'2020-01-02','Just Dance', 'Positive', '1', True);
insert into opinion_usability values (1,'Errors');
insert into opinion_ux values (1,'Trust');

select * from opinion;
select * from sentiment;
select * from game;
select * from youtube;
insert into usability values('Satisfaction');
insert into usability values('Errors');
insert into ux values('Trust');
select * from usability;
select * from opinion_usability;
select * from opinion_ux;
select * from health;
select * from ux;


truncate table opinion_usability;
truncate table opinion_health;
truncate table opinion_ux;
truncate table youtube cascade;
truncate table opinion cascade;

CREATE TABLE usability (
	uconcept VARCHAR(512),
	PRIMARY KEY(uconcept)
);

CREATE TABLE ux (
	uxconcept VARCHAR(512),
	PRIMARY KEY(uxconcept)
);


select o.comment_commentid, c.commentid, o.dimension_dimension_id, d.dimension_id, d.field
from opinion o, dimension d, comment c
where o.dimension_dimension_id = d.dimension_id and o.comment_commentid = c.commentid
#------------------------------------------------------------------------------------------------------------------------------------------------------------------


select h.health_hconcept, ux.ux_uxconcept from opinion_health h, opinion_ux ux where h.opinion_commentid= ux.opinion_commentid;
select h.health_hconcept, h.opinion_commentid, ux.ux_uxconcept, ux.opinion_commentid, u.usability_uconcept, u.opinion_commentid from opinion_health h, opinion_ux ux, opinion_usability u where h.opinion_commentid=ux.opinion_commentid and h.opinion_commentid=u.opinion_commentid;

#------------------------------------------------------------------------------------------------------------------------------------------------------------------

select distinct h.health_hconcept, h.opinion_commentid, ux.ux_uxconcept, ux.opinion_commentid, u.usability_uconcept, u.opinion_commentid
from opinion_health h, opinion_ux ux, opinion_usability u
where h.opinion_commentid=ux.opinion_commentid and h.opinion_commentid=u.opinion_commentid;
#------------------------------------------------------------------------------------------------------------------------------------------------------------------

select field, count(distinct comment_commentid) as count
from (
    select o.comment_commentid, o.dimension_dimension_id, d.dimension_id, d.field
    from opinion o, dimension d
    where o.dimension_dimension_id = d.dimension_id
) as fi
group by field;
#------------------------------------------------------------------------------------------------------------------------------------------------------------------

select field, count(*) as count
from (
    select o.comment_commentid, c.commentid, o.dimension_dimension_id, d.dimension_id, d.field
    from opinion o, dimension d, comment c
    where o.dimension_dimension_id = d.dimension_id and o.comment_commentid = c.commentid
    
) as fi
group by field;

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
select concept, count(*) as c from dimension where field = 'UX' group by concept
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
with u as(
    select count(distinct o.dimension_dimension_id) as usability from opinion o, dimension d where d.field='Usability'
),
ux as(
    select count(distinct o.dimension_dimension_id) as userexperience from opinion o, dimension d where d.field='User Experience'
),
h as(
    select count(distinct o.dimension_dimension_id) as health from opinion o, dimension d where d.field='health'
)
select usability, userexperience, health from u, ux, h 

#------------------------------------------------------------------------------------------------------------------------------------------------------------------

select count(distinct o.dimension_dimension_id) from opinion o, dimension d where d.field='Usability'

#------------------------------------------------------------------------------------------------------------------------------------------------------------------

with u as(
    select count(*) as usability from opinion_usability
),
ux as(
    select count(*) as userexperience from opinion_ux
),
h as(
    select count(*) as health from opinion_health
)
select usability, userexperience, health from u, ux, h [[where opinion_commentid = {{Field}}]];

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
select count(*) as u from opinion_usability [[where u = {{usability}}]



