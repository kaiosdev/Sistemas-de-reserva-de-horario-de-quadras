CREATE DATABASE IF NOT EXISTS athletix_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE athletix_db;

CREATE TABLE Modalidade (
    id_modalidade INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);