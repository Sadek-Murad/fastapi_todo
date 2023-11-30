CREATE DATABASE IF NOT EXISTS todo;

CREATE USER IF NOT EXISTS 'todo'@'localhost' IDENTIFIED BY '1234';

GRANT ALL PRIVILEGES ON todo.* TO 'todo'@'localhost';

FLUSH PRIVILEGES;

USE todo;


CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL DEFAULT 'open'
    );
           