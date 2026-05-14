DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS family_member;
DROP TABLE IF EXISTS family_member_user;
DROP TABLE IF EXISTS log_entry;
DROP TABLE IF EXISTS entry_types;
DROP TABLE IF EXISTS entry_durations;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL
);

CREATE TABLE family_member (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

CREATE TABLE family_member_user (
  family_member_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  PRIMARY KEY (family_member_id, user_id),
  FOREIGN KEY (family_member_id) REFERENCES family_member (id),
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE log_entry (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  family_member_id INTEGER,
  entry_type INTEGER NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (family_member_id) REFERENCES family_member (id),
  FOREIGN KEY (entry_type) REFERENCES entry_types (id)
);

CREATE TABLE entry_types (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  has_duration BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE entry_durations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  entry_id INTEGER NOT NULL,
  start TIMESTAMP NOT NULL,
  end TIMESTAMP,
  FOREIGN KEY (entry_id) REFERENCES log_entry (id)
);