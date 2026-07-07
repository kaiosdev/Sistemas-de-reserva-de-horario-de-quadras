-- ============================================================
-- ATHLETIX — Reset completo do banco de dados
-- DROPA tudo e recria do zero com o schema.sql correto.
-- Execute no pgAdmin/DBeaver no banco athletix_db.
-- ============================================================

DROP TABLE IF EXISTS Pagamento CASCADE;
DROP TABLE IF EXISTS Agendamento CASCADE;
DROP TABLE IF EXISTS Espaco CASCADE;
DROP TABLE IF EXISTS Cliente CASCADE;
DROP TABLE IF EXISTS Modalidade CASCADE;
DROP FUNCTION IF EXISTS func_valida_choque_horario() CASCADE;

-- Agora execute o schema.sql (ou cole o conteudo dele abaixo)
