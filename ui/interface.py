import tkinter as tk
from tkinter import ttk, messagebox
import re
from tkcalendar import DateEntry

# Importação dos Serviços
from services.cliente_service import ClienteService
from services.modalidade_service import ModalidadeService
from services.espaco_service import EspacoService
from services.agendamento_service import AgendamentoService
from services.pagamento_service import PagamentoService

class AthletixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Athletix - Gestão de Complexos Esportivos")
        self.root.geometry("1100x750")
        self.root.configure(bg="#ecf0f1")
        
        # 1. Aplicação do Estilo Moderno
        self.aplicar_estilo_moderno()
        
        # 2. Inicialização dos Serviços (Regras de Negócio e BD)
        self.cliente_service = ClienteService()
        self.modalidade_service = ModalidadeService()
        self.espaco_service = EspacoService()
        self.agendamento_service = AgendamentoService()
        self.pagamento_service = PagamentoService()
        
        self.reservas_memoria = [] # Cache para uso no pagamento
        
        # 3. Cabeçalho
        header = tk.Frame(self.root, bg="#2c3e50", height=60)
        header.pack(fill="x", side="top")
        tk.Label(header, text="ATHLETIX - Gestão Esportiva", font=("Segoe UI", 18, "bold"), fg="white", bg="#2c3e50").pack(pady=15)
        
        # 4. Sistema de Abas (Notebook)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.tab_clientes = ttk.Frame(self.notebook)
        self.tab_modalidades = ttk.Frame(self.notebook)
        self.tab_espacos = ttk.Frame(self.notebook)
        self.tab_agendamentos = ttk.Frame(self.notebook)
        self.tab_pagamentos = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_clientes, text="👤 Clientes")
        self.notebook.add(self.tab_modalidades, text="🎯 Modalidades")
        self.notebook.add(self.tab_espacos, text="🏟️ Espaços")
        self.notebook.add(self.tab_agendamentos, text="📅 Reservas")
        self.notebook.add(self.tab_pagamentos, text="💳 Caixa")
        
        # Variáveis de Seleção para o CRUD (Guardam o ID do item clicado na tabela)
        self.id_cliente_sel = tk.StringVar()
        self.id_modalidade_sel = tk.StringVar()
        self.id_espaco_sel = tk.StringVar()
        self.id_agendamento_sel = tk.StringVar()
        self.id_pagamento_sel = tk.StringVar()
        
        # 5. Construção das Telas
        self.setup_tab_clientes()
        self.setup_tab_modalidades()
        self.setup_tab_espacos()
        self.setup_tab_agendamentos()
        self.setup_tab_pagamentos()

    def aplicar_estilo_moderno(self):
        style = ttk.Style()
        style.theme_use('clam') 
        style.configure("TNotebook", background="#ecf0f1", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=[15, 8], background="#bdc3c7", foreground="#2c3e50")
        style.map("TNotebook.Tab", background=[("selected", "#3498db")], foreground=[("selected", "white")])
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff", font=("Segoe UI", 10), foreground="#34495e")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6, background="#ecf0f1")
        style.configure("Acao.TButton", background="#3498db", foreground="white")
        style.configure("Alerta.TButton", background="#e74c3c", foreground="white")
        style.configure("Sucesso.TButton", background="#2ecc71", foreground="white")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=30, borderwidth=0)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#ecf0f1", foreground="#2c3e50")
        style.map("Treeview", background=[("selected", "#3498db")])

    # ========================== ABA 1: CLIENTES ==========================
    def setup_tab_clientes(self):
        frame_form = ttk.Frame(self.tab_clientes)
        frame_form.pack(pady=20, fill="x", padx=20)
        
        ttk.Label(frame_form, text="Nome Completo:").grid(row=0, column=0, sticky="e", padx=5, pady=8)
        self.entry_nome_cli = ttk.Entry(frame_form, width=35, font=("Segoe UI", 10))
        self.entry_nome_cli.grid(row=0, column=1, padx=5, pady=8)
        
        ttk.Label(frame_form, text="CPF:").grid(row=0, column=2, sticky="e", padx=5, pady=8)
        self.entry_cpf_cli = ttk.Entry(frame_form, width=20, font=("Segoe UI", 10))
        self.entry_cpf_cli.grid(row=0, column=3, padx=5, pady=8)
        
        ttk.Label(frame_form, text="Endereço:").grid(row=1, column=0, sticky="e", padx=5, pady=8)
        self.entry_end_cli = ttk.Entry(frame_form, width=35, font=("Segoe UI", 10))
        self.entry_end_cli.grid(row=1, column=1, padx=5, pady=8)
        
        ttk.Label(frame_form, text="Telefone:").grid(row=1, column=2, sticky="e", padx=5, pady=8)
        self.entry_tel_cli = ttk.Entry(frame_form, width=20, font=("Segoe UI", 10))
        self.entry_tel_cli.grid(row=1, column=3, padx=5, pady=8)
        
        frame_btn = ttk.Frame(self.tab_clientes)
        frame_btn.pack(pady=10)
        ttk.Button(frame_btn, text="✔ Salvar Cliente", command=self.salvar_cliente, style="Acao.TButton").pack(side="left", padx=10)
        ttk.Button(frame_btn, text="✖ Excluir Selecionado", command=self.excluir_cliente, style="Alerta.TButton").pack(side="left", padx=10)
        ttk.Button(frame_btn, text="🔄 Limpar", command=self.limpar_cliente).pack(side="left", padx=10)

        colunas = ("ID", "Nome", "CPF", "Endereço", "Telefone")
        self.tree_clientes = ttk.Treeview(self.tab_clientes, columns=colunas, show="headings", height=12)
        for c in colunas: self.tree_clientes.heading(c, text=c)
        self.tree_clientes.column("ID", width=50, anchor="center")
        self.tree_clientes.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree_clientes.bind("<ButtonRelease-1>", self.selecionar_cliente)
        
        self.carregar_clientes()

    def carregar_clientes(self):
        for item in self.tree_clientes.get_children(): self.tree_clientes.delete(item)
        try:
            for c in self.cliente_service.listar_clientes():
                self.tree_clientes.insert("", "end", values=(c.id_cliente, c.nome, c.cpf, c.endereco, c.telefone))
        except Exception: pass

    def selecionar_cliente(self, event):
        sel = self.tree_clientes.selection()
        if sel:
            v = self.tree_clientes.item(sel, 'values')
            self.id_cliente_sel.set(v[0])
            self.entry_nome_cli.delete(0, tk.END); self.entry_nome_cli.insert(0, v[1])
            self.entry_cpf_cli.delete(0, tk.END); self.entry_cpf_cli.insert(0, v[2])
            self.entry_end_cli.delete(0, tk.END); self.entry_end_cli.insert(0, v[3])
            self.entry_tel_cli.delete(0, tk.END); self.entry_tel_cli.insert(0, v[4])

    def limpar_cliente(self):
        self.id_cliente_sel.set("")
        self.entry_nome_cli.delete(0, tk.END); self.entry_cpf_cli.delete(0, tk.END)
        self.entry_end_cli.delete(0, tk.END); self.entry_tel_cli.delete(0, tk.END)

    def salvar_cliente(self):
        texto = f"{self.entry_nome_cli.get()};{self.entry_cpf_cli.get()};{self.entry_end_cli.get()};{self.entry_tel_cli.get()}"
        try:
            if self.id_cliente_sel.get():
                self.cliente_service.atualizar_cliente(int(self.id_cliente_sel.get()), texto)
                messagebox.showinfo("Sucesso", "Cliente atualizado!")
            else:
                self.cliente_service.cadastrar_cliente_texto(texto)
                messagebox.showinfo("Sucesso", "Cliente cadastrado!")
            self.limpar_cliente(); self.carregar_clientes()
        except Exception as e: messagebox.showerror("Erro de Validação", str(e))

    def excluir_cliente(self):
        if not self.id_cliente_sel.get(): return
        if messagebox.askyesno("Confirmar", "Deseja excluir este cliente?"):
            try:
                self.cliente_service.excluir_cliente(int(self.id_cliente_sel.get()))
                self.limpar_cliente(); self.carregar_clientes()
            except Exception: messagebox.showerror("Erro de BD", "O cliente possui agendamentos ativos.")

    # ========================== ABA 2: MODALIDADES ==========================
    def setup_tab_modalidades(self):
        frame_form = ttk.Frame(self.tab_modalidades)
        frame_form.pack(pady=20, fill="x", padx=20)
        
        ttk.Label(frame_form, text="Nome da Modalidade (Ex: Futsal, Vôlei):").grid(row=0, column=0, sticky="e", padx=5, pady=8)
        self.entry_nome_mod = ttk.Entry(frame_form, width=40, font=("Segoe UI", 10))
        self.entry_nome_mod.grid(row=0, column=1, padx=5, pady=8)
        
        frame_btn = ttk.Frame(self.tab_modalidades)
        frame_btn.pack(pady=10)
        ttk.Button(frame_btn, text="✔ Salvar Modalidade", command=self.salvar_modalidade, style="Acao.TButton").pack(side="left", padx=10)
        ttk.Button(frame_btn, text="✖ Excluir Modalidade", command=self.excluir_modalidade, style="Alerta.TButton").pack(side="left", padx=10)
        ttk.Button(frame_btn, text="🔄 Limpar", command=self.limpar_modalidade).pack(side="left", padx=10)

        colunas = ("ID", "Nome da Modalidade")
        self.tree_modalidades = ttk.Treeview(self.tab_modalidades, columns=colunas, show="headings", height=10)
        for c in colunas: self.tree_modalidades.heading(c, text=c)
        self.tree_modalidades.column("ID", width=100, anchor="center")
        self.tree_modalidades.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree_modalidades.bind("<ButtonRelease-1>", self.selecionar_modalidade)
        
        self.carregar_modalidades()

    def carregar_modalidades(self):
        for item in self.tree_modalidades.get_children(): self.tree_modalidades.delete(item)
        try:
            for m in self.modalidade_service.listar_modalidades():
                self.tree_modalidades.insert("", "end", values=(m.id_modalidade, m.nome))
        except Exception: pass

    def selecionar_modalidade(self, event):
        sel = self.tree_modalidades.selection()
        if sel:
            v = self.tree_modalidades.item(sel, 'values')
            self.id_modalidade_sel.set(v[0])
            self.entry_nome_mod.delete(0, tk.END); self.entry_nome_mod.insert(0, v[1])

    def limpar_modalidade(self):
        self.id_modalidade_sel.set("")
        self.entry_nome_mod.delete(0, tk.END)

    def salvar_modalidade(self):
        nome = self.entry_nome_mod.get()
        if not nome.strip():
            messagebox.showwarning("Aviso", "O nome não pode ser vazio.")
            return
        try:
            if self.id_modalidade_sel.get():
                self.modalidade_service.atualizar_modalidade(int(self.id_modalidade_sel.get()), nome)
            else:
                self.modalidade_service.cadastrar_modalidade(nome)
            self.limpar_modalidade(); self.carregar_modalidades()
            self.sincronizar_combos_espacos()
            messagebox.showinfo("Sucesso", "Modalidade salva!")
        except Exception as e: messagebox.showerror("Erro", str(e))

    def excluir_modalidade(self):
        if not self.id_modalidade_sel.get(): return
        if messagebox.askyesno("Confirmar", "Deseja excluir esta modalidade?"):
            try:
                self.modalidade_service.excluir_modalidade(int(self.id_modalidade_sel.get()))
                self.limpar_modalidade(); self.carregar_modalidades()
                self.sincronizar_combos_espacos()
            except Exception: messagebox.showerror("Erro de BD", "Modalidade vinculada a um espaço não pode ser excluída.")

    # ========================== ABA 3: ESPAÇOS ==========================
    def setup_tab_espacos(self):
        frame_form = ttk.Frame(self.tab_espacos)
        frame_form.pack(pady=20, fill="x", padx=20)
        
        ttk.Button(frame_form, text="🔄 Sincronizar Modalidades", command=self.sincronizar_combos_espacos).grid(row=0, columnspan=4, pady=10)

        ttk.Label(frame_form, text="Nome Quadra:").grid(row=1, column=0, sticky="e", padx=5, pady=8)
        self.entry_nome_esp = ttk.Entry(frame_form, width=30)
        self.entry_nome_esp.grid(row=1, column=1, padx=5, pady=8)
        
        ttk.Label(frame_form, text="Valor/Hora (R$):").grid(row=1, column=2, sticky="e", padx=5, pady=8)
        self.entry_val_esp = ttk.Entry(frame_form, width=15)
        self.entry_val_esp.grid(row=1, column=3, sticky="w", padx=5, pady=8)
        
        ttk.Label(frame_form, text="Dimensões:").grid(row=2, column=0, sticky="e", padx=5, pady=8)
        self.entry_tam_esp = ttk.Entry(frame_form, width=30)
        self.entry_tam_esp.grid(row=2, column=1, padx=5, pady=8)
        
        ttk.Label(frame_form, text="Modalidade:").grid(row=2, column=2, sticky="e", padx=5, pady=8)
        self.combo_modalidades = ttk.Combobox(frame_form, width=25, state="readonly")
        self.combo_modalidades.grid(row=2, column=3, sticky="w", padx=5, pady=8)
        
        frame_btn = ttk.Frame(self.tab_espacos)
        frame_btn.pack(pady=10)
        ttk.Button(frame_btn, text="✔ Salvar Espaço", command=self.salvar_espaco, style="Acao.TButton").pack(side="left", padx=10)
        ttk.Button(frame_btn, text="✖ Excluir Espaço", command=self.excluir_espaco, style="Alerta.TButton").pack(side="left", padx=10)
        ttk.Button(frame_btn, text="🔄 Limpar", command=self.limpar_espaco).pack(side="left", padx=10)

        colunas = ("ID", "Nome", "Dimensões", "Modalidade", "Valor/Hora")
        self.tree_espacos = ttk.Treeview(self.tab_espacos, columns=colunas, show="headings", height=10)
        for c in colunas: self.tree_espacos.heading(c, text=c)
        self.tree_espacos.column("ID", width=50, anchor="center")
        self.tree_espacos.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree_espacos.bind("<ButtonRelease-1>", self.selecionar_espaco)
        
        self.sincronizar_combos_espacos()
        self.carregar_espacos()

    def sincronizar_combos_espacos(self):
        try:
            mods = self.modalidade_service.listar_modalidades()
            self.combo_modalidades['values'] = [f"{m.id_modalidade} - {m.nome}" for m in mods]
        except Exception: pass

    def carregar_espacos(self):
        for item in self.tree_espacos.get_children(): self.tree_espacos.delete(item)
        try:
            for e in self.espaco_service.listar_espacos():
                nome_mod = getattr(e, "nome_modalidade", f"Mod {e.id_modalidade}")
                self.tree_espacos.insert("", "end", values=(e.id_espaco, e.nome, e.tamanho_quadra, nome_mod, f"R$ {e.valor_hora:.2f}"))
        except Exception: pass

    def selecionar_espaco(self, event):
        sel = self.tree_espacos.selection()
        if sel:
            v = self.tree_espacos.item(sel, 'values')
            self.id_espaco_sel.set(v[0])
            self.entry_nome_esp.delete(0, tk.END); self.entry_nome_esp.insert(0, v[1])
            self.entry_tam_esp.delete(0, tk.END); self.entry_tam_esp.insert(0, v[2])
            self.entry_val_esp.delete(0, tk.END); self.entry_val_esp.insert(0, v[4].replace("R$ ", ""))

    def limpar_espaco(self):
        self.id_espaco_sel.set("")
        self.entry_nome_esp.delete(0, tk.END); self.entry_tam_esp.delete(0, tk.END)
        self.entry_val_esp.delete(0, tk.END); self.combo_modalidades.set("")

    def salvar_espaco(self):
        nome = self.entry_nome_esp.get()
        tam = self.entry_tam_esp.get()
        val = self.entry_val_esp.get()
        mod_str = self.combo_modalidades.get()
        
        if not nome or not val or not mod_str:
            messagebox.showwarning("Aviso", "Preencha Nome, Valor e escolha uma Modalidade.")
            return
            
        id_mod = int(mod_str.split(" - ")[0])
        try:
            if self.id_espaco_sel.get():
                self.espaco_service.atualizar_espaco(int(self.id_espaco_sel.get()), nome, "Quadra", tam, val, id_mod)
            else:
                self.espaco_service.cadastrar_espaco(nome, "Quadra", tam, val, id_mod)
            self.limpar_espaco(); self.carregar_espacos()
            messagebox.showinfo("Sucesso", "Espaço salvo com sucesso!")
        except Exception as e: messagebox.showerror("Erro", str(e))

    def excluir_espaco(self):
        if not self.id_espaco_sel.get(): return
        if messagebox.askyesno("Confirmar", "Deseja excluir este espaço?"):
            try:
                self.espaco_service.excluir_espaco(int(self.id_espaco_sel.get()))
                self.limpar_espaco(); self.carregar_espacos()
            except Exception: messagebox.showerror("Erro", "Espaço possui agendamentos.")

    # ========================== ABA 4: AGENDAMENTOS (Relacionamento N:N) ==========================
    def setup_tab_agendamentos(self):
        frame_form = ttk.Frame(self.tab_agendamentos)
        frame_form.pack(pady=20, fill="x", padx=20)
        
        ttk.Button(frame_form, text="🔄 Recarregar Dados", command=self.sincronizar_agendamento_combos).grid(row=0, columnspan=4, pady=10)
        
        ttk.Label(frame_form, text="Cliente:").grid(row=1, column=0, sticky="e", padx=5, pady=8)
        self.combo_clientes = ttk.Combobox(frame_form, width=35, state="readonly", font=("Segoe UI", 10))
        self.combo_clientes.grid(row=1, column=1, padx=5, pady=8)
        
        # Uso do Listbox Múltiplo para a Regra de Múltiplos Espaços
        ttk.Label(frame_form, text="Espaços (Ctrl+Clique p/ vários):").grid(row=1, column=2, sticky="ne", padx=5, pady=8)
        frame_list = ttk.Frame(frame_form)
        frame_list.grid(row=1, column=3, rowspan=2, sticky="w", padx=5, pady=8)
        self.list_espacos = tk.Listbox(frame_list, selectmode=tk.MULTIPLE, height=4, width=35, font=("Segoe UI", 10))
        self.list_espacos.pack(side="left", fill="y")
        scroll = ttk.Scrollbar(frame_list, orient="vertical", command=self.list_espacos.yview)
        scroll.pack(side="right", fill="y")
        self.list_espacos.config(yscrollcommand=scroll.set)
        
        ttk.Label(frame_form, text="Data da Reserva:").grid(row=2, column=0, sticky="e", padx=5, pady=8)
        self.entry_data = DateEntry(frame_form, width=15, background='#3498db', foreground='white', borderwidth=0, font=("Segoe UI", 10), date_pattern='yyyy-mm-dd')
        self.entry_data.grid(row=2, column=1, sticky="w", padx=5, pady=8)
        
        # Spinbox (Horas Inteligentes)
        ttk.Label(frame_form, text="Horário:").grid(row=3, column=0, sticky="e", padx=5, pady=8)
        frame_h = ttk.Frame(frame_form)
        frame_h.grid(row=3, column=1, sticky="w", padx=5)
        
        self.spin_ini_h = ttk.Spinbox(frame_h, from_=0, to=23, width=3, format="%02.0f", font=("Segoe UI", 10))
        self.spin_ini_h.pack(side="left"); self.spin_ini_h.set("08")
        ttk.Label(frame_h, text=" : ").pack(side="left")
        self.spin_ini_m = ttk.Spinbox(frame_h, from_=0, to=59, width=3, format="%02.0f", increment=15, font=("Segoe UI", 10))
        self.spin_ini_m.pack(side="left"); self.spin_ini_m.set("00")
        
        ttk.Label(frame_h, text="   até   ", font=("Segoe UI", 10, "bold")).pack(side="left")
        
        self.spin_fim_h = ttk.Spinbox(frame_h, from_=0, to=23, width=3, format="%02.0f", font=("Segoe UI", 10))
        self.spin_fim_h.pack(side="left"); self.spin_fim_h.set("09")
        ttk.Label(frame_h, text=" : ").pack(side="left")
        self.spin_fim_m = ttk.Spinbox(frame_h, from_=0, to=59, width=3, format="%02.0f", increment=15, font=("Segoe UI", 10))
        self.spin_fim_m.pack(side="left"); self.spin_fim_m.set("00")
        
        frame_btn = ttk.Frame(self.tab_agendamentos)
        frame_btn.pack(pady=10)
        ttk.Button(frame_btn, text="✔ Confirmar Reserva", command=self.salvar_agendamento, style="Sucesso.TButton").pack(side="left", padx=10)
        ttk.Button(frame_btn, text="✖ Cancelar Reserva", command=self.excluir_agendamento, style="Alerta.TButton").pack(side="left", padx=10)
        ttk.Button(frame_btn, text="🔄 Limpar", command=self.limpar_agendamento).pack(side="left", padx=10)

        colunas = ("ID", "Data", "Início", "Fim", "Cliente", "Espaços Ocupados", "Valor Base")
        self.tree_agendamentos = ttk.Treeview(self.tab_agendamentos, columns=colunas, show="headings", height=10)
        for c in colunas: self.tree_agendamentos.heading(c, text=c)
        self.tree_agendamentos.column("ID", width=50, anchor="center")
        self.tree_agendamentos.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree_agendamentos.bind("<ButtonRelease-1>", self.selecionar_agendamento)
        
        self.sincronizar_agendamento_combos()
        self.carregar_agendamentos()

    def sincronizar_agendamento_combos(self):
        try:
            self.combo_clientes['values'] = [f"{c.id_cliente} - {c.nome}" for c in self.cliente_service.listar_clientes()]
            self.list_espacos.delete(0, tk.END)
            for e in self.espaco_service.listar_espacos():
                self.list_espacos.insert(tk.END, f"{e.id_espaco} - {e.nome} (R$ {e.valor_hora:.2f})")
        except Exception: pass

    def carregar_agendamentos(self):
        for item in self.tree_agendamentos.get_children(): self.tree_agendamentos.delete(item)
        try:
            self.reservas_memoria = self.agendamento_service.listar_agendamentos()
            for a in self.reservas_memoria:
                self.tree_agendamentos.insert("", "end", values=(a.id_agendamento, a.data_reserva, a.hora_inicio, a.hora_fim, a.nome_cliente, a.espacos_str, f"R$ {a.valor_total_espacos:.2f}"))
        except Exception: pass

    def selecionar_agendamento(self, event):
        sel = self.tree_agendamentos.selection()
        if sel:
            v = self.tree_agendamentos.item(sel, 'values')
            self.id_agendamento_sel.set(v[0])
            self.entry_data.set_date(v[1])
            
            # Preenche os Spinboxes do relógio
            h_i, m_i = v[2].split(":")[:2]
            h_f, m_f = v[3].split(":")[:2]
            self.spin_ini_h.set(h_i); self.spin_ini_m.set(m_i)
            self.spin_fim_h.set(h_f); self.spin_fim_m.set(m_f)
            
            # Recupera o Cliente na ComboBox
            nome_cliente = v[4]
            for item in self.combo_clientes['values']:
                if nome_cliente in item:
                    self.combo_clientes.set(item)
                    break
                    
            # Recupera os Múltiplos Espaços marcando-os no Listbox
            self.list_espacos.selection_clear(0, tk.END)
            espacos_cadastrados = v[5].split(", ") # Quebra a string "vôlei, SALÃO"
            
            for i in range(self.list_espacos.size()):
                item_texto = self.list_espacos.get(i).lower()
                for espaco in espacos_cadastrados:
                    if espaco.lower() in item_texto:
                        self.list_espacos.selection_set(i) # Destaca a linha visualmente

    def limpar_agendamento(self):
        self.id_agendamento_sel.set("")
        self.combo_clientes.set("")
        self.list_espacos.selection_clear(0, tk.END)
        self.spin_ini_h.set("08"); self.spin_ini_m.set("00")
        self.spin_fim_h.set("09"); self.spin_fim_m.set("00")

    def salvar_agendamento(self):
        selecionados = self.list_espacos.curselection()
        if not self.combo_clientes.get() or not selecionados: 
            messagebox.showwarning("Aviso", "Selecione um Cliente e pelo menos UM Espaço.")
            return
        
        hora_ini = f"{int(self.spin_ini_h.get()):02d}:{int(self.spin_ini_m.get()):02d}"
        hora_fim = f"{int(self.spin_fim_h.get()):02d}:{int(self.spin_fim_m.get()):02d}"
        
        # Pega a lista de IDs de todas as quadras selecionadas
        ids_espacos = []
        for idx in selecionados:
            ids_espacos.append(int(self.list_espacos.get(idx).split(" - ")[0]))
            
        try:
            id_c = int(self.combo_clientes.get().split(" - ")[0])
            
            if self.id_agendamento_sel.get():
                # MODO UPDATE: Se clicou na tabela, atualiza a reserva existente
                self.agendamento_service.atualizar_agendamento(int(self.id_agendamento_sel.get()), self.entry_data.get(), hora_ini, hora_fim, id_c, ids_espacos)
                messagebox.showinfo("Sucesso", "Reserva atualizada no banco de dados!")
            else:
                # MODO INSERT: Se é novo, cria a reserva
                self.agendamento_service.cadastrar_agendamento(self.entry_data.get(), hora_ini, hora_fim, id_c, ids_espacos)
                messagebox.showinfo("Sucesso", "Reserva inserida no SGBD. Horários verificados!")
                
            self.limpar_agendamento()
            self.carregar_agendamentos()
        except Exception as e: 
            messagebox.showerror("Bloqueio SGBD (Trigger)", str(e))

    def excluir_agendamento(self):
        if not self.id_agendamento_sel.get(): return
        if messagebox.askyesno("Confirmar", "Cancelar toda a reserva e liberar os espaços?"):
            try:
                self.agendamento_service.excluir_agendamento(int(self.id_agendamento_sel.get()))
                self.limpar_agendamento(); self.carregar_agendamentos()
            except Exception as e: messagebox.showerror("Erro", str(e))

    # ========================== ABA 5: PAGAMENTOS (Layout Otimizado) ==========================
    def setup_tab_pagamentos(self):
        frame_form = ttk.Frame(self.tab_pagamentos)
        frame_form.pack(pady=20, fill="x", padx=20)
        
        ttk.Button(frame_form, text="🔄 Carregar Reservas do Banco", command=self.sincronizar_reservas_pagto).grid(row=0, columnspan=4, pady=10)
        
        ttk.Label(frame_form, text="Reserva Vinculada:").grid(row=1, column=0, sticky="e", padx=5, pady=8)
        self.combo_reservas = ttk.Combobox(frame_form, width=50, state="readonly", font=("Segoe UI", 10))
        self.combo_reservas.grid(row=1, column=1, columnspan=3, padx=5, pady=8, sticky="w")
        
        ttk.Label(frame_form, text="Valor Final a Pagar (R$):").grid(row=2, column=0, sticky="e", padx=5, pady=8)
        self.entry_val_pag = ttk.Entry(frame_form, width=15, font=("Segoe UI", 10))
        self.entry_val_pag.grid(row=2, column=1, sticky="w", padx=5, pady=8)
        
        ttk.Label(frame_form, text="Método de Pagamento:").grid(row=2, column=2, sticky="e", padx=5, pady=8)
        self.forma_var = tk.StringVar(value="PIX")
        fr_rad = ttk.Frame(frame_form)
        fr_rad.grid(row=2, column=3, sticky="w")
        ttk.Radiobutton(fr_rad, text="PIX", variable=self.forma_var, value="PIX").pack(side="left", padx=5)
        ttk.Radiobutton(fr_rad, text="Cartão de Crédito", variable=self.forma_var, value="CARTAO").pack(side="left", padx=5)
        
        ttk.Label(frame_form, text="Status Financeiro:").grid(row=3, column=0, sticky="e", padx=5, pady=8)
        self.combo_status = ttk.Combobox(frame_form, values=["Pendente", "Pago", "Cancelado"], width=15, state="readonly")
        self.combo_status.grid(row=3, column=1, sticky="w", padx=5, pady=8)
        self.combo_status.set("Pendente")
        
        ttk.Label(frame_form, text="Nº Cartão (Apenas Crédito):").grid(row=3, column=2, sticky="e", padx=5, pady=8)
        self.entry_cartao = ttk.Entry(frame_form, width=22)
        self.entry_cartao.grid(row=3, column=3, sticky="w", padx=5, pady=8)
        
        frame_btn = ttk.Frame(self.tab_pagamentos)
        frame_btn.pack(pady=10)
        ttk.Button(frame_btn, text="💳 Finalizar Transação", command=self.salvar_pagamento, style="Sucesso.TButton").pack(side="left", padx=10)
        ttk.Button(frame_btn, text="✖ Excluir Histórico", command=self.excluir_pagamento, style="Alerta.TButton").pack(side="left", padx=10)
        ttk.Button(frame_btn, text="🔄 Limpar", command=self.limpar_pagamento).pack(side="left", padx=10)

        # Nova Ordem das Colunas: Foco nos dados essenciais do usuário e transação no fim
        colunas = ("ID", "Cliente", "Espaços da Reserva", "Valor Pago", "Método", "Status", "Nº da Transação", "id_a")
        self.tree_pagamentos = ttk.Treeview(self.tab_pagamentos, columns=colunas, show="headings", height=10)
        
        larguras = {"ID": 40, "Cliente": 160, "Espaços da Reserva": 180, "Valor Pago": 100, "Método": 100, "Status": 100, "Nº da Transação": 250, "id_a": 0}
        
        for c in colunas: 
            self.tree_pagamentos.heading(c, text=c)
            ancoramento = "center" if c in ("ID", "Valor Pago", "Status", "Método") else "w"
            self.tree_pagamentos.column(c, width=larguras[c], anchor=ancoramento)
            
        self.tree_pagamentos.column("id_a", width=0, stretch=False)
        self.tree_pagamentos.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree_pagamentos.bind("<ButtonRelease-1>", self.selecionar_pagamento)
        
        self.sincronizar_reservas_pagto()
        self.carregar_pagamentos()

    def sincronizar_reservas_pagto(self):
        try:
            self.combo_reservas['values'] = [f"{r.id_agendamento} - {r.nome_cliente} | Total calculado: R$ {r.valor_total_espacos:.2f}" for r in self.reservas_memoria]
            self.combo_reservas.bind("<<ComboboxSelected>>", self.auto_preencher_valor)
        except Exception: pass

    def auto_preencher_valor(self, event):
        sel = self.combo_reservas.get()
        if sel:
            valor_calculado = sel.split("R$ ")[1]
            self.entry_val_pag.delete(0, tk.END)
            self.entry_val_pag.insert(0, valor_calculado)

    def carregar_pagamentos(self):
        for item in self.tree_pagamentos.get_children(): self.tree_pagamentos.delete(item)
        try:
            for p in self.pagamento_service.listar_pagamentos():
                detalhe = p["chave_pix"] if p["forma_pagamento"] == "PIX" else p["final_cartao"]
                # Inserção na nova ordem para facilitar a leitura do usuário
                self.tree_pagamentos.insert("", "end", values=(
                    p["id_pagamento"], 
                    p["cliente"], 
                    p["espaco"], 
                    f"R$ {p['valor_total']:.2f}", 
                    p["forma_pagamento"], 
                    p["status"], 
                    detalhe, 
                    p["id_agendamento"]
                ))
        except Exception: pass

    def selecionar_pagamento(self, event):
        sel = self.tree_pagamentos.selection()
        if sel:
            v = self.tree_pagamentos.item(sel, 'values')
            self.id_pagamento_sel.set(v[0])
            
            # Recupera os dados baseando-se nas novas posições das colunas
            self.entry_val_pag.delete(0, tk.END)
            self.entry_val_pag.insert(0, v[3].replace("R$ ", ""))
            
            self.forma_var.set(v[4])
            self.combo_status.set(v[5])
            
            for item in self.combo_reservas['values']:
                if item.startswith(str(v[7])): 
                    self.combo_reservas.set(item)
                    break

    def limpar_pagamento(self):
        self.id_pagamento_sel.set("")
        self.entry_val_pag.delete(0, tk.END); self.entry_cartao.delete(0, tk.END)
        self.combo_reservas.set(""); self.combo_status.set("Pendente")

    def salvar_pagamento(self):
        if not self.combo_reservas.get() or not self.entry_val_pag.get(): 
            messagebox.showwarning("Aviso", "Selecione a reserva e confira o valor.")
            return
            
        try:
            id_a = int(self.combo_reservas.get().split(" - ")[0])
            v_tot = float(self.entry_val_pag.get().replace(",", "."))
            forma = self.forma_var.get()
            
            if self.id_pagamento_sel.get():
                self.pagamento_service.atualizar_pagamento(int(self.id_pagamento_sel.get()), forma, v_tot, id_a, self.combo_status.get(), "")
            else:
                self.pagamento_service.processar_pagamento(forma, v_tot, id_a, numero_cartao=self.entry_cartao.get())
            
            self.limpar_pagamento()
            self.carregar_pagamentos()
            messagebox.showinfo("Sucesso", f"Transação finalizada com sucesso via {forma}!")
        except Exception as e: messagebox.showerror("Validação da Transação", str(e))

    def excluir_pagamento(self):
        if not self.id_pagamento_sel.get(): return
        if messagebox.askyesno("Confirmar", "Deseja apagar este registro financeiro?"):
            self.pagamento_service.excluir_pagamento(int(self.id_pagamento_sel.get()))
            self.limpar_pagamento(); self.carregar_pagamentos()