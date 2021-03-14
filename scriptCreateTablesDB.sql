CREATE TABLE youtube (
	source		 VARCHAR(512),
	channelid		 VARCHAR(512),
	channeltitle	 VARCHAR(512),
	videoid		 VARCHAR(512) NOT NULL,
	videotitle	 VARCHAR(512) NOT NULL,
	datevideo		 DATE,
	viewsvideo	 BIGINT,
	likesvideo	 INTEGER,
	dislikesvideo	 INTEGER,
	totalcommentsvideo BIGINT,
	PRIMARY KEY(videoid)
);

CREATE TABLE opinion (
	commentid		 VARCHAR(512),
	comment		 VARCHAR(4096) NOT NULL,
	likes		 NUMERIC(8,2) NOT NULL,
	datecomment	 DATE NOT NULL,
	maincomment	 BOOL,
	game_name		 VARCHAR(512) NOT NULL,
	sentiment_polarity VARCHAR(512) NOT NULL,
	youtube_videoid	 VARCHAR(512) NOT NULL,
	PRIMARY KEY(commentid)
);

CREATE TABLE sentiment (
	polarity	 VARCHAR(512),
	subjectivity NUMERIC(8,2),
	PRIMARY KEY(polarity)
);

CREATE TABLE usability (
	uconcept VARCHAR(512),
	PRIMARY KEY(uconcept)
);

CREATE TABLE ux (
	uxconcept VARCHAR(512),
	PRIMARY KEY(uxconcept)
);

CREATE TABLE health (
	hconcept VARCHAR(512),
	PRIMARY KEY(hconcept)
);

CREATE TABLE game (
	name VARCHAR(512),
	PRIMARY KEY(name)
);

CREATE TABLE opinion_ux (
	opinion_commentid VARCHAR(512),
	ux_uxconcept	 VARCHAR(512),
	PRIMARY KEY(opinion_commentid,ux_uxconcept)
);

CREATE TABLE opinion_health (
	opinion_commentid VARCHAR(512),
	health_hconcept	 VARCHAR(512),
	PRIMARY KEY(opinion_commentid,health_hconcept)
);

CREATE TABLE opinion_usability (
	opinion_commentid	 VARCHAR(512),
	usability_uconcept VARCHAR(512),
	PRIMARY KEY(opinion_commentid,usability_uconcept)
);

ALTER TABLE opinion ADD CONSTRAINT opinion_fk1 FOREIGN KEY (game_name) REFERENCES game(name);
ALTER TABLE opinion ADD CONSTRAINT opinion_fk2 FOREIGN KEY (sentiment_polarity) REFERENCES sentiment(polarity);
ALTER TABLE opinion ADD CONSTRAINT opinion_fk3 FOREIGN KEY (youtube_videoid) REFERENCES youtube(videoid);
ALTER TABLE opinion_ux ADD CONSTRAINT opinion_ux_fk1 FOREIGN KEY (opinion_commentid) REFERENCES opinion(commentid);
ALTER TABLE opinion_ux ADD CONSTRAINT opinion_ux_fk2 FOREIGN KEY (ux_uxconcept) REFERENCES ux(uxconcept);
ALTER TABLE opinion_health ADD CONSTRAINT opinion_health_fk1 FOREIGN KEY (opinion_commentid) REFERENCES opinion(commentid);
ALTER TABLE opinion_health ADD CONSTRAINT opinion_health_fk2 FOREIGN KEY (health_hconcept) REFERENCES health(hconcept);
ALTER TABLE opinion_usability ADD CONSTRAINT opinion_usability_fk1 FOREIGN KEY (opinion_commentid) REFERENCES opinion(commentid);
ALTER TABLE opinion_usability ADD CONSTRAINT opinion_usability_fk2 FOREIGN KEY (usability_uconcept) REFERENCES usability(uconcept);

