class Cliente:
    def __init__(self, id_cliente: int, nome: str, cpf: str, telefone: str, email: str):
        self.id_cliente = id_cliente
        self.nome = nome
        self.__cpf = cpf       
        self.telefone = telefone
        self.__email = email    

    @property
    def cpf(self):
        return self.__cpf
    @property
    def email(self):
        return self.__email

    def __str__(self):
        return f"Cliente(ID: {self.id_cliente} | Nome: {self.nome} | E-mail: {self.email})"