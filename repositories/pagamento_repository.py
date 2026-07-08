from database.connection import get_connection

class PagamentoRepository:
    def inserir(self, id_agendamento: int, valor_total: float, forma: str, status: str, chave_pix: str, final_cartao: str):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = """INSERT INTO Pagamento (id_agendamento, valor_total, forma_pagamento, status, chave_pix, final_cartao) 
                         VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_pagamento"""
                cursor.execute(sql, (id_agendamento, valor_total, forma, status, chave_pix or None, final_cartao or None))
                id_gerado = cursor.fetchone()[0]
                conexao.commit()
                return id_gerado
            finally:
                cursor.close()
                conexao.close()

    def listar_todos(self):
        conexao = get_connection()
        pagamentos = []
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = """
                    SELECT 
                        p.id_pagamento, p.valor_total, p.forma_pagamento, p.status, p.chave_pix, p.final_cartao, p.id_agendamento,
                        c.nome as cliente,
                        STRING_AGG(e.nome, ', ') as espacos
                    FROM Pagamento p
                    JOIN Agendamento a ON p.id_agendamento = a.id_agendamento
                    JOIN Cliente c ON a.id_cliente = c.id_cliente
                    JOIN Agendamento_Espaco ae ON a.id_agendamento = ae.id_agendamento
                    JOIN Espaco e ON ae.id_espaco = e.id_espaco
                    GROUP BY p.id_pagamento, p.valor_total, p.forma_pagamento, p.status, p.chave_pix, p.final_cartao, p.id_agendamento, c.nome
                    ORDER BY p.id_pagamento DESC
                """
                cursor.execute(sql)
                for l in cursor.fetchall():
                    pagamentos.append({
                        "id_pagamento": l[0], "valor_total": float(l[1]), "forma_pagamento": l[2], 
                        "status": l[3], "chave_pix": str(l[4]), "final_cartao": str(l[5]), "id_agendamento": l[6],
                        "cliente": l[7], "espaco": l[8]
                    })
            except Exception as e:
                print(f"Erro SQL no Pagamento: {e}")
            finally:
                cursor.close()
                conexao.close()
        return pagamentos

    def atualizar(self, id_pagamento: int, valor_total: float, forma: str, status: str, chave_pix: str, final_cartao: str):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = """UPDATE Pagamento SET valor_total=%s, forma_pagamento=%s, status=%s, chave_pix=%s, final_cartao=%s 
                         WHERE id_pagamento=%s"""
                cursor.execute(sql, (valor_total, forma, status, chave_pix or None, final_cartao or None, id_pagamento))
                conexao.commit()
            finally:
                cursor.close()
                conexao.close()

    def excluir(self, id_pagamento: int):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "DELETE FROM Pagamento WHERE id_pagamento = %s"
                cursor.execute(sql, (id_pagamento,))
                conexao.commit()
            finally:
                cursor.close()
                conexao.close()