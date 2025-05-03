DROP TABLE IF EXISTS
  challengematch,
  comment,
  activity,
  tag,
  usertag,
  projecttag,
  project,
  users
CASCADE;


CREATE TABLE tag (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL
);

CREATE TABLE users (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
nationality TEXT ,
created_at TIMESTAMPTZ DEFAULT NOW(),
last_active_at TIMESTAMPTZ DEFAULT NOW(),
total_points INTEGER DEFAULT 0
);

CREATE TABLE usertag (
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  tag_id INTEGER REFERENCES tag(id) ON DELETE CASCADE,
  PRIMARY KEY (user_id, tag_id)
);

CREATE TABLE project (
id SERIAL PRIMARY KEY,
user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
title TEXT,
description_raw TEXT,
description_ai TEXT,
generated_name TEXT,
created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE projecttag (
  project_id INTEGER REFERENCES project(id) ON DELETE CASCADE,
  tag_id INTEGER REFERENCES tag(id) ON DELETE CASCADE,
  PRIMARY KEY (project_id, tag_id)
);

CREATE TABLE activity (
id SERIAL PRIMARY KEY,
description TEXT NOT NULL,
event_type TEXT NOT NULL,
points INTEGER NOT NULL,
created_at TIMESTAMPTZ DEFAULT NOW(),
tag_id INTEGER REFERENCES tag(id) ON DELETE CASCADE
);

CREATE TABLE comment (
id SERIAL PRIMARY KEY,
from_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
to_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
text TEXT NOT NULL,
created_at TIMESTAMPTZ DEFAULT NOW(),
votes INTEGER DEFAULT 0
);

CREATE TABLE challengematch (
id SERIAL PRIMARY KEY,
from_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
to_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
activity_id INTEGER REFERENCES activity(id) ON DELETE CASCADE,
status TEXT NOT NULL DEFAULT 'pendiente',
created_at TIMESTAMPTZ DEFAULT NOW(),
updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_name ON users(name);
CREATE INDEX idx_project_users ON project(user_id);
