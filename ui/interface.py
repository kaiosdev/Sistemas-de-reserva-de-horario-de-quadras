import tkinter as tk
from tkinter import ttk, messagebox
import re # Usado para validacoes basicas
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
        self.root.geometry("700x550")
        
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
        
        tk.Label(frame, text="Nome da Quadra:").grid(row=0, column=0, sticky="e", pady=5)
        self.entry_nome_quadra = tk.Entry(frame, width=30)
        self.entry_nome_quadra.grid(row=0, column=1, padx=5)
        
        tk.Label(frame, text="Valor/Hora (R$):").grid(row=1, column=0, sticky="e", pady=5)
        self.entry_valor_quadra = tk.Entry(frame, width=15)
        self.entry_valor_quadra.grid(row=1, column=1, sticky="w", padx=5)
        
        tk.Button(frame, text="Salvar Espaco", command=self.salvar_espaco).grid(row=2, columnspan=2, pady=15)

    def setup_tab_clientes(self):
        tk.Label(self.tab_clientes, text="Cadastro de Clientes", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Nova interface segregada (UX melhorada)
        frame = tk.Frame(self.tab_clientes)
        frame.pack(pady=5)
        
        tk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="e", pady=2)
        self.entry_nome_cli = tk.Entry(frame, width=40)
        self.entry_nome_cli.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(frame, text="CPF (11 digitos):").grid(row=1, column=0, sticky="e", pady=2)
        self.entry_cpf_cli = tk.Entry(frame, width=20)
        self.entry_cpf_cli.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        tk.Label(frame, text="Endereco:").grid(row=2, column=0, sticky="e", pady=2)
        self.entry_end_cli = tk.Entry(frame, width=40)
        self.entry_end_cli.grid(row=2, column=1, padx=5, pady=2)
        
        tk.Label(frame, text="Telefone:").grid(row=3, column=0, sticky="e", pady=2)
        self.entry_tel_cli = tk.Entry(frame, width=20)
        self.entry_tel_cli.grid(row=3, column=1, sticky="w", padx=5, pady=2)
        
        tk.Button(frame, text="Cadastrar Cliente", command=self.cadastrar_cliente_seguro).grid(row=4, columnspan=2, pady=15)

    def setup_tab_agendamentos(self):
        tk.Label(self.tab_agendamentos, text="Reserva de Horarios", font=("Arial", 12, "bold")).pack(pady=10)
        frame = tk.Frame(self.tab_agendamentos)
        frame.pack(pady=10)
        
        tk.Button(frame, text="🔄 Atualizar Listas", command=self.carregar_dados).grid(row=0, columnspan=2, pady=10)
        
        tk.Label(frame, text="Cliente:").grid(row=1, column=0, sticky="e", pady=5)
        self.combo_clientes = ttk.Combobox(frame, width=40, state="readonly")
        self.combo_clientes.grid(row=1, column=1, padx=5)
        
        tk.Label(frame, text="Espaco:").grid(row=2, column=0, sticky="e", pady=5)
        self.combo_espacos = ttk.Combobox(frame, width=40, state="readonly")
        self.combo_espacos.grid(row=2, column=1, padx=5)
        
        tk.Label(frame, text="Data (YYYY-MM-DD):").grid(row=3, column=0, sticky="e", pady=5)
        self.entry_data = tk.Entry(frame, width=15)
        self.entry_data.grid(row=3, column=1, sticky="w", padx=5)
        
        tk.Label(frame, text="Inicio (HH:MM):").grid(row=4, column=0, sticky="e", pady=5)
        self.entry_inicio = tk.Entry(frame, width=10)
        self.entry_inicio.grid(row=4, column=1, sticky="w", padx=5)
        
        tk.Label(frame, text="Fim (HH:MM):").grid(row=5, column=0, sticky="e", pady=5)
        self.entry_fim = tk.Entry(frame, width=10)
        self.entry_fim.grid(row=5, column=1, sticky="w", padx=5)
        
        tk.Button(frame, text="Confirmar Reserva", command=self.confirmar_agendamento_seguro).grid(row=6, columnspan=2, pady=15)

    def setup_tab_pagamentos(self):
        tk.Label(self.tab_pagamentos, text="Processamento de Pagamento", font=("Arial", 12, "bold")).pack(pady=10)
        frame = tk.Frame(self.tab_pagamentos)
        frame.pack(pady=10)
        
        tk.Button(frame, text="🔄 Carregar Reservas Pendentes", command=self.carregar_reservas_pagamento).grid(row=0, columnspan=2, pady=10)
        
        tk.Label(frame, text="Selecione a Reserva:").grid(row=1, column=0, sticky="e", pady=5)
        self.combo_reservas_pagto = ttk.Combobox(frame, width=50, state="readonly")
        self.combo_reservas_pagto.grid(row=1, column=1, padx=5)
        
        tk.Label(frame, text="Forma de Pagamento:").grid(row=2, column=0, sticky="e", pady=15)
        self.forma_pagto = tk.StringVar(value="PIX")
        
        frame_radios = tk.Frame(frame)
        frame_radios.grid(row=2, column=1, sticky="w")
        tk.Radiobutton(frame_radios, text="PIX", variable=self.forma_pagto, value="PIX").pack(side="left")
        tk.Radiobutton(frame_radios, text="Cartao", variable=self.forma_pagto, value="CARTAO").pack(side="left")
        
        tk.Button(frame, text="Realizar Pagamento", command=self.processar_pagamento_seguro).grid(row=3, columnspan=2, pady=10)

    # ========================== ACOES E VALIDARCOES ==========================

    def salvar_espaco(self):
        nome = self.entry_nome_quadra.get()
        valor = self.entry_valor_quadra.get()
        if not nome or not valor:
            messagebox.showwarning("Aviso", "Preencha o nome e o valor da quadra.")
            return
        try:
            val_float = float(valor.replace(",", "."))
            novo_espaco = Espaco(0, nome, "Quadra Padrao", "Oficial", val_float)
            self.espaco_repo.inserir(novo_espaco)
            messagebox.showinfo("Sucesso", "Espaco cadastrado no PostgreSQL.")
            self.entry_nome_quadra.delete(0, tk.END)
            self.entry_valor_quadra.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "O valor da quadra deve ser numerico.")
        except Exception as e:
            messagebox.showerror("Erro do Banco", str(e))

    def cadastrar_cliente_seguro(self):
        nome = self.entry_nome_cli.get().replace(";", "")
        cpf = self.entry_cpf_cli.get().replace(";", "")
        endereco = self.entry_end_cli.get().replace(";", "")
        telefone = self.entry_tel_cli.get().replace(";", "")
        
        if not all([nome, cpf, endereco]):
            messagebox.showwarning("Aviso", "Nome, CPF e Endereco sao obrigatorios.")
            return
            
        # Solucao: Formata a string estruturada usando ; e envia pro Named Constructor (POO exigida)
        texto_formatado = f"{nome};{cpf};{endereco};{telefone}"
        
        try:
            self.cliente_service.cadastrar_cliente_texto(texto_formatado)
            messagebox.showinfo("Sucesso", "Cliente registrado com sucesso!")
            self.entry_nome_cli.delete(0, tk.END)
            self.entry_cpf_cli.delete(0, tk.END)
            self.entry_end_cli.delete(0, tk.END)
            self.entry_tel_cli.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def carregar_dados(self):
        self.combo_clientes['values'] = [f"{c.id_cliente} - {c.nome}" for c in self.cliente_service.listar_clientes()]
        self.combo_espacos['values'] = [f"{e.id_espaco} - {e.nome} (R${e.valor_hora:.2f})" for e in self.espaco_repo.listar_todos()]
        if self.combo_clientes['values']: self.combo_clientes.current(0)
        if self.combo_espacos['values']: self.combo_espacos.current(0)

    def confirmar_agendamento_seguro(self):
        cliente_sel = self.combo_clientes.get()
        espaco_sel = self.combo_espacos.get()
        data = self.entry_data.get()
        h_ini = self.entry_inicio.get()
        h_fim = self.entry_fim.get()
        
        if not all([cliente_sel, espaco_sel, data, h_ini, h_fim]):
            messagebox.showwarning("Aviso", "Preencha todos os campos da reserva.")
            return
            
        # Validacao simples de Data/Hora (UX)
        if not re.match(r"\d{4}-\d{2}-\d{2}", data):
            messagebox.showerror("Erro", "A data deve estar no formato YYYY-MM-DD")
            return
        if not re.match(r"\d{2}:\d{2}", h_ini) or not re.match(r"\d{2}:\d{2}", h_fim):
            messagebox.showerror("Erro", "As horas devem estar no formato HH:MM")
            return
            
        try:
            id_cliente = int(cliente_sel.split(" - ")[0])
            id_espaco = int(espaco_sel.split(" - ")[0])
            ag = Agendamento(0, data, h_ini, h_fim, id_cliente, id_espaco)
            
            # Aqui a Trigger do PostgreSQL atua!
            self.agendamento_repo.inserir(ag)
            messagebox.showinfo("Sucesso", "Reserva inserida sem choque de horarios!")
        except Exception as e:
            messagebox.showerror("Bloqueio pelo Banco de Dados", str(e))

    def carregar_reservas_pagamento(self):
        reservas = self.agendamento_repo.listar_todos()
        self.combo_reservas_pagto['values'] = [f"Reserva {r.id_agendamento}: {r.nome_cliente} em {r.nome_espaco}" for r in reservas]
        if self.combo_reservas_pagto['values']: self.combo_reservas_pagto.current(0)

    def processar_pagamento_seguro(self):
        reserva_sel = self.combo_reservas_pagto.get()
        if not reserva_sel:
            messagebox.showwarning("Aviso", "Carregue e selecione uma reserva pendente.")
            return
            
        try:
            id_agendamento = int(reserva_sel.split(":")[0].replace("Reserva ", ""))
            forma = self.forma_pagto.get()
            valor_simulado = 150.00 # Aqui idealmente buscaria o calculo real via select de join
            
            if forma == "PIX":
                pag = PagamentoPix(id_pagamento=0, valor_total=valor_simulado, id_agendamento=id_agendamento, chave_pix="123.456.789-00")
            else:
                pag = PagamentoCartao(id_pagamento=0, valor_total=valor_simulado, id_agendamento=id_agendamento, final_cartao="4321")
                
            pag.processar() # Polimorfismo e Ligacao Dinamica executados
            messagebox.showinfo("Polimorfismo POO", f"Transacao aprovada via {forma}.\n\nO metodo .processar() da subclasse foi acionado com sucesso. Status do objeto: {pag.status}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))