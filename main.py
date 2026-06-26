import sys
from services.cliente_service import ClienteService
from models.pagamento import PagamentoPix, PagamentoCartao

def exibir_menu():
    print("\n" + "="*40)
    print("🏆 ATHLETIX - GESTÃO ESPORTIVA 🏆")
    print("="*40)
    print("1. Cadastrar Novo Cliente")
    print("2. Listar Clientes")
    print("3. Atualizar Cliente")
    print("4. Deletar Cliente")
    print("5. Testar Polimorfismo (Pagamento)")
    print("0. Sair")
    print("="*40)

def main():
    cliente_service = ClienteService()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\n--- NOVO CADASTRO ---")
            nome = input("Nome: ")
            cpf = input("CPF (apenas números ou com pontuação): ")
            telefone = input("Telefone: ")
            email = input("E-mail: ")
            cliente_service.cadastrar_cliente(0, nome, cpf, telefone, email)

        elif opcao == '2':
            print("\n--- LISTA DE CLIENTES ---")
            clientes = cliente_service.listar_clientes()
            if not clientes:
                print("Nenhum cliente cadastrado.")
            else:
                for cli in clientes:
                    # Aqui o Python chama automaticamente o método __str__ que criamos
                    print(cli)

        elif opcao == '3':
            print("\n--- ATUALIZAR CLIENTE ---")
            cpf = input("Informe o CPF do cliente que deseja atualizar: ")
            nome = input("Novo Nome: ")
            telefone = input("Novo Telefone: ")
            email = input("Novo E-mail: ")
            cliente_service.atualizar_cliente(nome, cpf, telefone, email)

        elif opcao == '4':
            print("\n--- DELETAR CLIENTE ---")
            cpf = input("Informe o CPF do cliente a ser deletado: ")
            cliente_service.deletar_cliente(cpf)

        elif opcao == '5':
            print("\n--- TESTE DE POLIMORFISMO (PAGAMENTO) ---")
            print("Gerando cobranças fictícias para demonstração...")
            
            pag_pix = PagamentoPix(id_pagamento=1, valor_total=150.00, status='Pendente', id_agendamento=101)
            pag_cartao = PagamentoCartao(id_pagamento=2, valor_total=300.00, status='Pendente', id_agendamento=102)
            
            # Ligação Dinâmica e Polimorfismo em ação:
            lista_pagamentos = [pag_pix, pag_cartao]
            for pag in lista_pagamentos:
                pag.processar() # O mesmo método se comporta diferente dependendo da classe filha!
                print(pag)

        elif opcao == '0':
            print("Saindo do Athletix... Até logo!")
            sys.exit()
            
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()