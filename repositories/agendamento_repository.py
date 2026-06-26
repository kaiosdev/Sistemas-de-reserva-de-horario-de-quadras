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