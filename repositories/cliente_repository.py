from database.connection import get_connection
from models.cliente import Cliente

class ClienteRepository:
    def inserir(self, cliente: Cliente):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "INSERT INTO Cliente (nome, cpf, endereco, telefone) VALUES (%s, %s, %s, %s)"
                valores = (cliente.nome, cliente.cpf, cliente.endereco, cliente.telefone)
                cursor.execute(sql, valores)
                conexao.commit()
            finally:
                cursor.close()
                conexao.close()

    def listar_todos(self):
        conexao = get_connection()
        clientes = []
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "SELECT id_cliente, nome, cpf, endereco, telefone FROM Cliente"
                cursor.execute(sql)
                for linha in cursor.fetchall():
                    clientes.append(Cliente(linha[0], linha[1], linha[2], linha[3], linha[4]))
            finally:
                cursor.close()
                conexao.close()
        return clientes
    
    def atualizar(self, id_cliente: int, nome: str, cpf: str, endereco: str, telefone: str):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "UPDATE Cliente SET nome=%s, cpf=%s, endereco=%s, telefone=%s WHERE id_cliente=%s"
                cursor.execute(sql, (nome, cpf, endereco, telefone, id_cliente))
                conexao.commit()
            finally:
                cursor.close()
                conexao.close()

    def excluir(self, id_cliente: int):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "DELETE FROM Cliente WHERE id_cliente = %s"
                cursor.execute(sql, (id_cliente,))
                conexao.commit()
            finally:
                cursor.close()
                conexao.close()