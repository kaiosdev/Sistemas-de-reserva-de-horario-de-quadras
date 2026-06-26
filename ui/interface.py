import tkinter as tk
from tkinter import messagebox
from services.cliente_service import ClienteService
from models.pagamento import PagamentoPix, PagamentoCartao

class AthletixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Athletix - Gestao Esportiva")
        self.root.geometry("600x450")
        
        self.cliente_service = ClienteService()
        self.setup_ui()

    def setup_ui(self):
        # Frame de Cadastro via Texto (Testando Named Constructor)
        frame_cadastro = tk.LabelFrame(self.root, text="Cadastrar Cliente via Texto")
        frame_cadastro.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame_cadastro, text="Formato: ID, Nome, CPF, Endereco, Telefone").pack(anchor="w", padx=5)
        self.entry_texto = tk.Entry(frame_cadastro, width=80)
        self.entry_texto.pack(padx=5, pady=5)
        
        btn_cadastrar = tk.Button(frame_cadastro, text="Cadastrar", command=self.cadastrar_cliente)
        btn_cadastrar.pack(pady=5)
        
        # Frame de Listagem
        frame_lista = tk.LabelFrame(self.root, text="Clientes Cadastrados")
        frame_lista.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.listbox_clientes = tk.Listbox(frame_lista)
        self.listbox_clientes.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Frame de Botoes de Acao
        frame_acoes = tk.Frame(self.root)
        frame_acoes.pack(fill="x", padx=10, pady=10)
        
        btn_listar = tk.Button(frame_acoes, text="Atualizar Lista", command=self.atualizar_lista)
        btn_listar.pack(side="left", padx=5)
        
        btn_deletar = tk.Button(frame_acoes, text="Deletar Selecionado", command=self.deletar_cliente)
        btn_deletar.pack(side="left", padx=5)
        
        btn_polimorfismo = tk.Button(frame_acoes, text="Testar Polimorfismo", command=self.testar_polimorfismo)
        btn_polimorfismo.pack(side="right", padx=5)
        
        self.atualizar_lista()

    def cadastrar_cliente(self):
        texto = self.entry_texto.get()
        if not texto:
            messagebox.showwarning("Aviso", "Digite os dados do cliente.")
            return
        
        try:
            self.cliente_service.cadastrar_cliente_texto(texto)
            messagebox.showinfo("Sucesso", "Comando de cadastro enviado ao banco de dados.")
            self.entry_texto.delete(0, tk.END)
            self.atualizar_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na operacao: {e}")

    def atualizar_lista(self):
        self.listbox_clientes.delete(0, tk.END)
        clientes = self.cliente_service.listar_clientes()
        for cli in clientes:
            # Mostra o CPF oculto (encapsulamento), o nome e o telefone na lista
            self.listbox_clientes.insert(tk.END, f"{cli.cpf} - {cli.nome} - {cli.telefone}")

    def deletar_cliente(self):
        selecionado = self.listbox_clientes.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente na lista para deletar.")
            return
        
        item_texto = self.listbox_clientes.get(selecionado[0])
        cpf = item_texto.split(" - ")[0] # Extrai o CPF da string exibida na lista
        
        self.cliente_service.deletar_cliente(cpf)
        messagebox.showinfo("Sucesso", f"Cliente com CPF {cpf} deletado.")
        self.atualizar_lista()

    def testar_polimorfismo(self):
        # Instancia as classes filhas de Pagamento
        pag_pix = PagamentoPix(id_pagamento=1, valor_total=150.00, id_agendamento=101, chave_pix="123.456.789-00")
        pag_cartao = PagamentoCartao(id_pagamento=2, valor_total=300.00, id_agendamento=102, final_cartao="4321")
        
        # Chama os metodos polimorficos
        pag_pix.processar()
        pag_cartao.processar()
        
        resultado = (
            f"Processamento concluido na memoria.\n\n"
            f"PIX Status: {pag_pix.status}\n"
            f"Cartao Status: {pag_cartao.status}\n\n"
            f"Verifique o terminal do VS Code para os logs completos da transacao."
        )
        messagebox.showinfo("Teste de Polimorfismo e Ligacao Dinamica", resultado)