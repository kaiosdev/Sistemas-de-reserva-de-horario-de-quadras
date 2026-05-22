USE athletix_db;

DELIMITER //

-- Cria a trigger para validação de conflito e choque de hráros
CREATE TRIGGER tg_valida_choque_horario
BEFORE INSERT ON Agendamento
FOR EACH ROW
BEGIN
    DECLARE conflitos INT;

    -- Verifica se já existe um agendamento no mesmo espaço que cruza com o novo horário
    SELECT COUNT(*) INTO conflitos
    FROM Agendamento
    WHERE id_espaco = NEW.id_espaco
      AND (NEW.data_hora_inicio < data_hora_fim AND NEW.data_hora_fim > data_hora_inicio);

    -- Bloqueia a inserção se houver sobreposição
    IF conflitos > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro de Regra de Negócio: Choque de horários detectado para o espaço selecionado.';
    END IF;
END;
//

DELIMITER ;
