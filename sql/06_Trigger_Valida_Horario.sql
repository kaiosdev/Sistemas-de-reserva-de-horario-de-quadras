USE athletix_db;

DELIMITER $$

CREATE TRIGGER trg_valida_choque_horario
BEFORE INSERT ON Agendamento
FOR EACH ROW
BEGIN
    DECLARE conflitos INT;

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
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: A quadra ja possui reserva neste horario!';
    END IF;

END$$

DELIMITER ;