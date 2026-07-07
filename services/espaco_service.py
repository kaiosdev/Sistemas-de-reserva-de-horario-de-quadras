from repositories.espaco_repository import EspacoRepository
from repositories.modalidade_repository import ModalidadeRepository
from models.espaco import Espaco


class EspacoService:
    """Regras de negocio da entidade Espaco (quadra).

    Validacoes aplicadas antes de persistir:
      - nome obrigatorio e nao vazio
      - valor_hora deve ser positivo
      - descricao/tamanho recebem defaults quando omitidos
      - modalidade deve existir (default: 1 = Geral)
    """

    DESCRICAO_PADRAO = "Quadra Poliesportiva"
    TAMANHO_PADRAO = "Oficial"

    def __init__(self):
        self.repository = EspacoRepository()
        self.modalidade_repo = ModalidadeRepository()

    def listar_todos(self):
        return self.repository.listar_todos()

    def _validar_modalidade(self, id_modalidade):
        try:
            id_modalidade = int(id_modalidade)
        except (TypeError, ValueError):
            raise ValueError("Modalidade invalida.")
        validas = [m.id_modalidade for m in self.modalidade_repo.listar_todos()]
        if id_modalidade not in validas:
            raise ValueError("Modalidade selecionada nao existe.")
        return id_modalidade

    def cadastrar(self, nome: str, valor_hora, descricao: str = None, tamanho_quadra: str = None, id_modalidade: int = 1):
        nome = (nome or "").strip()
        if not nome:
            raise ValueError("O nome da quadra e obrigatorio.")

        try:
            valor = float(valor_hora)
        except (TypeError, ValueError):
            raise ValueError("O valor por hora deve ser numerico.")
        if valor <= 0:
            raise ValueError("O valor por hora deve ser maior que zero.")

        id_modalidade = self._validar_modalidade(id_modalidade)

        novo = Espaco(
            id_espaco=0,
            nome=nome,
            descricao=(descricao or self.DESCRICAO_PADRAO).strip(),
            tamanho_quadra=(tamanho_quadra or self.TAMANHO_PADRAO).strip(),
            valor_hora=valor,
            id_modalidade=id_modalidade,
        )
        self.repository.inserir(novo)
        return novo

    def atualizar(self, id_espaco, nome, valor_hora, descricao=None, tamanho_quadra=None, id_modalidade=1):
        nome = (nome or "").strip()
        if not nome:
            raise ValueError("O nome da quadra e obrigatorio.")
        try:
            valor = float(valor_hora)
        except (TypeError, ValueError):
            raise ValueError("O valor por hora deve ser numerico.")
        if valor <= 0:
            raise ValueError("O valor por hora deve ser maior que zero.")

        id_modalidade = self._validar_modalidade(id_modalidade)

        return self.repository.atualizar(
            int(id_espaco),
            nome,
            (descricao or self.DESCRICAO_PADRAO).strip(),
            (tamanho_quadra or self.TAMANHO_PADRAO).strip(),
            valor,
            id_modalidade,
        )

    def excluir(self, id_espaco: int):
        return self.repository.deletar(id_espaco)
