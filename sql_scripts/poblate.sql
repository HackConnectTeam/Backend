-- Insertar usuarios
INSERT INTO users (name) VALUES
('Alice'),
('Bob'),
('Carol');

INSERT INTO tag (name) VALUES
('Python'),
('JavaScript'),
('SQL'),
('Machine Learning');

INSERT INTO user_tag (user_id, tag_id) VALUES
(1, 1),  -- Alice - Python
(1, 3),  -- Alice - SQL
(2, 2),  -- Bob - JavaScript
(3, 1),  -- Carol - Python
(3, 4);  -- Carol - ML

-- Insertar proyectos
INSERT INTO project (user_id, title, description_raw, description_ai, generated_name)
VALUES
(1, 'Proyecto A', 'Descripción original A', 'Descripción AI A', 'GenA'),
(2, 'Proyecto B', 'Descripción original B', 'Descripción AI B', 'GenB');

INSERT INTO project_tag (project_id, tag_id) VALUES
(1, 1),  -- Proyecto A - Python
(1, 3),  -- Proyecto A - SQL
(2, 2);  -- Proyecto B - JavaScript

-- Insertar logs de actividad
INSERT INTO activity (description, event_type, points) VALUES
('Inicio de sesión', 'login', 5),                   -- ID 1
('Completó un reto', 'challenge_completed', 20),   -- ID 2
('Comentó un proyecto', 'comment', 10);            -- ID 3

-- Insertar comentarios
INSERT INTO comment (from_user_id, to_user_id, text)
VALUES
(1, 2, '¡Buen trabajo!'),
(2, 1, 'Gracias por el comentario'),
(3, 1, 'Interesante proyecto');

-- Insertar desafíos entre usuarios
INSERT INTO challenge_match (from_user_id, to_user_id, activity_id, status) VALUES
(1, 2, 1, 'pendiente'),
(2, 3, 2, 'aceptado'),
(3, 1, 3, 'rechazado');
