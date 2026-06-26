from models.cliente import Cliente
from repositories.cliente_repository import ClienteRepository

class ClienteService:
    def __init__(self):
        self.repository = ClienteRepository()

    def cadastrar_cliente_texto(self, texto: str):
        try:
            # Utilizando o Named Constructor
            novo_cliente = Cliente.de_texto(texto)
            
            # Regras de Negocio
            if len(novo_cliente.cpf) != 11 and len(novo_cliente.cpf) != 14:
                print("Erro: O CPF deve conter 11 digitos (ou 14 com pontuacao).")
                return
                
            self.repository.inserir(novo_cliente)
        except Exception as e:
            print(f"Erro ao processar o texto de cadastro: {e}")

    def listar_clientes(self):
        return self.repository.listar_todos()

    def atualizar_cliente(self, nome: str, cpf: str, endereco: str, telefone: str):
        cliente_atualizado = Cliente(0, nome, cpf, endereco, telefone)
        self.repository.atualizar(cliente_atualizado)

    def deletar_cliente(self, cpf: str):
        if not cpf:
            print("Erro: O CPF e obrigatorio para exclusao.")
            return
        self.repository.deletar(cpf)