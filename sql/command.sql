USE users;
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT primary_key PRIMARY KEY (id),
    CONSTRAINT unique_key UNIQUE KEY (email)
)

CREATE USER 'access_viewer'@'%' IDENTIFIED BY 'Viewer@123';
GRANT SELECT ON users.* TO 'access_viewer'@'localhost';

CREATE USER 'access_write'@'%' IDENTIFIED BY 'Writer@123';
GRANT INSERT ON users.* TO 'access_write'@'%';

INSERT INTO users (first_name, last_name, email)
VALUES ("Angelo", "Fidelis", "angelo@gmail.com"),
       ("Caio", "Silva", "caio@gmail.com"),
       ("Pedro", "Henrique", "pedro@gmail.com");