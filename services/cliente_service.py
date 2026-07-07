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

    def buscar(self, criterio: str):
        """Busca clientes por CPF (exato) ou nome (parcial).

        Regra: se o critério for numerico/curto, tenta CPF; senao, busca por nome.
        Sempre tenta ambos e concatena para nao depender de adivinhar a intencao.
        """
        criterio = (criterio or "").strip()
        if not criterio:
            return []

        # Tenta por CPF (exato)
        por_cpf = self.repository.buscar_por_cpf(criterio)
        # Tenta por nome (parcial, ILIKE)
        por_nome = self.repository.buscar_por_nome(criterio)

        # Concatena sem duplicar (usa id_cliente como chave)
        vistos = set()
        resultado = []
        for cli in ([por_cpf] if por_cpf else []) + por_nome:
            if cli and cli.id_cliente not in vistos:
                vistos.add(cli.id_cliente)
                resultado.append(cli)
        return resultado

    def atualizar(self, id_cliente, nome, cpf, endereco, telefone):
        nome = (nome or "").strip()
        cpf = (cpf or "").strip()
        if not nome:
            raise ValueError("O nome e obrigatorio.")
        if len(cpf) not in (11, 14):
            raise ValueError("O CPF deve conter 11 digitos.")
        return self.repository.atualizar(
            int(id_cliente), nome, cpf,
            (endereco or "").strip(),
            (telefone or "Nao informado").strip(),
        )

    def excluir(self, id_cliente: int):
        return self.repository.deletar(id_cliente)
