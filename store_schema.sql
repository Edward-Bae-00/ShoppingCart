PRAGMA foreign_keys=off;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  username        varchar(50) not null PRIMARY KEY,
  password        varchar(50) not null,
  fname           varchar(50) not null,
  lname           varchar(50) not null
);

DROP TABLE IF EXISTS items;
CREATE TABLE items (
  id          int(8) not null PRIMARY KEY,
  name        varchar(50) not null,
  image       varchar(50) not null,
  price       double(8) not null,
  type        varchar(50) not null,
  inventory   int(8) not null
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
  order_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  username    varchar(50) not null,
  total_price double(8) not null,
  order_date  DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);

DROP TABLE IF EXISTS order_items;
CREATE TABLE order_items (
  order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id      INTEGER not null,
  item_id       INTEGER not null,
  quantity      int(8) not null,
  price         double(8) not null,      
  FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
  FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
);


PRAGMA foreign_keys=on;


INSERT INTO users VALUES ('edward', 'pass', 'Edward', 'Bae');
INSERT INTO users VALUES ('testuser', 'testpass', 'test', 'user');


INSERT INTO items VALUES (1,'Alphafly', 'alphafly.png', 300.00, 'Carbon', 100);
INSERT INTO items VALUES (2,'Vaporfly', 'vaporflyv3.webp', 250.00, 'Carbon', 1);
INSERT INTO items VALUES (3,'Vaporfly V3', 'streakfly.webp', 280.00, 'Carbon', 3);
INSERT INTO items VALUES (4,'Streakfly', 'vaporfly.webp',200.00, 'Carbon', 100);
INSERT INTO items VALUES (5,'MetaSpeed SkyParis', 'metaspeedskyparis.png', 300.00, 'Carbon', 100);
INSERT INTO items VALUES (6,'FuelCell Rebel', 'FuelcellRebel.png', 200.00, 'Carbon', 100);
INSERT INTO items VALUES (7,'SuperBlast', 'superblast.png', 180.00, 'Mileage', 100);
INSERT INTO items VALUES (8,'1080v14', '1080v14.png', 100.00, 'Mileage', 100);
INSERT INTO items VALUES (9,'Invincibles', 'invincible.png', 180.00, 'Mileage', 100);
INSERT INTO items VALUES (10,'Maxfly', 'maxfly.webp', 150.00, 'Spikes', 100);
INSERT INTO items VALUES (11,'Dragonfly','dragonfly.webp', 200.00, 'Spikes', 100);
INSERT INTO items VALUES (12,'Rivalfly', 'rivalfly.webp', 170.00, 'Spikes', 100);