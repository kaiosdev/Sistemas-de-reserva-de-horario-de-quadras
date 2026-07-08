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

CREATE TABLE Modalidade (
    id_modalidade SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT
);

CREATE TABLE Agendamento (
    id_agendamento SERIAL PRIMARY KEY,
    data_reserva DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    id_cliente INT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES Cliente (id_cliente)
);

CREATE TABLE Agendamento_Espaco (
    id_agendamento INT NOT NULL,
    id_espaco INT NOT NULL,
    PRIMARY KEY (id_agendamento, id_espaco),
    FOREIGN KEY (id_agendamento) REFERENCES Agendamento (id_agendamento) ON DELETE CASCADE,
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
    v_data DATE;
    v_ini TIME;
    v_fim TIME;
BEGIN
    SELECT data_reserva, hora_inicio, hora_fim INTO v_data, v_ini, v_fim
    FROM Agendamento WHERE id_agendamento = NEW.id_agendamento;

    SELECT COUNT(*) INTO conflitos
    FROM Agendamento_Espaco ae
    JOIN Agendamento a ON ae.id_agendamento = a.id_agendamento
    WHERE ae.id_espaco = NEW.id_espaco
      AND a.data_reserva = v_data
      AND a.id_agendamento != NEW.id_agendamento
      AND (
          (v_ini >= a.hora_inicio AND v_ini < a.hora_fim) OR
          (v_fim > a.hora_inicio AND v_fim <= a.hora_fim) OR
          (v_ini <= a.hora_inicio AND v_fim >= a.hora_fim)
      );

    IF conflitos > 0 THEN
        RAISE EXCEPTION 'Choque de horário! Um dos espaços já está ocupado neste período.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_valida_choque_horario
BEFORE INSERT ON Agendamento_Espaco
FOR EACH ROW EXECUTE FUNCTION func_valida_choque_horario();