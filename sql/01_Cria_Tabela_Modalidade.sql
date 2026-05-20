-- Cria o banco de dados e define o uso dele
CREATE DATABASE IF NOT EXISTS athletix_db;
USE athletix_db;

-- Cria a tabela base de Modalidades
CREATE TABLE Modalidade (
    id_modalidade INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);