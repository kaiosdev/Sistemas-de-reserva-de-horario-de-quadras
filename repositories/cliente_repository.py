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
                print(f"Sucesso: Cliente {cliente.nome} cadastrado!")
            except Exception as e:
                print(f"Erro ao inserir cliente: {e}")
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
                registros = cursor.fetchall()
                for linha in registros:
                    cli = Cliente(id_cliente=linha[0], nome=linha[1], cpf=linha[2], endereco=linha[3], telefone=linha[4])
                    clientes.append(cli)
            except Exception as e:
                print(f"Erro ao listar clientes: {e}")
            finally:
                cursor.close()
                conexao.close()
        return clientes

    def atualizar(self, cliente: Cliente):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "UPDATE Cliente SET nome = %s, endereco = %s, telefone = %s WHERE cpf = %s"
                valores = (cliente.nome, cliente.endereco, cliente.telefone, cliente.cpf)
                cursor.execute(sql, valores)
                conexao.commit()
                print(f"Sucesso: Dados de {cliente.nome} atualizados!")
            except Exception as e:
                print(f"Erro ao atualizar cliente: {e}")
            finally:
                cursor.close()
                conexao.close()

    def deletar(self, cpf: str):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "DELETE FROM Cliente WHERE cpf = %s"
                cursor.execute(sql, (cpf,))
                conexao.commit()
                print(f"Sucesso: Cliente com CPF {cpf} excluido!")
            except Exception as e:
                print(f"Erro ao deletar cliente: {e}")
            finally:
                cursor.close()
                conexao.close()