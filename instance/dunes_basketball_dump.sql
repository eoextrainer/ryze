PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE clubs (
	id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	tier VARCHAR(10) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	city VARCHAR(120), 
	logo_path VARCHAR(255), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (name), 
	UNIQUE (email)
);
INSERT INTO clubs VALUES(1,'Paris Basketball','Pro A','contact@parisbball.fr','pbkdf2:sha256:600000$9gn1GSuED4zoBKgV$57058a665e686746c5dfd80f23f403bff46d54449321c32e1c8a31c9571bc90f','Paris',NULL,'2025-12-10 11:22:13.747138');
INSERT INTO clubs VALUES(2,'Monaco Basketball','Pro A','contact@monaco.fr','pbkdf2:sha256:600000$WyxkOWsrAAsSybbO$6e5547ac68b5e6bce71bd788bdf10cc7689ae47a334d364eb0d3d5a3149d309c','Monaco',NULL,'2025-12-10 11:22:13.747143');
INSERT INTO clubs VALUES(3,'Asvel Lyon','Pro A','contact@asvel.fr','pbkdf2:sha256:600000$M4Zrrws6gmzExG6W$f49c5dde86cb7154b5d3c3e29e58dfc9a9f4fcae2c73398cce8295ff8a24a024','Lyon',NULL,'2025-12-10 11:22:13.747144');
INSERT INTO clubs VALUES(4,'Strasbourg IG','Pro B','contact@strasbourg.fr','pbkdf2:sha256:600000$LoW9VJMCIzpIIzj1$a658576f1089c0778e9943864fefa1dbc6bf851a38c9646241118947d7b91025','Strasbourg',NULL,'2025-12-10 11:22:13.747146');
INSERT INTO clubs VALUES(5,'Dijon Basketball','Pro B','contact@dijon.fr','pbkdf2:sha256:600000$TOiHl2DJ3ttf2V6t$9da08b5d1b886cdb42776ef1adeff4b7dad8c28f5d36df5c3a8abbb7a42286a6','Dijon',NULL,'2025-12-10 11:22:13.747147');
INSERT INTO clubs VALUES(6,'Nanterre 92','Pro B','contact@nanterre.fr','pbkdf2:sha256:600000$yINqWnX9lnkXWQr9$c407915963550f0a0776cb5f448040dcc9f6882495c688094653d11511f759f8','Nanterre',NULL,'2025-12-10 11:22:13.747148');
INSERT INTO clubs VALUES(7,'Boulogne-Levallois','N1','contact@boulogne.fr','pbkdf2:sha256:600000$xS7HiLqEIZfmUVbK$3e9173c72fc102e3fc231c806dd189e8a84abe45239fbfed5d5881f76ce257bd','Boulogne',NULL,'2025-12-10 11:22:13.747149');
INSERT INTO clubs VALUES(8,'Saint-Quentin','N1','contact@stquentin.fr','pbkdf2:sha256:600000$GCs9hGO1pDBKfHTv$fa68136259475f2bd16423c0ea070df4105a475535246bc0c182fa2392346b5d','Saint-Quentin',NULL,'2025-12-10 11:22:13.747150');
INSERT INTO clubs VALUES(9,'Roanne','N1','contact@roanne.fr','pbkdf2:sha256:600000$thltXZPnaPrpd3FH$e9784b0531b813857b12a3af71203598dcaacf457c12c6954108551e6ec4d702','Roanne',NULL,'2025-12-10 11:22:13.747152');
INSERT INTO clubs VALUES(10,'Toulouse','N2','contact@toulouse.fr','pbkdf2:sha256:600000$8XbhI71nqKVC6ni5$9341e3eeda43560ef825e06594a1d9444cd98c7d834dc0afcd719e05f648035f','Toulouse',NULL,'2025-12-10 11:22:13.747153');
INSERT INTO clubs VALUES(11,'Marseille','N2','contact@marseille.fr','pbkdf2:sha256:600000$GaJnIxUJy8eDUml8$2d21190acff3dcc718285e35b3378f7a6ca6c293536e26b2552f10dfc5ff8faa','Marseille',NULL,'2025-12-10 11:22:13.747154');
INSERT INTO clubs VALUES(12,'Bordeaux','N2','contact@bordeaux.fr','pbkdf2:sha256:600000$tU5beA65fADHxeAZ$d3d6f53ff8024107ae3d7ab005d750a5c11a38c395a964e46f159771c991ad4c','Bordeaux',NULL,'2025-12-10 11:22:13.747155');
INSERT INTO clubs VALUES(13,'Lille','N3','contact@lille.fr','pbkdf2:sha256:600000$e0KXeuVzAElc77pc$a0b2c71bf5dc782948c711320013747ead7abb7f4f8f60497bbb1cc22f143e57','Lille',NULL,'2025-12-10 11:22:13.747156');
INSERT INTO clubs VALUES(14,'Nice','N3','contact@nice.fr','pbkdf2:sha256:600000$AIcp37EboQPf3dE2$c0099c727a360987854aa413f2c83a1b96d18b9d4177c3746e4ca1b8b3d8818b','Nice',NULL,'2025-12-10 11:22:13.747157');
INSERT INTO clubs VALUES(15,'Nantes','N3','contact@nantes.fr','pbkdf2:sha256:600000$NQCWmtIKAyBL58sn$2bd9f27281ad5fba921a893d12f37b485ece14b23c9a2a51f9470ffb43953fe0','Nantes',NULL,'2025-12-10 11:22:13.747158');
CREATE TABLE players (
	id INTEGER NOT NULL, 
	first_name VARCHAR(120) NOT NULL, 
	last_name VARCHAR(120) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	date_of_birth DATE, 
	height FLOAT, 
	weight FLOAT, 
	nationality VARCHAR(120), 
	position VARCHAR(50), 
	photo_path VARCHAR(255), 
	subscription_tier VARCHAR(20) NOT NULL, 
	subscription_start DATETIME, 
	subscription_end DATETIME, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
/****** CORRUPTION ERROR *******/
CREATE TABLE club_player (
	id INTEGER NOT NULL, 
	club_id INTEGER NOT NULL, 
	player_id INTEGER NOT NULL, 
	status VARCHAR(20), 
	PRIMARY KEY (id), 
	FOREIGN KEY(club_id) REFERENCES clubs (id), 
	FOREIGN KEY(player_id) REFERENCES players (id)
);
/****** CORRUPTION ERROR *******/
CREATE TABLE player_stats (
	id INTEGER NOT NULL, 
	player_id INTEGER NOT NULL, 
	points_per_game FLOAT, 
	assists_per_game FLOAT, 
	rebounds_per_game FLOAT, 
	field_goal_percentage FLOAT, 
	speed_kmh FLOAT, 
	attack_performance_score FLOAT, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(player_id) REFERENCES players (id)
);
/****** CORRUPTION ERROR *******/
CREATE TABLE performances (
	id INTEGER NOT NULL, 
	player_id INTEGER NOT NULL, 
	game_date DATE NOT NULL, 
	points INTEGER, 
	assists INTEGER, 
	rebounds INTEGER, 
	field_goals_made INTEGER, 
	field_goals_attempted INTEGER, 
	opponent VARCHAR(120), 
	PRIMARY KEY (id), 
	FOREIGN KEY(player_id) REFERENCES players (id)
);
/****** CORRUPTION ERROR *******/
CREATE TABLE player_resume (
	id INTEGER NOT NULL, 
	player_id INTEGER NOT NULL, 
	club_id INTEGER NOT NULL, 
	season_start INTEGER, 
	season_end INTEGER, 
	is_current BOOLEAN, 
	is_future BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(player_id) REFERENCES players (id), 
	FOREIGN KEY(club_id) REFERENCES clubs (id)
);
/****** CORRUPTION ERROR *******/
CREATE TABLE news (
	id INTEGER NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	content TEXT, 
	category VARCHAR(50) NOT NULL, 
	club_id INTEGER, 
	player_id INTEGER, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(club_id) REFERENCES clubs (id), 
	FOREIGN KEY(player_id) REFERENCES players (id)
);
/****** CORRUPTION ERROR *******/
CREATE TABLE agents (
	id INTEGER NOT NULL, 
	first_name VARCHAR(120) NOT NULL, 
	last_name VARCHAR(120) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	agency VARCHAR(120), 
	city VARCHAR(120), 
	phone VARCHAR(40), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
ROLLBACK; -- due to errors
