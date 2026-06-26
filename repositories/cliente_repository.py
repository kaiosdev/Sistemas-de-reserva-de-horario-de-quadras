from database.connection import get_connection
from models.cliente import Cliente

class ClienteRepository:
    
    # 1. CREATE (INSERT)
    def inserir(self, cliente: Cliente):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "INSERT INTO Cliente (nome, cpf, telefone, email) VALUES (%s, %s, %s, %s)"
                # Acessando as propriedades encapsuladas do objeto Cliente
                valores = (cliente.nome, cliente.cpf, cliente.telefone, cliente.email)
                
                cursor.execute(sql, valores)
                conexao.commit()
                print(f" Cliente {cliente.nome} cadastrado com sucesso!")
                
            except Exception as e:
                print(f" Erro ao inserir cliente: {e}")
            finally:
                cursor.close()
                conexao.close()

    # 2. READ (SELECT)
    def listar_todos(self):
        conexao = get_connection()
        clientes = []
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "SELECT id_cliente, nome, cpf, telefone, email FROM Cliente"
                cursor.execute(sql)
                registros = cursor.fetchall()
                
                # Convertendo os registros do banco em Objetos Cliente
                for linha in registros:
                    cli = Cliente(id_cliente=linha[0], nome=linha[1], cpf=linha[2], telefone=linha[3], email=linha[4])
                    clientes.append(cli)
                    
            except Exception as e:
                print(f" Erro ao listar clientes: {e}")
            finally:
                cursor.close()
                conexao.close()
        return clientes

    # 3. UPDATE (UPDATE)
    def atualizar(self, cliente: Cliente):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "UPDATE Cliente SET nome = %s, telefone = %s, email = %s WHERE cpf = %s"
                # Usando o CPF como base para não alterar os dados privados
                valores = (cliente.nome, cliente.telefone, cliente.email, cliente.cpf)
                
                cursor.execute(sql, valores)
                conexao.commit()
                print(f" Dados do cliente {cliente.nome} atualizados com sucesso!")
                
            except Exception as e:
                print(f" Erro ao atualizar cliente: {e}")
            finally:
                cursor.close()
                conexao.close()

    # 4. DELETE (DELETE)
    def deletar(self, cpf: str):
        conexao = get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "DELETE FROM Cliente WHERE cpf = %s"
                cursor.execute(sql, (cpf,))
                conexao.commit()
                print(f"Cliente com CPF {cpf} excluído com sucesso!")
                
            except Exception as e:
                print(f"Erro ao deletar cliente: {e}")
            finally:
                cursor.close()
                conexao.close()