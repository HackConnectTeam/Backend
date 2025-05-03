DROP TABLE IF EXISTS
  challenge_match,
  comment,
  activity_log,
  tag,
  user_tag,
  project_tag,
  project,
  users
CASCADE;

CREATE TABLE tag (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL
);

CREATE TABLE users (
id SERIAL PRIMARY KEY,
name TEXT UNIQUE NOT NULL,
created_at TIMESTAMPTZ DEFAULT NOW(),
last_active_at TIMESTAMPTZ DEFAULT NOW(),
total_points INTEGER DEFAULT 0
);

CREATE TABLE user_tag (
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

CREATE TABLE project_tag (
  project_id INTEGER REFERENCES project(id) ON DELETE CASCADE,
  tag_id INTEGER REFERENCES tag(id) ON DELETE CASCADE,
  PRIMARY KEY (project_id, tag_id)
);

CREATE TABLE activity_log (
id SERIAL PRIMARY KEY,
user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
description TEXT NOT NULL,
event_type TEXT NOT NULL,
points INTEGER NOT NULL,
created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE comment (
id SERIAL PRIMARY KEY,
from_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
to_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
text TEXT NOT NULL,
created_at TIMESTAMPTZ DEFAULT NOW(),
votes INTEGER DEFAULT 0
);

CREATE TABLE challenge_match (
id SERIAL PRIMARY KEY,
from_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
to_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
status TEXT NOT NULL DEFAULT 'pendiente',
created_at TIMESTAMPTZ DEFAULT NOW(),
updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_name ON users(name);
CREATE INDEX idx_project_users ON project(user_id);
CREATE INDEX idx_log_users_event ON activity_log(user_id, event_type);
