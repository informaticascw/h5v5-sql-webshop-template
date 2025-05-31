-- source: https://chatgpt.com/share/67f1905a-73b0-8012-ae39-f105fcf0efc4
-- create database from command line:
-- bash start.sh


-- Create categories table
DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- Create products table
DROP TABLE IF EXISTS products;
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    image_link TEXT,
    category_id INTEGER,
    price REAL,
    FOREIGN KEY(category_id) REFERENCES category(id)
);

-- Create colors table
DROP TABLE IF EXISTS colors;
CREATE TABLE colors (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- Create join table for N:M relationship
DROP TABLE IF EXISTS product_colors;
CREATE TABLE product_colors (
    product_id INTEGER,
    color_id INTEGER,
    FOREIGN KEY(product_id) REFERENCES products(id),
    FOREIGN KEY(color_id) REFERENCES colors(id)
);

-- Add category
INSERT INTO categories (id, name) VALUES
    (1, 'Poppetje'),
    (2, 'Huisje');

-- Add products
INSERT INTO products (id, name, image_link, category_id, price) VALUES
    (1, 'Muzieksmurf', 'muzieksmurf.png', 1, 29.99),
    (2, 'Knutselsmurf', 'knutselsmurf.png', 1, 14.95),
    (3, 'Smurfin', 'smurfin.png', 1, 9.50),
    (4, 'Grote smurf', 'grotesmurf.png', 1, 10.50),
    (5, 'Klein huis', 'huis.png', 2, 15.50),
    (6, 'Paars huis', 'paarshuis.png', 2, 15.50),
    (7, 'Groot huis', 'hooghuis.png', 2, 15.50);

-- Add colors
INSERT INTO colors (id, name) VALUES
    (1, 'Blauw'),
    (2, 'Wit'),
    (3, 'Donkerblauw'),
    (4, 'Geel'),
    (5, 'Goud'),
    (6, 'Bruin'),
    (7, 'Rood'),
    (8, 'Paars');

-- Link products to colors
INSERT INTO product_colors (product_id, color_id) VALUES
    (1, 1), (1, 2), (1, 5),
    (2, 1), (2, 2), (2, 3), (2, 6),
    (3, 4), (3, 1), (3, 2),
    (4, 7), (4, 1), (4, 2),
    (5, 6), (5, 7), (5, 2),
    (6, 8), (6, 7), (6, 2),
    (7, 6), (7, 7);    