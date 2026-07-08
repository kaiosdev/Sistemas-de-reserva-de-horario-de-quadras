from database.connection import get_connection
from models.agendamento import Agendamento

class AgendamentoRepository:
    def inserir(self, agendamento: Agendamento, ids_espacos: list):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql_ag = "INSERT INTO Agendamento (data_reserva, hora_inicio, hora_fim, id_cliente) VALUES (%s, %s, %s, %s) RETURNING id_agendamento"
                cursor.execute(sql_ag, (agendamento.data_reserva, agendamento.hora_inicio, agendamento.hora_fim, agendamento.id_cliente))
                id_gerado = cursor.fetchone()[0]
                
                for id_e in ids_espacos:
                    cursor.execute("INSERT INTO Agendamento_Espaco (id_agendamento, id_espaco) VALUES (%s, %s)", (id_gerado, id_e))
                
                conexao.commit()
            except Exception as e:
                conexao.rollback()
                raise Exception(f"{e}")
            finally:
                cursor.close()
                conexao.close()

    def listar_todos(self):
        conexao = get_connection()
        agendamentos = []
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = """
                    SELECT 
                        a.id_agendamento, a.data_reserva, a.hora_inicio, a.hora_fim, a.id_cliente,
                        c.nome AS nome_cliente,
                        STRING_AGG(e.nome, ', ') AS espacos_str,
                        SUM(e.valor_hora) AS valor_total
                    FROM Agendamento a
                    INNER JOIN Cliente c ON a.id_cliente = c.id_cliente
                    INNER JOIN Agendamento_Espaco ae ON a.id_agendamento = ae.id_agendamento
                    INNER JOIN Espaco e ON ae.id_espaco = e.id_espaco
                    GROUP BY a.id_agendamento, a.data_reserva, a.hora_inicio, a.hora_fim, a.id_cliente, c.nome
                """
                cursor.execute(sql)
                for linha in cursor.fetchall():
                    agendamentos.append(Agendamento(linha[0], str(linha[1]), str(linha[2]), str(linha[3]), linha[4], linha[5], linha[6], float(linha[7])))
            finally:
                cursor.close()
                conexao.close()
        return agendamentos
    
    def atualizar(self, id_agendamento: int, data_reserva: str, hora_inicio: str, hora_fim: str, id_cliente: int, ids_espacos: list):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql_ag = """UPDATE Agendamento SET data_reserva=%s, hora_inicio=%s, hora_fim=%s, id_cliente=%s 
                            WHERE id_agendamento=%s"""
                cursor.execute(sql_ag, (data_reserva, hora_inicio, hora_fim, id_cliente, id_agendamento))
                
                cursor.execute("DELETE FROM Agendamento_Espaco WHERE id_agendamento = %s", (id_agendamento,))
                
                for id_e in ids_espacos:
                    cursor.execute("INSERT INTO Agendamento_Espaco (id_agendamento, id_espaco) VALUES (%s, %s)", (id_agendamento, id_e))
                
                conexao.commit()
            except Exception as e:
                conexao.rollback()
                raise Exception(f"{e}")
            finally:
                cursor.close()
                conexao.close()

    def excluir(self, id_agendamento: int):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM Agendamento WHERE id_agendamento = %s", (id_agendamento,))
                conexao.commit()
            finally:
                cursor.close()
                conexao.close()