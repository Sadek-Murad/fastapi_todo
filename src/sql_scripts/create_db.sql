CREATE DATABASE IF NOT EXISTS todo;

CREATE USER IF NOT EXISTS 'todo'@'localhost' IDENTIFIED BY '1234';

GRANT ALL PRIVILEGES ON todo.* TO 'todo'@'localhost';

FLUSH PRIVILEGES;




CREATE DATABASE IF NOT EXISTS todo;

USE todo;


CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    status ENUM('open', 'in progress', 'finished') NOT NULL DEFAULT 'open');
           