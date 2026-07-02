from database.connection import get_connection

class PagamentoRepository:
    def inserir(self, id_agendamento: int, valor_total: float, forma: str, status: str, chave_pix: str, final_cartao: str):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = """INSERT INTO Pagamento (id_agendamento, valor_total, forma_pagamento, status, chave_pix, final_cartao) 
                         VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_pagamento"""
                valores = (id_agendamento, valor_total, forma, status, chave_pix or None, final_cartao or None)
                cursor.execute(sql, valores)
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
                # Junção para exibir um histórico completo de pagamentos
                sql = """SELECT p.id_pagamento, p.valor_total, p.forma_pagamento, p.status, p.chave_pix, p.final_cartao,
                                c.nome as cliente, e.nome as espaco
                         FROM Pagamento p
                         JOIN Agendamento a ON p.id_agendamento = a.id_agendamento
                         JOIN Cliente c ON a.id_cliente = c.id_cliente
                         JOIN Espaco e ON a.id_espaco = e.id_espaco
                         ORDER BY p.id_pagamento DESC"""
                cursor.execute(sql)
                for linha in cursor.fetchall():
                    pagamentos.append({
                        "id_pagamento": linha[0], "valor_total": float(linha[1]), "forma_pagamento": linha[2], 
                        "status": linha[3], "chave_pix": linha[4], "final_cartao": linha[5],
                        "cliente": linha[6], "espaco": linha[7]
                    })
            finally:
                cursor.close()
                conexao.close()
        return pagamentos