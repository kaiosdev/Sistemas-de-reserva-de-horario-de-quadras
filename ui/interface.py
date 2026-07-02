import tkinter as tk
from tkinter import ttk, messagebox
import re
from services.cliente_service import ClienteService
from services.espaco_service import EspacoService
from services.agendamento_service import AgendamentoService
from services.pagamento_service import PagamentoService

class AthletixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Athletix - Gestao Esportiva (CRUD Integrado)")
        self.root.geometry("900x600")
        
        self.cliente_service = ClienteService()
        self.espaco_service = EspacoService()
        self.agendamento_service = AgendamentoService()
        self.pagamento_service = PagamentoService()
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_clientes = ttk.Frame(self.notebook)
        self.tab_espacos = ttk.Frame(self.notebook)
        self.tab_agendamentos = ttk.Frame(self.notebook)
        self.tab_pagamentos = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_clientes, text="1. Clientes")
        self.notebook.add(self.tab_espacos, text="2. Espacos")
        self.notebook.add(self.tab_agendamentos, text="3. Agendamentos")
        self.notebook.add(self.tab_pagamentos, text="4. Pagamentos")
        
        self.id_cliente_sel = tk.StringVar()
        self.id_espaco_sel = tk.StringVar()
        self.id_agendamento_sel = tk.StringVar()
        self.id_pagamento_sel = tk.StringVar()
        
        self.setup_tab_clientes()
        self.setup_tab_espacos()
        self.setup_tab_agendamentos()
        self.setup_tab_pagamentos()

    # ========================== ABA 1: CLIENTES (CRUD) ==========================
    def setup_tab_clientes(self):
        frame_form = tk.Frame(self.tab_clientes)
        frame_form.pack(pady=10, fill="x", padx=10)
        
        tk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky="e")
        self.entry_nome_cli = tk.Entry(frame_form, width=25)
        self.entry_nome_cli.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(frame_form, text="CPF:").grid(row=0, column=2, sticky="e")
        self.entry_cpf_cli = tk.Entry(frame_form, width=15)
        self.entry_cpf_cli.grid(row=0, column=3, padx=5, pady=2)
        
        tk.Label(frame_form, text="Endereco:").grid(row=1, column=0, sticky="e")
        self.entry_end_cli = tk.Entry(frame_form, width=25)
        self.entry_end_cli.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(frame_form, text="Telefone:").grid(row=1, column=2, sticky="e")
        self.entry_tel_cli = tk.Entry(frame_form, width=15)
        self.entry_tel_cli.grid(row=1, column=3, padx=5, pady=2)
        
        frame_btn = tk.Frame(self.tab_clientes)
        frame_btn.pack(pady=5)
        tk.Button(frame_btn, text="Salvar Cliente", command=self.salvar_cliente, bg="lightblue").pack(side="left", padx=5)
        tk.Button(frame_btn, text="Excluir Cliente", command=self.excluir_cliente, bg="salmon").pack(side="left", padx=5)
        tk.Button(frame_btn, text="Limpar", command=self.limpar_cliente).pack(side="left", padx=5)

        colunas = ("ID", "Nome", "CPF", "Endereco", "Telefone")
        self.tree_clientes = ttk.Treeview(self.tab_clientes, columns=colunas, show="headings", height=12)
        for c in colunas: self.tree_clientes.heading(c, text=c); self.tree_clientes.column(c, width=150)
        self.tree_clientes.column("ID", width=50)
        self.tree_clientes.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree_clientes.bind("<ButtonRelease-1>", self.selecionar_cliente)
        self.carregar_clientes()

    def carregar_clientes(self):
        for item in self.tree_clientes.get_children(): self.tree_clientes.delete(item)
        for c in self.cliente_service.listar_clientes():
            self.tree_clientes.insert("", "end", values=(c.id_cliente, c.nome, c.cpf, c.endereco, c.telefone))

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
        t = f"{self.entry_nome_cli.get()};{self.entry_cpf_cli.get()};{self.entry_end_cli.get()};{self.entry_tel_cli.get()}"
        try:
            if self.id_cliente_sel.get():
                self.cliente_service.atualizar_cliente(int(self.id_cliente_sel.get()), t)
            else:
                self.cliente_service.cadastrar_cliente_texto(t)
            self.limpar_cliente(); self.carregar_clientes()
        except Exception as e: messagebox.showerror("Erro", str(e))

    def excluir_cliente(self):
        if not self.id_cliente_sel.get(): return
        try:
            self.cliente_service.excluir_cliente(int(self.id_cliente_sel.get()))
            self.limpar_cliente(); self.carregar_clientes()
        except Exception: messagebox.showerror("Erro Relacional", "Cliente possui agendamentos ativos.")

    # ========================== ABA 2: ESPAÇOS (CRUD) ==========================
    def setup_tab_espacos(self):
        frame_form = tk.Frame(self.tab_espacos)
        frame_form.pack(pady=10, fill="x", padx=10)
        
        tk.Label(frame_form, text="Nome Quadra:").grid(row=0, column=0, sticky="e")
        self.entry_nome_esp = tk.Entry(frame_form, width=25)
        self.entry_nome_esp.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(frame_form, text="Valor/Hora:").grid(row=0, column=2, sticky="e")
        self.entry_val_esp = tk.Entry(frame_form, width=15)
        self.entry_val_esp.grid(row=0, column=3, padx=5, pady=2)
        
        tk.Label(frame_form, text="Dimensao:").grid(row=1, column=0, sticky="e")
        self.entry_tam_esp = tk.Entry(frame_form, width=25)
        self.entry_tam_esp.grid(row=1, column=1, padx=5, pady=2)
        
        frame_btn = tk.Frame(self.tab_espacos)
        frame_btn.pack(pady=5)
        tk.Button(frame_btn, text="Salvar Espaco", command=self.salvar_espaco, bg="lightblue").pack(side="left", padx=5)
        tk.Button(frame_btn, text="Excluir Espaco", command=self.excluir_espaco, bg="salmon").pack(side="left", padx=5)
        tk.Button(frame_btn, text="Limpar", command=self.limpar_espaco).pack(side="left", padx=5)

        colunas = ("ID", "Nome", "Dimensao", "Valor/Hora")
        self.tree_espacos = ttk.Treeview(self.tab_espacos, columns=colunas, show="headings", height=12)
        for c in colunas: self.tree_espacos.heading(c, text=c); self.tree_espacos.column(c, width=180)
        self.tree_espacos.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree_espacos.bind("<ButtonRelease-1>", self.selecionar_espaco)
        self.carregar_espacos()

    def carregar_espacos(self):
        for item in self.tree_espacos.get_children(): self.tree_espacos.delete(item)
        for e in self.espaco_service.listar_espacos():
            self.tree_espacos.insert("", "end", values=(e.id_espaco, e.nome, e.tamanho_quadra, f"{e.valor_hora:.2f}"))

    def selecionar_espaco(self, event):
        sel = self.tree_espacos.selection()
        if sel:
            v = self.tree_espacos.item(sel, 'values')
            self.id_espaco_sel.set(v[0])
            self.entry_nome_esp.delete(0, tk.END); self.entry_nome_esp.insert(0, v[1])
            self.entry_tam_esp.delete(0, tk.END); self.entry_tam_esp.insert(0, v[2])
            self.entry_val_esp.delete(0, tk.END); self.entry_val_esp.insert(0, v[3])

    def limpar_espaco(self):
        self.id_espaco_sel.set("")
        self.entry_nome_esp.delete(0, tk.END); self.entry_tam_esp.delete(0, tk.END); self.entry_val_esp.delete(0, tk.END)

    def salvar_espaco(self):
        try:
            if self.id_espaco_sel.get():
                self.espaco_service.atualizar_espaco(int(self.id_espaco_sel.get()), self.entry_nome_esp.get(), "Quadra", self.entry_tam_esp.get(), self.entry_val_esp.get())
            else:
                self.espaco_service.cadastrar_espaco(self.entry_nome_esp.get(), "Quadra", self.entry_tam_esp.get(), self.entry_val_esp.get())
            self.limpar_espaco(); self.carregar_espacos()
        except Exception as e: messagebox.showerror("Erro", str(e))

    def excluir_espaco(self):
        if not self.id_espaco_sel.get(): return
        try:
            self.espaco_service.excluir_espaco(int(self.id_espaco_sel.get()))
            self.limpar_espaco(); self.carregar_espacos()
        except Exception: messagebox.showerror("Erro Relacional", "Espaco possui agendamentos vinculados.")

    # ========================== ABA 3: AGENDAMENTOS (CRUD) ==========================
    def setup_tab_agendamentos(self):
        frame_form = tk.Frame(self.tab_agendamentos)
        frame_form.pack(pady=10, fill="x", padx=10)
        
        tk.Button(frame_form, text="🔄 Atualizar Listas Suspenses", command=self.sincronizar_combos).grid(row=0, columnspan=4, pady=5)
        
        tk.Label(frame_form, text="Cliente:").grid(row=1, column=0, sticky="e")
        self.combo_clientes = ttk.Combobox(frame_form, width=25, state="readonly")
        self.combo_clientes.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(frame_form, text="Espaco:").grid(row=1, column=2, sticky="e")
        self.combo_espacos = ttk.Combobox(frame_form, width=25, state="readonly")
        self.combo_espacos.grid(row=1, column=3, padx=5, pady=2)
        
        tk.Label(frame_form, text="Data (AAAA-MM-DD):").grid(row=2, column=0, sticky="e")
        self.entry_data = tk.Entry(frame_form, width=15)
        self.entry_data.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        
        tk.Label(frame_form, text="Inicio / Fim (HH:MM):").grid(row=2, column=2, sticky="e")
        frame_h = tk.Frame(frame_form)
        frame_h.grid(row=2, column=3, sticky="w", padx=5)
        self.entry_ini = tk.Entry(frame_h, width=7); self.entry_ini.pack(side="left")
        tk.Label(frame_h, text=" as ").pack(side="left")
        self.entry_fim = tk.Entry(frame_h, width=7); self.entry_fim.pack(side="left")
        
        frame_btn = tk.Frame(self.tab_agendamentos)
        frame_btn.pack(pady=5)
        tk.Button(frame_btn, text="Salvar Agendamento", command=self.salvar_agendamento, bg="lightblue").pack(side="left", padx=5)
        tk.Button(frame_btn, text="Excluir Agendamento", command=self.excluir_agendamento, bg="salmon").pack(side="left", padx=5)
        tk.Button(frame_btn, text="Limpar", command=self.limpar_agendamento).pack(side="left", padx=5)

        colunas = ("ID", "Data", "Inicio", "Fim", "Cliente", "Espaco", "id_c", "id_e")
        self.tree_agendamentos = ttk.Treeview(self.tab_agendamentos, columns=colunas, show="headings", height=10)
        for c in colunas: self.tree_agendamentos.heading(c, text=c); self.tree_agendamentos.column(c, width=120)
        self.tree_agendamentos.column("id_c", width=0, stretch=False); self.tree_agendamentos.column("id_e", width=0, stretch=False)
        self.tree_agendamentos.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree_agendamentos.bind("<ButtonRelease-1>", self.selecionar_agendamento)
        self.sincronizar_combos()
        self.carregar_agendamentos()

    def sincronizar_combos(self):
        self.combo_clientes['values'] = [f"{c.id_cliente} - {c.nome}" for c in self.cliente_service.listar_clientes()]
        self.combo_espacos['values'] = [f"{e.id_espaco} - {e.nome}" for e in self.espaco_service.listar_espacos()]

    def carregar_agendamentos(self):
        for item in self.tree_agendamentos.get_children(): self.tree_agendamentos.delete(item)
        for a in self.agendamento_service.listar_agendamentos():
            self.tree_agendamentos.insert("", "end", values=(a.id_agendamento, a.data_reserva, a.hora_inicio, a.hora_fim, a.nome_cliente, a.nome_espaco, a.id_cliente, a.id_espaco))

    def selecionar_agendamento(self, event):
        sel = self.tree_agendamentos.selection()
        if sel:
            v = self.tree_agendamentos.item(sel, 'values')
            self.id_agendamento_sel.set(v[0])
            self.entry_data.delete(0, tk.END); self.entry_data.insert(0, v[1])
            self.entry_ini.delete(0, tk.END); self.entry_ini.insert(0, v[2])
            self.entry_fim.delete(0, tk.END); self.entry_fim.insert(0, v[3])
            
            for item in self.combo_clientes['values']:
                if item.startswith(str(v[6])): self.combo_clientes.set(item); break
            for item in self.combo_espacos['values']:
                if item.startswith(str(v[7])): self.combo_espacos.set(item); break

    def limpar_agendamento(self):
        self.id_agendamento_sel.set("")
        self.entry_data.delete(0, tk.END); self.entry_ini.delete(0, tk.END); self.entry_fim.delete(0, tk.END)
        self.combo_clientes.set(""); self.combo_espacos.set("")

    def salvar_agendamento(self):
        if not all([self.combo_clientes.get(), self.combo_espacos.get(), self.entry_data.get(), self.entry_ini.get(), self.entry_fim.get()]): return
        try:
            id_c = int(self.combo_clientes.get().split(" - ")[0])
            id_e = int(self.combo_espacos.get().split(" - ")[0])
            if self.id_agendamento_sel.get():
                self.agendamento_service.atualizar_agendamento(int(self.id_agendamento_sel.get()), self.entry_data.get(), self.entry_ini.get(), self.entry_fim.get(), id_c, id_e)
            else:
                self.agendamento_service.cadastrar_agendamento(self.entry_data.get(), self.entry_ini.get(), self.entry_fim.get(), id_c, id_e)
            self.limpar_agendamento(); self.carregar_agendamentos()
        except Exception as e: messagebox.showerror("Bloqueio por Regra (Trigger)", str(e))

    def excluir_agendamento(self):
        if not self.id_agendamento_sel.get(): return
        self.agendamento_service.excluir_agendamento(int(self.id_agendamento_sel.get()))
        self.limpar_agendamento(); self.carregar_agendamentos()

    # ========================== ABA 4: PAGAMENTOS (CRUD) ==========================
    def setup_tab_pagamentos(self):
        frame_form = tk.Frame(self.tab_pagamentos)
        frame_form.pack(pady=10, fill="x", padx=10)
        
        tk.Button(frame_form, text="🔄 Sincronizar Reservas Pendentes", command=self.sincronizar_reservas_pagto).grid(row=0, columnspan=4, pady=5)
        
        tk.Label(frame_form, text="Reserva:").grid(row=1, column=0, sticky="e")
        self.combo_reservas = ttk.Combobox(frame_form, width=40, state="readonly")
        self.combo_reservas.grid(row=1, column=1, columnspan=3, padx=5, pady=2, sticky="w")
        
        tk.Label(frame_form, text="Valor:").grid(row=2, column=0, sticky="e")
        self.entry_val_pag = tk.Entry(frame_form, width=15)
        self.entry_val_pag.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        
        tk.Label(frame_form, text="Forma:").grid(row=2, column=2, sticky="e")
        self.forma_var = tk.StringVar(value="PIX")
        fr_rad = tk.Frame(frame_form)
        fr_rad.grid(row=2, column=3, sticky="w")
        tk.Radiobutton(fr_rad, text="PIX", variable=self.forma_var, value="PIX").pack(side="left")
        tk.Radiobutton(fr_rad, text="Cartao", variable=self.forma_var, value="CARTAO").pack(side="left")
        
        tk.Label(frame_form, text="Status / Cartao (ou Pix):").grid(row=3, column=0, sticky="e")
        self.combo_status = ttk.Combobox(frame_form, values=["Pendente", "Pago", "Cancelado"], width=12, state="readonly")
        self.combo_status.grid(row=3, column=1, sticky="w", padx=5, pady=2)
        self.combo_status.set("Pendente")
        
        self.entry_detalhe = tk.Entry(frame_form, width=25)
        self.entry_detalhe.grid(row=3, column=2, columnspan=2, sticky="w", padx=5, pady=2)
        
        frame_btn = tk.Frame(self.tab_pagamentos)
        frame_btn.pack(pady=5)
        tk.Button(frame_btn, text="Processar / Atualizar", command=self.salvar_pagamento, bg="lightblue").pack(side="left", padx=5)
        tk.Button(frame_btn, text="Excluir Registro", command=self.excluir_pagamento, bg="salmon").pack(side="left", padx=5)
        tk.Button(frame_btn, text="Limpar", command=self.limpar_pagamento).pack(side="left", padx=5)

        colunas = ("ID", "Valor", "Forma", "Status", "Chave/Final", "Cliente", "Espaco", "id_a")
        self.tree_pagamentos = ttk.Treeview(self.tab_pagamentos, columns=colunas, show="headings", height=10)
        for c in colunas: self.tree_pagamentos.heading(c, text=c); self.tree_pagamentos.column(c, width=110)
        self.tree_pagamentos.column("id_a", width=0, stretch=False)
        self.tree_pagamentos.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree_pagamentos.bind("<ButtonRelease-1>", self.selecionar_pagamento)
        self.sincronizar_reservas_pagto()
        self.carregar_pagamentos()

    def sincronizar_reservas_pagto(self):
        self.combo_reservas['values'] = [f"{r.id_agendamento} - {r.nome_cliente} ({r.data_reserva})" for r in self.agendamento_service.listar_agendamentos()]

    def carregar_pagamentos(self):
        for item in self.tree_pagamentos.get_children(): self.tree_pagamentos.delete(item)
        for p in self.pagamento_service.listar_pagamentos():
            detalhe = p["chave_pix"] if p["forma_pagamento"] == "PIX" else p["final_cartao"]
            self.tree_pagamentos.insert("", "end", values=(p["id_pagamento"], f"R$ {p['valor_total']:.2f}", p["forma_pagamento"], p["status"], detalhe, p["cliente"], p["espaco"], p["id_agendamento"]))

    def selecionar_pagamento(self, event):
        sel = self.tree_pagamentos.selection()
        if sel:
            v = self.tree_pagamentos.item(sel, 'values')
            self.id_pagamento_sel.set(v[0])
            self.entry_val_pag.delete(0, tk.END); self.entry_val_pag.insert(0, v[1].replace("R$ ", ""))
            self.forma_var.set(v[2])
            self.combo_status.set(v[3])
            self.entry_detalhe.delete(0, tk.END); self.entry_detalhe.insert(0, v[4] if v[4] != "None" else "")
            
            for item in self.combo_reservas['values']:
                if item.startswith(str(v[7])): self.combo_reservas.set(item); break

    def limpar_pagamento(self):
        self.id_pagamento_sel.set("")
        self.entry_val_pag.delete(0, tk.END); self.entry_detalhe.delete(0, tk.END)
        self.combo_reservas.set(""); self.combo_status.set("Pendente")

    def salvar_pagamento(self):
        if not self.combo_reservas.get() or not self.entry_val_pag.get(): return
        try:
            id_a = int(self.combo_reservas.get().split(" - ")[0])
            v_tot = float(self.entry_val_pag.get())
            forma = self.forma_var.get()
            
            if self.id_pagamento_sel.get():
                self.pagamento_service.atualizar_pagamento(int(self.id_pagamento_sel.get()), forma, v_tot, id_a, self.combo_status.get(), self.entry_detalhe.get())
            else:
                # Dispara o Polimorfismo Real (Algoritmo de Luhn ou Hash Pix) antes de salvar
                self.pagamento_service.processar_pagamento(forma, v_tot, id_a, numero_cartao=self.entry_detalhe.get())
            
            self.limpar_pagamento(); self.carregar_pagamentos()
        except Exception as e: messagebox.showerror("Validacao de POO", str(e))

    def excluir_pagamento(self):
        if not self.id_pagamento_sel.get(): return
        self.pagamento_service.excluir_pagamento(int(self.id_pagamento_sel.get()))
        self.limpar_pagamento(); self.carregar_pagamentos()