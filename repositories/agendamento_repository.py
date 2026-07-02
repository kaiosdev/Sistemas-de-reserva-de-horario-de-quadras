from database.connection import get_connection
from models.agendamento import Agendamento

class AgendamentoRepository:
    def inserir(self, agendamento: Agendamento):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "INSERT INTO Agendamento (data_reserva, hora_inicio, hora_fim, id_cliente, id_espaco) VALUES (%s, %s, %s, %s, %s)"
                valores = (agendamento.data_reserva, agendamento.hora_inicio, agendamento.hora_fim, agendamento.id_cliente, agendamento.id_espaco)
                cursor.execute(sql, valores)
                conexao.commit()
            except Exception as e:
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
                        a.id_agendamento, 
                        a.data_reserva, 
                        a.hora_inicio, 
                        a.hora_fim, 
                        a.id_cliente, 
                        a.id_espaco,
                        c.nome AS nome_cliente,
                        e.nome AS nome_espaco
                    FROM Agendamento a
                    INNER JOIN Cliente c ON a.id_cliente = c.id_cliente
                    INNER JOIN Espaco e ON a.id_espaco = e.id_espaco
                """
                cursor.execute(sql)
                registros = cursor.fetchall()
                for linha in registros:
                    ag = Agendamento(
                        id_agendamento=linha[0], 
                        data_reserva=str(linha[1]), 
                        hora_inicio=str(linha[2]), 
                        hora_fim=str(linha[3]), 
                        id_cliente=linha[4], 
                        id_espaco=linha[5],
                        nome_cliente=linha[6],
                        nome_espaco=linha[7]
                    )
                    agendamentos.append(ag)
            except Exception as e:
                print(f"Erro ao listar agendamentos: {e}")
            finally:
                cursor.close()
                conexao.close()
        return agendamentos

    def atualizar(self, id_agendamento: int, data_reserva: str, hora_inicio: str, hora_fim: str, id_cliente: int, id_espaco: int):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = """UPDATE Agendamento SET data_reserva=%s, hora_inicio=%s, hora_fim=%s, id_cliente=%s, id_espaco=%s 
                         WHERE id_agendamento=%s"""
                cursor.execute(sql, (data_reserva, hora_inicio, hora_fim, id_cliente, id_espaco, id_agendamento))
                conexao.commit()
            except Exception as e:
                raise Exception(f"{e}")
            finally:
                cursor.close()
                conexao.close()

    def excluir(self, id_agendamento: int):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "DELETE FROM Agendamento WHERE id_agendamento = %s"
                cursor.execute(sql, (id_agendamento,))
                conexao.commit()
            finally:
                cursor.close()
                conexao.close()