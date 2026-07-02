from database.connection import get_connection
from models.espaco import Espaco

class EspacoRepository:
    def inserir(self, espaco: Espaco):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                # Removido id_modalidade para refletir o MER original
                sql = "INSERT INTO Espaco (nome, descricao, tamanho_quadra, valor_hora) VALUES (%s, %s, %s, %s) RETURNING id_espaco"
                valores = (espaco.nome, espaco.descricao, espaco.tamanho_quadra, espaco.valor_hora)
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
                # Removido id_modalidade do SELECT
                sql = "SELECT id_espaco, nome, descricao, tamanho_quadra, valor_hora FROM Espaco ORDER BY id_espaco"
                cursor.execute(sql)
                for linha in cursor.fetchall():
                    # Instanciando o objeto Espaco apenas com os 5 atributos reais
                    espacos.append(Espaco(linha[0], linha[1], linha[2], linha[3], float(linha[4])))
            finally:
                cursor.close()
                conexao.close()
        return espacos

    def excluir(self, id_espaco: int):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM Espaco WHERE id_espaco = %s", (id_espaco,))
                conexao.commit()
            finally:
                cursor.close()
                conexao.close()