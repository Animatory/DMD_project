CREATE DATABASE company;
CREATE USER 'manager'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON company.* TO 'manager'@'localhost';