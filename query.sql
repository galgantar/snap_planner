/*Useful queries used with database.py*/

/*CREATE TABLE Users (
    ID SERIAL PRIMARY KEY,
    Name varchar(100) NOT NULL,
    Surname varchar(100) NOT NULL,
    Password varchar(60) NOT NULL,
    Email varchar(30) NOT NULL,
    Tel varchar(20) NOT NULL,
    Role varchar(20) NOT NULL,
    Confirmed BOOLEAN NOT NULL DEFAULT FALSE <-- default value because of later addition of a column
);*/

/*CREATE TABLE Confirmations (
    ID SERIAL PRIMARY KEY,
    Email varchar(30) NOT NULL,
    Code varchar(100) NOT NULL,
    Creation TIMESTAMP NOT NULL,
    Type varchar(15) NOT NULL DEFAULT 'email', <-- default value because of later addition of a column
    Active BOOLEAN NOT NULL DEFAULT FALSE  <-- default value because of later addition of a column
);*/

/*CREATE TABLE Dates (
  ID SERIAL PRIMARY KEY,
  Email varchar(30) NOT NULL,
  MainDate TIMESTAMP NOT NULL,
  Parent varchar(30) NOT NULL,
  Active BOOLEAN NOT NULL DEFAULT FALSE <-- default value because of later addition of a column
);*/

/*CREATE TABLE Tables (
  ID SERIAL PRIMARY KEY,
  Name varchar(30) NOT NULL,
  Creator varchar(30) NOT NULL,
  CreationDate TIMESTAMP NOT NULL,
  Days varchar(5) NOT NULL
);*/

--SELECT * FROM USERS;
