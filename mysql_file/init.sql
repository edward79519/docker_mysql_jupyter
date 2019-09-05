CREATE DATABASE IF NOT EXISTS iii_project CHARACTER SET utf8 COLLATE utf8_general_ci;
USE iii_project;
CREATE TABLE eur_usd_4hr(
    DateTime   DATETIME      PRIMARY KEY,
    Open   DECIMAL(10,5) NOT NULL,
    High   DECIMAL(10,5) NOT NULL,
    Low    DECIMAL(10,5) NOT NULL,
    Close  DECIMAL(10,5) NOT NULL);
