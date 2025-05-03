DROP TABLE IF EXISTS
  challengematch,
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
id TEXT PRIMARY KEY,
name TEXT,
role TEXT NOT NULL DEFAULT 'participant',
nationality TEXT ,
created_at TIMESTAMPTZ DEFAULT NOW(),
last_active_at TIMESTAMPTZ DEFAULT NOW(),
total_points INTEGER DEFAULT 0
);

CREATE TABLE usertag (
  user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
  tag_id INTEGER REFERENCES tag(id) ON DELETE CASCADE,
  PRIMARY KEY (user_id, tag_id)
);

CREATE TABLE project (
id SERIAL PRIMARY KEY,
user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
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
active BOOLEAN DEFAULT TRUE,
points INTEGER NOT NULL,
created_at TIMESTAMPTZ DEFAULT NOW(),
tag_id INTEGER REFERENCES tag(id) ON DELETE CASCADE
);

CREATE TABLE post (
id SERIAL PRIMARY KEY,
from_user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
to_user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
activity_id INTEGER REFERENCES activity(id) ON DELETE CASCADE,
status TEXT NOT NULL DEFAULT 'pendiente',
created_at TIMESTAMPTZ DEFAULT NOW(),
updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_name ON users(name);
CREATE INDEX idx_project_users ON project(user_id);
