/*Useful queries used with database.py*/

/*CREATE TABLE Users (
    ID SERIAL PRIMARY KEY,
    Name varchar(100) NOT NULL,
    Surname varchar(100) NOT NULL,
    Password varchar(60) NOT NULL,
    Email varchar(30) NOT NULL,
    Tel varchar(20) NOT NULL,
    Role varchar(20) NOT NULL
    Confirmed BOOLEAN NOT NULL DEFAULT FALSE
);*/

/*CREATE TABLE Confirmations (
    ID SERIAL PRIMARY KEY,
    Email varchar(30) NOT NULL,
    Code varchar(100) NOT NULL,
    Creation TIMESTAMP NOT NULL
);*/

SELECT * FROM Confirmations;
