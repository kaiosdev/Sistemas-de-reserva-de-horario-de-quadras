from database.connection import get_connection
from models.agendamento import Agendamento


class AgendamentoRepository:
    def inserir(self, agendamento: Agendamento):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "INSERT INTO Agendamento (data_reserva, hora_inicio, hora_fim, id_cliente, id_espaco) VALUES (%s, %s, %s, %s, %s) RETURNING id_agendamento"
                valores = (agendamento.data_reserva, agendamento.hora_inicio, agendamento.hora_fim, agendamento.id_cliente, agendamento.id_espaco)
                cursor.execute(sql, valores)
                novo_id = cursor.fetchone()[0]
                conexao.commit()
                return novo_id
            except Exception as e:
                raise Exception(f"{e}")
            finally:
                cursor.close()
                conexao.close()
        return None

    def listar_todos(self):
        """Lista agendamentos com dados de cliente e espaco (JOIN).

        Devolve uma lista de dicionarios prontos para serializacao JSON.
        """
        conexao = get_connection()
        agendamentos = []
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = """
                    SELECT a.id_agendamento, a.data_reserva, a.hora_inicio, a.hora_fim,
                           a.id_cliente, c.nome AS cliente, c.cpf,
                           a.id_espaco, e.nome AS espaco, e.valor_hora
                    FROM Agendamento a
                    JOIN Cliente c ON a.id_cliente = c.id_cliente
                    JOIN Espaco e ON a.id_espaco = e.id_espaco
                    ORDER BY a.data_reserva DESC, a.hora_inicio ASC
                """
                cursor.execute(sql)
                for linha in cursor.fetchall():
                    agendamentos.append({
                        "id_agendamento": linha[0],
                        "data_reserva": linha[1].isoformat() if linha[1] else None,
                        "hora_inicio": linha[2].strftime("%H:%M") if linha[2] else None,
                        "hora_fim": linha[3].strftime("%H:%M") if linha[3] else None,
                        "id_cliente": linha[4],
                        "cliente": linha[5],
                        "cpf": linha[6],
                        "id_espaco": linha[7],
                        "espaco": linha[8],
                        "valor_hora": float(linha[9]),
                    })
            finally:
                cursor.close()
                conexao.close()
        return agendamentos

    def buscar_por_id(self, id_agendamento: int):
        """Retorna um dict com o agendamento + dados de cliente/espaco, ou None."""
        conexao = get_connection()
        if not conexao:
            return None
        try:
            cursor = conexao.cursor()
            sql = """
                SELECT a.id_agendamento, a.data_reserva, a.hora_inicio, a.hora_fim,
                       a.id_cliente, c.nome AS cliente,
                       a.id_espaco, e.nome AS espaco, e.valor_hora
                FROM Agendamento a
                JOIN Cliente c ON a.id_cliente = c.id_cliente
                JOIN Espaco e ON a.id_espaco = e.id_espaco
                WHERE a.id_agendamento = %s
            """
            cursor.execute(sql, (id_agendamento,))
            linha = cursor.fetchone()
            if not linha:
                return None
            return {
                "id_agendamento": linha[0],
                "data_reserva": linha[1].isoformat() if linha[1] else None,
                "hora_inicio": linha[2].strftime("%H:%M") if linha[2] else None,
                "hora_fim": linha[3].strftime("%H:%M") if linha[3] else None,
                "id_cliente": linha[4],
                "cliente": linha[5],
                "id_espaco": linha[6],
                "espaco": linha[7],
                "valor_hora": float(linha[8]),
            }
        finally:
            cursor.close()
            conexao.close()

    def atualizar(self, id_agendamento: int, data_reserva: str, hora_inicio: str, hora_fim: str, id_cliente: int, id_espaco: int):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(
                    "UPDATE Agendamento SET data_reserva = %s, hora_inicio = %s, hora_fim = %s, id_cliente = %s, id_espaco = %s WHERE id_agendamento = %s",
                    (data_reserva, hora_inicio, hora_fim, id_cliente, id_espaco, id_agendamento),
                )
                conexao.commit()
                return cursor.rowcount > 0
            finally:
                cursor.close()
                conexao.close()
        return False

    def deletar(self, id_agendamento: int):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM Agendamento WHERE id_agendamento = %s", (id_agendamento,))
                conexao.commit()
                return cursor.rowcount > 0
            finally:
                cursor.close()
                conexao.close()
        return False