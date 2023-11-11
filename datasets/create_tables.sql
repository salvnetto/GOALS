-- Ligas
CREATE TABLE futebol.leagues (
	id INT PRIMARY KEY,
	name VARCHAR(255)
);

INSERT INTO futebol.leagues (id, name) VALUES
	(0, 'Brasileirao A'),
    (1, 'Premier League'),
    (2, 'Serie A TIM'),
    (3, 'Bundesliga'),
	(4, 'La Liga');


-- Times
CREATE TABLE futebol.teams (
	team_id INT PRIMARY KEY,
	league_id INT,
	team_name VARCHAR(255),
	FOREIGN KEY (league_id) REFERENCES futebol.leagues(id)
);

-- Historico
CREATE TABLE futebol.match_history (
    game_id INT PRIMARY KEY,
    "date" DATE,
    comp VARCHAR(255),
    round INT,
    venue VARCHAR(255),
    "result" VARCHAR(255),
    gf INT,
    ga INT,
    opponent VARCHAR(255),
    xg NUMERIC,
    xga NUMERIC,
    poss INT,
    sh INT,
    sot INT,
	saves INT,
    cmp INT,
    att INT,
    prgp INT,
    kp INT,
    pass_3rd INT,
    sw INT,
    crs INT,
    sca INT,
    gca INT,
    tkl INT,
    tklw INT,
    tkl_def_3rd INT,
    tkl_att_3rd INT,
    blocks INT,
    "int" INT,
    touches_att_3rd INT,
    fls INT,
    "off" INT,
    recov INT,
    season INT,
    team VARCHAR(255),
    days INT,
    time_diff NUMERIC,
	home_team_id INT,
	away_team_id INT,
	league_id INT,
    FOREIGN KEY (home_team_id) REFERENCES futebol.teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES futebol.teams(team_id),
	FOREIGN KEY (league_id) REFERENCES futebol.leagues(id)
);

-- Tabela de colocação
CREATE TABLE futebol.standings (
	season INT,
    rk INT,
	team_id INT,
    team_name VARCHAR(255),
    league_id INT,
    mp INT,
    w INT,
    d INT,
    l INT,
    gf INT,
    ga INT,
    gd INT,
    pts INT,
    "pts/mp" NUMERIC,
    xg NUMERIC,
    xga NUMERIC,
    xgd NUMERIC,
    "xgd/90" NUMERIC,
    league_name VARCHAR(255),
    xg_conv NUMERIC,
    xga_conv NUMERIC,
    att_rating NUMERIC,
    def_rating NUMERIC,
    naive_rating NUMERIC,
	FOREIGN KEY (team_id) REFERENCES futebol.teams(team_id),
	FOREIGN KEY (league_id) REFERENCES futebol.leagues(id)
);

-- Rodadas
CREATE TABLE futebol.rounds (
    wk NUMERIC,
    xg_casa NUMERIC,
    xg_fora NUMERIC,
    home VARCHAR(255),
    gols_casa VARCHAR(255),
    gols_fora VARCHAR(255),
    away VARCHAR(255),
    league_name VARCHAR(255),
    home_id INT,
    away_id INT,
    league_id INT,
    FOREIGN KEY (home_id) REFERENCES futebol.teams(team_id),
    FOREIGN KEY (away_id) REFERENCES futebol.teams(team_id),
	FOREIGN KEY (league_id) REFERENCES futebol.leagues(id)
);