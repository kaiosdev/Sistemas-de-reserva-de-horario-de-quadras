class Cliente:
    # Atributo de classe (compartilhado por todas as instancias)
    total_clientes = 0 

    def __init__(self, id_cliente: int, nome: str, cpf: str, endereco: str, telefone: str = "Nao informado"):
        self.id_cliente = id_cliente
        self.nome = nome
        self.__cpf = cpf  # Encapsulamento
        self.endereco = endereco
        self.telefone = telefone
        Cliente.total_clientes += 1

    @property
    def cpf(self):
        return self.__cpf

    # Factory Method / Named Constructor
    @classmethod
    def de_texto(cls, texto: str):
        # Formato esperado: "id, nome, cpf, endereco, telefone"
        partes = texto.split(",")
        return cls(int(partes[0]), partes[1].strip(), partes[2].strip(), partes[3].strip(), partes[4].strip())

    # Metodos especiais
    def __str__(self):
        return f"Cliente(ID: {self.id_cliente} | Nome: {self.nome})"

    def __repr__(self):
        return f"Cliente(id_cliente={self.id_cliente}, nome='{self.nome}', cpf='{self.cpf}')"

    def __eq__(self, outro):
        if not isinstance(outro, Cliente):
            return False
        return self.cpf == outro.cpf