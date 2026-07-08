from models.cliente import Cliente
from repositories.cliente_repository import ClienteRepository

class ClienteService:
    def __init__(self):
        self.repository = ClienteRepository()

    def cadastrar_cliente_texto(self, texto: str):
        novo_cliente = Cliente.de_texto(texto)
        if len(novo_cliente.cpf) not in (11, 14):
            raise ValueError("O CPF deve conter 11 digitos.")
        self.repository.inserir(novo_cliente)

    def listar_clientes(self):
        return self.repository.listar_todos()

    def excluir_cliente(self, id_cliente: int):
        self.repository.excluir(id_cliente)
    
    def atualizar_cliente(self, id_cliente: int, texto: str):
        from models.cliente import Cliente
        cli = Cliente.de_texto(texto)
        self.repository.atualizar(id_cliente, cli.nome, cli.cpf, cli.endereco, cli.telefone)

    def excluir_cliente(self, id_cliente: int):
        self.repository.excluir(id_cliente)