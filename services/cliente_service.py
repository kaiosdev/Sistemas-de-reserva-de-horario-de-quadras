from models.cliente import Cliente
from repositories.cliente_repository import ClienteRepository

class ClienteService:
    def __init__(self):
        self.repository = ClienteRepository()

    def cadastrar_cliente(self, id_cliente: int, nome: str, cpf: str, telefone: str, email: str):
        # Regra de Negócio 1: Validação de tamanho de CPF
        if len(cpf) != 11 and len(cpf) != 14:
            print("❌ Erro de Validação: O CPF deve conter 11 dígitos (ou 14 com pontuação).")
            return

        # Regra de Negócio 2: O e-mail precisa conter '@'
        if "@" not in email:
            print("❌ Erro de Validação: E-mail inválido.")
            return

        # Se passou pelas validações, cria o objeto e envia para o repositório
        novo_cliente = Cliente(id_cliente, nome, cpf, telefone, email)
        self.repository.inserir(novo_cliente)

    def listar_clientes(self):
        return self.repository.listar_todos()

    def atualizar_cliente(self, nome: str, cpf: str, telefone: str, email: str):
        # Para atualizar, usamos um ID fictício (0) pois a busca no banco será pelo CPF
        cliente_atualizado = Cliente(0, nome, cpf, telefone, email)
        self.repository.atualizar(cliente_atualizado)

    def deletar_cliente(self, cpf: str):
        if not cpf:
            print("❌ Erro: O CPF é obrigatório para exclusão.")
            return
        self.repository.deletar(cpf)