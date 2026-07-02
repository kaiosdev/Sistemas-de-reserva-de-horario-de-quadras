CREATE TABLE Cliente (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    endereco VARCHAR(255),
    telefone VARCHAR(15)
);

CREATE TABLE Espaco (
    id_espaco SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    tamanho_quadra VARCHAR(50),
    valor_hora DECIMAL(10, 2) NOT NULL
);

CREATE TABLE Agendamento (
    id_agendamento SERIAL PRIMARY KEY,
    data_reserva DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    id_cliente INT NOT NULL,
    id_espaco INT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES Cliente (id_cliente),
    FOREIGN KEY (id_espaco) REFERENCES Espaco (id_espaco)
);

CREATE TABLE Pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    valor_total DECIMAL(10, 2) NOT NULL,
    forma_pagamento VARCHAR(50) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('Pendente', 'Pago', 'Cancelado')) DEFAULT 'Pendente',
    chave_pix VARCHAR(255),
    final_cartao VARCHAR(4),
    id_agendamento INT UNIQUE NOT NULL,
    FOREIGN KEY (id_agendamento) REFERENCES Agendamento (id_agendamento) ON DELETE CASCADE
);

CREATE OR REPLACE FUNCTION func_valida_choque_horario()
RETURNS TRIGGER AS $$
DECLARE
    conflitos INT;
BEGIN
    SELECT COUNT(*) INTO conflitos
    FROM Agendamento
    WHERE id_espaco = NEW.id_espaco
      AND data_reserva = NEW.data_reserva
      AND (
          (NEW.hora_inicio >= hora_inicio AND NEW.hora_inicio < hora_fim) OR
          (NEW.hora_fim > hora_inicio AND NEW.hora_fim <= hora_fim) OR
          (NEW.hora_inicio <= hora_inicio AND NEW.hora_fim >= hora_fim)
      );

    IF conflitos > 0 THEN
        RAISE EXCEPTION 'Erro: O espaco ja possui reserva neste horario!';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_valida_choque_horario
BEFORE INSERT ON Agendamento
FOR EACH ROW
EXECUTE FUNCTION func_valida_choque_horario();