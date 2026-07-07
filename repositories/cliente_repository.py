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
                sql = "SELECT id_cliente, nome, cpf, endereco, telefone FROM Cliente ORDER BY id_cliente"
                cursor.execute(sql)
                for linha in cursor.fetchall():
                    clientes.append(Cliente(linha[0], linha[1], linha[2], linha[3], linha[4]))
            finally:
                cursor.close()
                conexao.close()
        return clientes

    def buscar_por_cpf(self, cpf: str):
        """Busca exata por CPF (critério único)."""
        conexao = get_connection()
        if not conexao:
            return None
        try:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id_cliente, nome, cpf, endereco, telefone FROM Cliente WHERE cpf = %s",
                (cpf,),
            )
            linha = cursor.fetchone()
            if not linha:
                return None
            return Cliente(linha[0], linha[1], linha[2], linha[3], linha[4])
        finally:
            cursor.close()
            conexao.close()

    def buscar_por_nome(self, termo: str):
        """Busca parcial por nome (LIKE %termo%)."""
        conexao = get_connection()
        clientes = []
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(
                    "SELECT id_cliente, nome, cpf, endereco, telefone FROM Cliente WHERE nome ILIKE %s ORDER BY id_cliente",
                    (f"%{termo}%",),
                )
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
                cursor.execute(
                    "UPDATE Cliente SET nome = %s, cpf = %s, endereco = %s, telefone = %s WHERE id_cliente = %s",
                    (nome, cpf, endereco, telefone, id_cliente),
                )
                conexao.commit()
                return cursor.rowcount > 0
            finally:
                cursor.close()
                conexao.close()
        return False

    def deletar(self, id_cliente: int):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM Cliente WHERE id_cliente = %s", (id_cliente,))
                conexao.commit()
                return cursor.rowcount > 0
            finally:
                cursor.close()
                conexao.close()
        return False