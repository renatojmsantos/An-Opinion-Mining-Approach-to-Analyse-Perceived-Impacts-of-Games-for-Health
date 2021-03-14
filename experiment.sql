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

CREATE TABLE usability (
	uconcept VARCHAR(512),
	PRIMARY KEY(uconcept)
);

CREATE TABLE ux (
	uxconcept VARCHAR(512),
	PRIMARY KEY(uxconcept)
);