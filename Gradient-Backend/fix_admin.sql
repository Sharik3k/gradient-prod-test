-- Додати колонку role якщо її немає
ALTER TABLE users ADD COLUMN IF NOT EXISTS role TEXT NOT NULL DEFAULT 'manager';

-- Перевірити що admin має правильну роль
UPDATE users SET role = 'admin' WHERE username = 'admin';

-- Видалити дублікат admin@example.com (рядок 3)
DELETE FROM users WHERE id = 5;

-- Перевірити результат
SELECT id, username, email, role FROM users;
