DROP TABLE IF EXISTS roles;

CREATE TABLE roles (id INTEGER PRIMARY KEY,description TEXT);

INSERT INTO roles (id, description) VALUES (1, 'Muggle - No magical ability'), (2, 'Squib - No practical magic'),(3, 'Wizard - Can use basic spells'),(4, 'Auror - Advanced dark magic defense');




DROP TABLE IF EXISTS wands;
CREATE TABLE wands (id INTEGER PRIMARY KEY AUTOINCREMENT,owner TEXT,wood TEXT,core TEXT,length TEXT);


DROP TABLE IF EXISTS sorting_hat;
CREATE TABLE sorting_hat (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,house TEXT);

INSERT INTO sorting_hat (name, house) VALUES ('Harry Potter', 'Gryffindor'), ('Hermione Granger', 'Gryffindor'), ('Draco Malfoy', 'Slytherin'), ('Luna Lovegood', 'Ravenclaw');
CREATE TABLE flags (id INTEGER PRIMARY KEY, flag TEXT);
INSERT INTO flags (flag) VALUES ('1ng3neer2k25{h0gwarts_sess10n_m4g1c_leak}');