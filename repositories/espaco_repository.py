from database.connection import get_connection
from models.espaco import Espaco

class EspacoRepository:
    def inserir(self, espaco: Espaco):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = """INSERT INTO Espaco (nome, descricao, tamanho_quadra, valor_hora, id_modalidade) 
                         VALUES (%s, %s, %s, %s, %s) RETURNING id_espaco"""
                valores = (espaco.nome, espaco.descricao, espaco.tamanho_quadra, espaco.valor_hora, espaco.id_modalidade)
                cursor.execute(sql, valores)
                id_gerado = cursor.fetchone()[0]
                espaco.id_espaco = id_gerado
                conexao.commit()
                return id_gerado
            finally:
                cursor.close()
                conexao.close()

    def listar_todos(self):
        conexao = get_connection()
        espacos = []
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = """SELECT e.id_espaco, e.nome, e.descricao, e.tamanho_quadra, e.valor_hora, e.id_modalidade, m.nome 
                         FROM Espaco e
                         INNER JOIN Modalidade m ON e.id_modalidade = m.id_modalidade
                         ORDER BY e.id_espaco"""
                cursor.execute(sql)
                for linha in cursor.fetchall():
                    espacos.append(Espaco(linha[0], linha[1], linha[2], linha[3], float(linha[4]), linha[5], linha[6]))
            finally:
                cursor.close()
                conexao.close()
        return espacos

    def atualizar(self, id_espaco: int, nome: str, descricao: str, tamanho_quadra: str, valor_hora: float, id_modalidade: int):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = """UPDATE Espaco SET nome=%s, descricao=%s, tamanho_quadra=%s, valor_hora=%s, id_modalidade=%s 
                         WHERE id_espaco=%s"""
                cursor.execute(sql, (nome, descricao, tamanho_quadra, valor_hora, id_modalidade, id_espaco))
                conexao.commit()
            finally:
                cursor.close()
                conexao.close()

    def excluir(self, id_espaco: int):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "DELETE FROM Espaco WHERE id_espaco = %s"
                cursor.execute(sql, (id_espaco,))
                conexao.commit()
            finally:
                cursor.close()
                conexao.close()