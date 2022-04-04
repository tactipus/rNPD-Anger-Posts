DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
  id TEXT PRIMARY KEY,
  title TEXT,
  link TEXT,
  author TEXT,
  score TEXT,
  time_created TEXT,
  comms_num TEXT,
  body TEXT,
  ups TEXT
);