class Cliente:
    total_clientes = 0 

    def __init__(self, id_cliente: int, nome: str, cpf: str, endereco: str, telefone: str = "Nao informado"):
        self.id_cliente = id_cliente
        self.nome = nome
        self._cpf = cpf 
        self.endereco = endereco
        self.telefone = telefone
        Cliente.total_clientes += 1

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, novo_cpf: str):
        if len(novo_cpf.strip()) not in (11, 14):
            raise ValueError("Erro: CPF invalido.")
        self._cpf = novo_cpf

    @classmethod
    def de_texto(cls, texto: str):
        partes = texto.split(";")
        if len(partes) != 4:
            raise ValueError("O texto nao possui a quantidade de campos esperada.")
        
        return cls(0, partes[0].strip(), partes[1].strip(), partes[2].strip(), partes[3].strip())

    def __str__(self):
        return f"Cliente: {self.nome} | Telefone: {self.telefone}"

    def __repr__(self):
        return f"Cliente(id_cliente={self.id_cliente}, nome='{self.nome}', cpf='{self._cpf}')"

    def __eq__(self, outro):
        if not isinstance(outro, Cliente):
            return False
        return self._cpf == outro.cpf