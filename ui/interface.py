import tkinter as tk
from tkinter import ttk, messagebox
from services.cliente_service import ClienteService
from repositories.espaco_repository import EspacoRepository
from repositories.agendamento_repository import AgendamentoRepository
from models.espaco import Espaco
from models.agendamento import Agendamento
from models.pagamento import PagamentoPix, PagamentoCartao

class AthletixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Athletix - Gestao Esportiva")
        self.root.geometry("700x500")
        
        self.cliente_service = ClienteService()
        self.espaco_repo = EspacoRepository()
        self.agendamento_repo = AgendamentoRepository()
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_espacos = ttk.Frame(self.notebook)
        self.tab_clientes = ttk.Frame(self.notebook)
        self.tab_agendamentos = ttk.Frame(self.notebook)
        self.tab_pagamentos = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_espacos, text="1. Espacos")
        self.notebook.add(self.tab_clientes, text="2. Clientes")
        self.notebook.add(self.tab_agendamentos, text="3. Agendamentos")
        self.notebook.add(self.tab_pagamentos, text="4. Pagamentos")
        
        self.setup_tab_espacos()
        self.setup_tab_clientes()
        self.setup_tab_agendamentos()
        self.setup_tab_pagamentos()

    def setup_tab_espacos(self):
        tk.Label(self.tab_espacos, text="Cadastro de Quadras", font=("Arial", 12, "bold")).pack(pady=10)
        frame = tk.Frame(self.tab_espacos)
        frame.pack(pady=5)
        
        tk.Label(frame, text="Nome da Quadra:").grid(row=0, column=0, sticky="w")
        self.entry_nome_quadra = tk.Entry(frame, width=30)
        self.entry_nome_quadra.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Valor/Hora (R$):").grid(row=1, column=0, sticky="w")
        self.entry_valor_quadra = tk.Entry(frame, width=15)
        self.entry_valor_quadra.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        tk.Button(self.tab_espacos, text="Salvar Espaco", command=self.salvar_espaco).pack(pady=10)

    def setup_tab_clientes(self):
        tk.Label(self.tab_clientes, text="Gestao de Clientes", font=("Arial", 12, "bold")).pack(pady=10)
        frame = tk.LabelFrame(self.tab_clientes, text="Cadastrar Cliente via Texto")
        frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame, text="Formato: ID, Nome, CPF, Endereco, Telefone").pack(anchor="w", padx=5)
        self.entry_texto_cliente = tk.Entry(frame, width=70)
        self.entry_texto_cliente.pack(padx=5, pady=5)
        tk.Button(frame, text="Cadastrar", command=self.cadastrar_cliente).pack(pady=5)

    def setup_tab_agendamentos(self):
        tk.Label(self.tab_agendamentos, text="Reserva de Horarios", font=("Arial", 12, "bold")).pack(pady=10)
        frame = tk.Frame(self.tab_agendamentos)
        frame.pack(pady=10)
        
        tk.Button(frame, text="Carregar Dados", command=self.carregar_dados_agendamento).grid(row=0, columnspan=2, pady=5)
        
        tk.Label(frame, text="Cliente:").grid(row=1, column=0, sticky="w")
        self.combo_clientes = ttk.Combobox(frame, width=40)
        self.combo_clientes.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Espaco:").grid(row=2, column=0, sticky="w")
        self.combo_espacos = ttk.Combobox(frame, width=40)
        self.combo_espacos.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Data (YYYY-MM-DD):").grid(row=3, column=0, sticky="w")
        self.entry_data = tk.Entry(frame, width=15)
        self.entry_data.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        tk.Label(frame, text="Inicio (HH:MM):").grid(row=4, column=0, sticky="w")
        self.entry_hora_inicio = tk.Entry(frame, width=10)
        self.entry_hora_inicio.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        
        tk.Label(frame, text="Fim (HH:MM):").grid(row=5, column=0, sticky="w")
        self.entry_hora_fim = tk.Entry(frame, width=10)
        self.entry_hora_fim.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        
        tk.Button(self.tab_agendamentos, text="Confirmar Agendamento", command=self.confirmar_agendamento).pack(pady=15)

    def setup_tab_pagamentos(self):
        tk.Label(self.tab_pagamentos, text="Processamento de Pagamento", font=("Arial", 12, "bold")).pack(pady=10)
        frame = tk.Frame(self.tab_pagamentos)
        frame.pack(pady=10)
        
        tk.Label(frame, text="Forma de Pagamento:").grid(row=0, column=0, sticky="w")
        self.forma_pagto_var = tk.StringVar(value="PIX")
        tk.Radiobutton(frame, text="PIX", variable=self.forma_pagto_var, value="PIX").grid(row=0, column=1, sticky="w")
        tk.Radiobutton(frame, text="Cartao de Credito", variable=self.forma_pagto_var, value="CARTAO").grid(row=0, column=2, sticky="w")
        
        tk.Button(self.tab_pagamentos, text="Processar Pagamento", command=self.processar_pagamento).pack(pady=15)

    def salvar_espaco(self):
        nome = self.entry_nome_quadra.get()
        valor = self.entry_valor_quadra.get()
        if not nome or not valor:
            messagebox.showwarning("Aviso", "Preencha o nome e o valor da quadra.")
            return
        try:
            novo_espaco = Espaco(0, nome, "Quadra Poliesportiva", "Oficial", float(valor))
            self.espaco_repo.inserir(novo_espaco)
            messagebox.showinfo("Sucesso", "Espaco cadastrado.")
            self.entry_nome_quadra.delete(0, tk.END)
            self.entry_valor_quadra.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def cadastrar_cliente(self):
        texto = self.entry_texto_cliente.get()
        if not texto:
            messagebox.showwarning("Aviso", "Digite os dados do cliente.")
            return
        try:
            self.cliente_service.cadastrar_cliente_texto(texto)
            messagebox.showinfo("Sucesso", "Cliente cadastrado.")
            self.entry_texto_cliente.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def carregar_dados_agendamento(self):
        clientes = self.cliente_service.listar_clientes()
        espacos = self.espaco_repo.listar_todos()
        self.combo_clientes['values'] = [f"{cli.id_cliente} - {cli.nome}" for cli in clientes]
        self.combo_espacos['values'] = [f"{esp.id_espaco} - {esp.nome}" for esp in espacos]

    def confirmar_agendamento(self):
        cliente_sel = self.combo_clientes.get()
        espaco_sel = self.combo_espacos.get()
        data = self.entry_data.get()
        h_ini = self.entry_hora_inicio.get()
        h_fim = self.entry_hora_fim.get()
        
        if not all([cliente_sel, espaco_sel, data, h_ini, h_fim]):
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return
        try:
            id_cliente = int(cliente_sel.split(" - ")[0])
            id_espaco = int(espaco_sel.split(" - ")[0])
            novo_agendamento = Agendamento(0, data, h_ini, h_fim, id_cliente, id_espaco)
            self.agendamento_repo.inserir(novo_agendamento)
            messagebox.showinfo("Sucesso", "Agendamento realizado.")
        except Exception as e:
            messagebox.showerror("Erro de Regra de Negocio", f"Falha no agendamento:\n{e}")

    def processar_pagamento(self):
        forma = self.forma_pagto_var.get()
        if forma == "PIX":
            pagamento = PagamentoPix(id_pagamento=1, valor_total=100.00, id_agendamento=1, chave_pix="123.456.789-00")
        else:
            pagamento = PagamentoCartao(id_pagamento=1, valor_total=100.00, id_agendamento=1, final_cartao="4321")
            
        pagamento.processar()
        messagebox.showinfo("Polimorfismo", f"O pagamento via {forma} foi processado. Status: {pagamento.status}")