CREATE TABLE IF NOT EXISTS coordinates(
  id INT,
  x INT,
  y INT,
  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Model(
  id int AUTO_INCREMENT,
  PRICE INT unsigned,
  Class TEXT,
  Type_Of_Socket TEXT,
  MAX_Charge INT UNSIGNED,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Cars(
  VIN INT,
  mid INT,
  COLOR TEXT,
  CID INT AUTO_INCREMENT,
  Is_available BIT default 1,
  Remaining INT unsigned default 100,
  coord_id INT NOT NULL,
  Wear_of_the_car INT unsigned default 100,
  PRIMARY KEY (CID),
  FOREIGN KEY (mid) REFERENCES Model(id),
  FOREIGN KEY(coord_id) REFERENCES coordinates(id)
);

CREATE TABLE IF NOT EXISTS providers(
  Name varchar(256) ,
  Type_of_car_parts TEXT,
  Phone INT UNSIGNED,
  PRIMARY KEY (Name)
);

CREATE TABLE IF NOT EXISTS car_part(
  Name text,
  id INT,
  primary key(id)
);

CREATE TABLE IF NOT EXISTS Available_Parts(
  Part_id INT,
  id INT,
  PRIMARY KEY (id)
);

-- workshop (parts,timing,wid)
CREATE TABLE IF NOT EXISTS workshop(
  wid INT,
  available_parts_id INT,
  timing TEXT,
  PRIMARY KEY (wid)
);