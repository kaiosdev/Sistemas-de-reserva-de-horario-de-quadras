from database.connection import get_connection
from models.espaco import Espaco

class EspacoRepository:
    def inserir(self, espaco: Espaco):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "INSERT INTO Espaco (nome, descricao, tamanho_quadra, valor_hora, id_modalidade) VALUES (%s, %s, %s, %s, 1)"
                valores = (espaco.nome, espaco.descricao, espaco.tamanho_quadra, espaco.valor_hora)
                cursor.execute(sql, valores)
                conexao.commit()
            finally:
                cursor.close()
                conexao.close()

    def listar_todos(self):
        conexao = get_connection()
        espacos = []
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "SELECT id_espaco, nome, descricao, tamanho_quadra, valor_hora FROM Espaco"
                cursor.execute(sql)
                for linha in cursor.fetchall():
                    espacos.append(Espaco(linha[0], linha[1], linha[2], linha[3], float(linha[4])))
            finally:
                cursor.close()
                conexao.close()
        return espacos