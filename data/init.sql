-- source based on: https://chatgpt.com/share/67f1905a-73b0-8012-ae39-f105fcf0efc4
-- create database from command line:
-- bash start.sh


-- BETTER ERROR CHECKING
-- next line enables checking of values for keys
PRAGMA foreign_keys = ON; 
-- STRICT is added to each table for better error checking

--
-- CREATE TABLES
--

-- Create products table
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    image_link TEXT
);

--
-- POPULATE TABLES WITH DATA
--

-- Add products
INSERT INTO products (id, name, image_link) VALUES
    (1, 'Smurfin', 'smurfin.png'),
    (2, 'Muzieksmurf', 'muzieksmurf.png'),
    (3, 'Grote smurf', 'grotesmurf.png');
