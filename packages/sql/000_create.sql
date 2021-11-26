drop table if exists complient;
drop table if exists resident;
drop table if exists room;
drop table if exists hostel;
drop table if exists usr;

CREATE TABLE usr(
    id VARCHAR(20) PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone VARCHAR(20),
    password VARCHAR(20),
    is_admin BOOLEAN
);

CREATE TABLE hostel(
    id VARCHAR(10) PRIMARY KEY,
    Hname TEXT,
    Nroom INTEGER
);

CREATE TABLE room(
    id VARCHAR(10) PRIMARY KEY,
    vacancy INTEGER,
    capacity INTEGER,
    hid VARCHAR(10),
    FOREIGN KEY (hid) REFERENCES hostel(id)
);

CREATE TABLE resident(
    sid VARCHAR(20),
    rid VARCHAR(10),
    FOREIGN KEY (sid) REFERENCES usr(id),
    FOREIGN KEY (rid) REFERENCES room(id)
);

CREATE TABLE complient(
    Cno SERIAL PRIMARY KEY,
    Ctype VARCHAR(20),
    description TEXT,
    sid VARCHAR(20),
    rid VARCHAR(10),
    hid VARCHAR(10),
    FOREIGN KEY (hid) REFERENCES hostel(id),
    FOREIGN KEY (sid) REFERENCES usr(id),
    FOREIGN KEY (rid) REFERENCES room(id)
);
