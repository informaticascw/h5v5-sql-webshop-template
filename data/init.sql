-- source based on: https://chatgpt.com/share/67f1905a-73b0-8012-ae39-f105fcf0efc4
-- create database from command line:
-- bash start.sh

--
-- create tables
--

-- Create products table
DROP TABLE IF EXISTS products;
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    image_link TEXT
);

--
-- populate tables with data
--

-- Add products
INSERT INTO products (id, name, image_link) VALUES
    (1, 'Smurfin', 'smurfin.png'),
    (2, 'Muzieksmurf', 'muzieksmurf.png'),
    (3, 'Grote smurf', 'grotesmurf.png');
