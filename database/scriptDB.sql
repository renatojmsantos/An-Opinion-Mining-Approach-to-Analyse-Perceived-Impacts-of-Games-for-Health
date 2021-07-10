CREATE TABLE video (
	channelid		 VARCHAR(512) NOT NULL,
	channeltitle	 VARCHAR(512) NOT NULL,
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

CREATE TABLE annotation (
	annotationid	 INTEGER,
	field		 VARCHAR(512) NOT NULL,
	concept		 VARCHAR(512) NOT NULL,
	comment_commentid VARCHAR(512) NOT NULL,
	game_game_id	 INTEGER NOT NULL,
	video_videoid	 VARCHAR(512) NOT NULL,
	PRIMARY KEY(annotationid)
);

CREATE TABLE game (
	game_id	 INTEGER,
	edition	 VARCHAR(512) NOT NULL,
	platform VARCHAR(512) NOT NULL,
	PRIMARY KEY(game_id)
);

CREATE TABLE comment (
	commentid	 VARCHAR(512),
	originaltext	 VARCHAR(9999) NOT NULL,
	processedtext VARCHAR(9999) NOT NULL,
	polarity	 VARCHAR(512) NOT NULL,
	likes	 INTEGER NOT NULL,
	datecomment	 DATE NOT NULL,
	maincomment	 VARCHAR(512) NOT NULL,
	PRIMARY KEY(commentid)
);

ALTER TABLE annotation ADD CONSTRAINT annotation_fk1 FOREIGN KEY (comment_commentid) REFERENCES comment(commentid);
ALTER TABLE annotation ADD CONSTRAINT annotation_fk2 FOREIGN KEY (game_game_id) REFERENCES game(game_id);
ALTER TABLE annotation ADD CONSTRAINT annotation_fk3 FOREIGN KEY (video_videoid) REFERENCES video(videoid);

