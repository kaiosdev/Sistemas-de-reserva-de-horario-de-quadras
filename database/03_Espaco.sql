USE athletix_db;

CREATE TABLE Espaco (
    id_espaco INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    valor_hora DECIMAL(10, 2) NOT NULL,
    id_modalidade INT NOT NULL,
    FOREIGN KEY (id_modalidade) REFERENCES Modalidade(id_modalidade)
);