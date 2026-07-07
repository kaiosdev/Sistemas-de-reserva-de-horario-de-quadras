from database.connection import get_connection


class PagamentoRepository:
    """Persistencia da tabela Pagamento.

    Observacao: o modelo de dominio (models/pagamento.py) usa heranca/abstracao
    para PIX e Cartao (polimorfismo). No banco, porem, existe uma unica tabela
    'Pagamento' com coluna 'forma_pagamento'. Este repository opera sobre essa
    tabela generica e devolve dicts simples para a camada de apresentacao.
    """

    def listar_todos(self):
        conexao = get_connection()
        pagamentos = []
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = """
                    SELECT p.id_pagamento, p.valor_total, p.forma_pagamento,
                           p.status, p.id_agendamento,
                           c.nome AS cliente, e.nome AS espaco,
                           a.data_reserva, a.hora_inicio
                    FROM Pagamento p
                    JOIN Agendamento a ON p.id_agendamento = a.id_agendamento
                    JOIN Cliente c ON a.id_cliente = c.id_cliente
                    JOIN Espaco e ON a.id_espaco = e.id_espaco
                    ORDER BY p.id_pagamento DESC
                """
                cursor.execute(sql)
                for linha in cursor.fetchall():
                    pagamentos.append({
                        "id_pagamento": linha[0],
                        "valor_total": float(linha[1]),
                        "forma_pagamento": linha[2],
                        "status": linha[3],
                        "id_agendamento": linha[4],
                        "cliente": linha[5],
                        "espaco": linha[6],
                        "data_reserva": linha[7].isoformat() if linha[7] else None,
                        "hora_inicio": linha[8].strftime("%H:%M") if linha[8] else None,
                    })
            finally:
                cursor.close()
                conexao.close()
        return pagamentos

    def inserir(self, valor_total: float, forma_pagamento: str, id_agendamento: int, status: str = "Pago"):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = """
                    INSERT INTO Pagamento (valor_total, forma_pagamento, status, id_agendamento)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_pagamento
                """
                cursor.execute(sql, (valor_total, forma_pagamento, status, id_agendamento))
                id_pagamento = cursor.fetchone()[0]
                conexao.commit()
                return id_pagamento
            finally:
                cursor.close()
                conexao.close()
        return None

    def atualizar_status(self, id_pagamento: int, novo_status: str):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(
                    "UPDATE Pagamento SET status = %s WHERE id_pagamento = %s",
                    (novo_status, id_pagamento),
                )
                conexao.commit()
            finally:
                cursor.close()
                conexao.close()

    def atualizar(self, id_pagamento: int, valor_total: float, forma_pagamento: str, status: str):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(
                    "UPDATE Pagamento SET valor_total = %s, forma_pagamento = %s, status = %s WHERE id_pagamento = %s",
                    (valor_total, forma_pagamento, status, id_pagamento),
                )
                conexao.commit()
                return cursor.rowcount > 0
            finally:
                cursor.close()
                conexao.close()
        return False

    def deletar(self, id_pagamento: int):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM Pagamento WHERE id_pagamento = %s", (id_pagamento,))
                conexao.commit()
                return cursor.rowcount > 0
            finally:
                cursor.close()
                conexao.close()
        return False
