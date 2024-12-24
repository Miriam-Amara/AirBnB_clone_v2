-- A script that prepares a MySQL server for AirBnB_clone project:

-- A database hbnb_dev_db
-- A new user hbnb_dev (in localhost)
-- The password of hbnb_dev should be set to hbnb_dev_pwd
-- hbnb_dev should have all privileges on the database hbnb_dev_db (and only this database)
-- hbnb_dev should have SELECT privilege on the database performance_schema (and only this database)
-- If the database hbnb_dev_db or the user hbnb_dev already exists, your script should not fail


-- create database 'hbnb_dev_db'
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- create new user
CREATE user IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- grant privileges to the new user
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
