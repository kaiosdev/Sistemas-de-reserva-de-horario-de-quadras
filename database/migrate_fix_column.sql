-- ============================================================
-- ATHLETIX — Migração: corrigir coluna id_espacio → id_espaco
-- Execute este script no pgAdmin/DBeaver no banco athletix_db
-- se o banco foi criado com o schema modificado (com erro de digitação).
-- ============================================================

-- 1. Remove a trigger e a FK que referenciam a coluna errada
ALTER TABLE Agendamento DROP CONSTRAINT IF EXISTS agendamento_id_espaco_fkey;
DROP TRIGGER IF EXISTS trg_valida_choque_horario ON Agendamento;

-- 2. Renomeia a coluna (se existir como id_espacio)
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'agendamento' AND column_name = 'id_espacio'
    ) THEN
        ALTER TABLE Agendamento RENAME COLUMN id_espacio TO id_espaco;
        RAISE NOTICE 'Coluna id_espacio renomeada para id_espaco.';
    ELSE
        RAISE NOTICE 'Coluna id_espacio nao encontrada (ja esta como id_espaco?).';
    END IF;
END $$;

-- 3. Recria a FK
ALTER TABLE Agendamento
    ADD CONSTRAINT agendamento_id_espaco_fkey
    FOREIGN KEY (id_espaco) REFERENCES Espaco (id_espaco);

-- 4. Recria a trigger (referencia id_espaco)
CREATE TRIGGER trg_valida_choque_horario
BEFORE INSERT ON Agendamento
FOR EACH ROW
EXECUTE FUNCTION func_valida_choque_horario();

SELECT 'Migracao concluida com sucesso!' AS resultado;
