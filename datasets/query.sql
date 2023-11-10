CREATE TABLE futebol.leagues (
	league_id INT PRIMARY KEY,
	league_name VARCHAR(255),
	league_season INT
);

CREATE TABLE futebol.teams (
	team_id INT PRIMARY KEY,
	league_id INT,
	team_name VARCHAR(255),
	FOREIGN KEY (league_id) REFERENCES futebol.leagues(league_id)
);

CREATE TABLE futebol.squad (
	team_id INT,
	player_name VARCHAR(255),
	coach_name VARCHAR(255),
	FOREIGN KEY (team_id) REFERENCES futebol.teams(team_id)
);

CREATE TABLE futebol.match_history (
    game_id INT PRIMARY KEY,
    date DATE,
    comp VARCHAR(255),
    round INT,
    "day" INT,
    venue VARCHAR(255),
    "result" VARCHAR(255),
    gf INT,
    ga INT,
    opponent VARCHAR(255),
    xg NUMERIC,
    xga NUMERIC,
    poss NUMERIC,
    sh NUMERIC,
    sot NUMERIC,
    season INT,
    team VARCHAR(255),
    days INT,
    time_diff NUMERIC,
	home_team_id INT,
	away_team_id INT,
    FOREIGN KEY (home_team_id) REFERENCES futebol.teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES futebol.teams(team_id)
);

