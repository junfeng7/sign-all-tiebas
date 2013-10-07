-- DROP TABLE IF EXISTS wishes;
CREATE TABLE IF NOT EXISTS tiebas(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    tieba varchar(100) NOT NULL
);

-- DROP TABLE IF EXISTS settings;
CREATE TABLE IF NOT EXISTS settings (
    name varchar(30) NOT NULL PRIMARY KEY,
    value varchar(30) NOT NULL
);

-- DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
    id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email varchar(100) NOT NULL UNIQUE,
    name varchar(100) NOT NULL,
    cookie varchar(2000),
    passwd varchar(100) NOT NULL
);
-- DROP TABLE IF EXISTS wishes_user;
CREATE TABLE IF NOT EXISTS tiebas_users (
    tieba_id INT NOT NULL REFERENCES tiebas(id),
    user_id INT NOT NULL REFERENCES users(id)
);
