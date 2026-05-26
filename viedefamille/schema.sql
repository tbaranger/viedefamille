DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS family_member;
DROP TABLE IF EXISTS user_family_members;
DROP TABLE IF EXISTS entry_type;
DROP TABLE IF EXISTS log_entry;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL
);

CREATE TABLE family_member (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

CREATE TABLE user_family_members (
  user_id INTEGER NOT NULL,
  family_member_id INTEGER NOT NULL,
  PRIMARY KEY (user_id, family_member_id),
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (family_member_id) REFERENCES family_member (id)
);

CREATE TABLE entry_type(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  unit TEXT
);

CREATE TABLE log_entry (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  event_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  family_member_id INTEGER,
  entry_type_id INTEGER NOT NULL,
  amount INTEGER,
  comments TEXT,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (family_member_id) REFERENCES family_member (id),
  FOREIGN KEY (entry_type_id) REFERENCES entry_type (id)
);