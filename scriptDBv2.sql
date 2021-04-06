CREATE TABLE video (
	channelid		 VARCHAR(512),
	channeltitle	 VARCHAR(512),
	videoid		 VARCHAR(512) NOT NULL,
	videotitle	 VARCHAR(512) NOT NULL,
	datevideo		 DATE,
	viewsvideo	 BIGINT,
	likesvideo	 INTEGER,
	dislikesvideo	 INTEGER,
	totalcommentsvideo BIGINT,
	description	 VARCHAR(3000) NOT NULL,
	PRIMARY KEY(videoid)
);

CREATE TABLE opinion (
	opinionid		 INTEGER,
	comment_commentid	 VARCHAR(512) NOT NULL,
	dimension_dimension_id INTEGER NOT NULL,
	game_game_id		 INTEGER NOT NULL,
	video_videoid		 VARCHAR(512) NOT NULL,
	PRIMARY KEY(opinionid)
);

CREATE TABLE game (
	game_id	 INTEGER,
	edition	 VARCHAR(512),
	platform VARCHAR(512),
	PRIMARY KEY(game_id)
);

CREATE TABLE dimension (
	dimension_id INTEGER,
	field	 VARCHAR(512),
	concept	 VARCHAR(512),
	PRIMARY KEY(dimension_id)
);

CREATE TABLE comment (
	commentid	 VARCHAR(512),
	comment	 VARCHAR(512) NOT NULL,
	polarity	 VARCHAR(512) NOT NULL,
	likes	 INTEGER NOT NULL,
	datecomment DATE NOT NULL,
	maincomment BOOL NOT NULL,
	PRIMARY KEY(commentid)
);

ALTER TABLE opinion ADD CONSTRAINT opinion_fk1 FOREIGN KEY (comment_commentid) REFERENCES comment(commentid);
ALTER TABLE opinion ADD CONSTRAINT opinion_fk2 FOREIGN KEY (dimension_dimension_id) REFERENCES dimension(dimension_id);
ALTER TABLE opinion ADD CONSTRAINT opinion_fk3 FOREIGN KEY (game_game_id) REFERENCES game(game_id);
ALTER TABLE opinion ADD CONSTRAINT opinion_fk4 FOREIGN KEY (video_videoid) REFERENCES video(videoid);

