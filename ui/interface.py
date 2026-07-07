import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from services.cliente_service import ClienteService
from repositories.espaco_repository import EspacoRepository
from repositories.agendamento_repository import AgendamentoRepository
from repositories.pagamento_repository import PagamentoRepository
from models.espaco import Espaco
from models.agendamento import Agendamento

# Tema dark moderno alinhado ao design system do frontend web
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class AthletixApp:
    """Interface desktop moderna (CustomTkinter) do Athletix.

    Fluxo de gestao: Espacos -> Clientes -> Agendamentos -> Pagamentos.
    Acesso direto aos repositories (sem passar pela API Flask).
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Athletix - Gestao Esportiva")
        self.root.geometry("960x620")
        self.root.minsize(820, 560)

        self.cliente_service = ClienteService()
        self.espaco_repo = EspacoRepository()
        self.agendamento_repo = AgendamentoRepository()
        self.pagamento_repo = PagamentoRepository()

        self._build_layout()

        self.tab_espacos_id = self.tabview.add("1. Espacos")
        self.tab_clientes_id = self.tabview.add("2. Clientes")
        self.tab_agendamentos_id = self.tabview.add("3. Agendamentos")
        self.tab_pagamentos_id = self.tabview.add("4. Pagamentos")

        self._setup_tab_espacos()
        self._setup_tab_clientes()
        self._setup_tab_agendamentos()
        self._setup_tab_pagamentos()

        # Carrega listagens iniciais
        self._atualizar_lista_espacos()
        self._atualizar_lista_clientes()
        self._atualizar_lista_agendamentos()
        self._atualizar_lista_pagamentos()

    # ------------------------------------------------------------------
    # LAYOUT BASE
    # ------------------------------------------------------------------
    def _build_layout(self):
        # Cabecalho com marca
        header = ctk.CTkFrame(self.root, corner_radius=0, fg_color=("gray92", "#0f1421"))
        header.pack(fill="x")

        ctk.CTkLabel(
            header, text="🏆  ATHLETIX",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#0f1421", "#00e676"),
        ).pack(side="left", padx=24, pady=18)

        ctk.CTkLabel(
            header, text="Sistema de Gestao de Espacos Esportivos",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=8)

        # Container de abas
        self.tabview = ctk.CTkTabview(
            self.root,
            segmented_button_fg_color=("#e5e7eb", "#161c2d"),
            segmented_button_selected_color=("#00c853", "#00e676"),
            segmented_button_selected_hover_color=("#00b248", "#00c853"),
        )
        self.tabview.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    # ------------------------------------------------------------------
    # TAB: ESPACOS
    # ------------------------------------------------------------------
    def _setup_tab_espacos(self):
        tab = self.tab_espacos_id

        form = ctk.CTkFrame(tab)
        form.pack(fill="x", padx=14, pady=14)

        ctk.CTkLabel(
            form, text="Cadastro de Quadras",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(anchor="w", padx=14, pady=(12, 4))

        campos = ctk.CTkFrame(form, fg_color="transparent")
        campos.pack(fill="x", padx=14, pady=(0, 8))

        self.ent_nome_quadra = ctk.CTkEntry(campos, placeholder_text="Nome da quadra", width=260)
        self.ent_nome_quadra.grid(row=0, column=0, padx=6, pady=6, sticky="ew")

        self.ent_valor_quadra = ctk.CTkEntry(campos, placeholder_text="Valor/hora (R$)", width=140)
        self.ent_valor_quadra.grid(row=0, column=1, padx=6, pady=6)

        self.ent_tamanho_quadra = ctk.CTkEntry(campos, placeholder_text="Tamanho (Oficial)", width=160)
        self.ent_tamanho_quadra.grid(row=0, column=2, padx=6, pady=6)
        self.ent_tamanho_quadra.insert(0, "Oficial")

        campos.columnconfigure(0, weight=1)

        ctk.CTkButton(form, text="Salvar espaco", command=self._salvar_espaco).pack(anchor="w", padx=14, pady=(0, 12))

        # Lista
        ctk.CTkLabel(tab, text="Quadras cadastradas", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=14)
        self.lista_espacos = ctk.CTkTextbox(tab, height=200, font=ctk.CTkFont(size=13))
        self.lista_espacos.pack(fill="both", expand=True, padx=14, pady=(4, 14))

    def _salvar_espaco(self):
        nome = self.ent_nome_quadra.get().strip()
        valor = self.ent_valor_quadra.get().strip()
        tamanho = self.ent_tamanho_quadra.get().strip() or "Oficial"
        if not nome or not valor:
            messagebox.showwarning("Aviso", "Preencha o nome e o valor da quadra.")
            return
        try:
            novo = Espaco(0, nome, "Quadra Poliesportiva", tamanho, float(valor))
            self.espaco_repo.inserir(novo)
            messagebox.showinfo("Sucesso", "Espaco cadastrado.")
            self.ent_nome_quadra.delete(0, tk.END)
            self.ent_valor_quadra.delete(0, tk.END)
            self._atualizar_lista_espacos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _atualizar_lista_espacos(self):
        self.lista_espacos.delete("1.0", tk.END)
        try:
            espacos = self.espaco_repo.listar_todos()
        except Exception as e:
            self.lista_espacos.insert(tk.END, f"Erro ao carregar: {e}")
            return
        if not espacos:
            self.lista_espacos.insert(tk.END, "Nenhum espaco cadastrado.")
            return
        for e in espacos:
            self.lista_espacos.insert(
                tk.END,
                f"#{e.id_espaco}  {e.nome}  |  {e.tamanho_quadra}  |  R$ {e.valor_hora:.2f}/h\n"
            )

    # ------------------------------------------------------------------
    # TAB: CLIENTES
    # ------------------------------------------------------------------
    def _setup_tab_clientes(self):
        tab = self.tab_clientes_id

        form = ctk.CTkFrame(tab)
        form.pack(fill="x", padx=14, pady=14)

        ctk.CTkLabel(form, text="Gestao de Clientes", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=14, pady=(12, 4))

        grid = ctk.CTkFrame(form, fg_color="transparent")
        grid.pack(fill="x", padx=14, pady=(0, 8))

        self.ent_cli_nome = ctk.CTkEntry(grid, placeholder_text="Nome completo", width=240)
        self.ent_cli_nome.grid(row=0, column=0, padx=6, pady=6, sticky="ew")
        self.ent_cli_cpf = ctk.CTkEntry(grid, placeholder_text="CPF (11 digitos)", width=160)
        self.ent_cli_cpf.grid(row=0, column=1, padx=6, pady=6)
        self.ent_cli_tel = ctk.CTkEntry(grid, placeholder_text="Telefone", width=150)
        self.ent_cli_tel.grid(row=1, column=0, padx=6, pady=6, sticky="ew")
        self.ent_cli_end = ctk.CTkEntry(grid, placeholder_text="Endereco", width=300)
        self.ent_cli_end.grid(row=1, column=1, padx=6, pady=6, columnspan=2, sticky="ew")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(2, weight=1)

        ctk.CTkButton(form, text="Cadastrar cliente", command=self._cadastrar_cliente).pack(anchor="w", padx=14, pady=(0, 12))

        ctk.CTkLabel(tab, text="Clientes cadastrados", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=14)
        self.lista_clientes = ctk.CTkTextbox(tab, height=180, font=ctk.CTkFont(size=13))
        self.lista_clientes.pack(fill="both", expand=True, padx=14, pady=(4, 14))

    def _cadastrar_cliente(self):
        nome = self.ent_cli_nome.get().strip()
        cpf = self.ent_cli_cpf.get().strip()
        tel = self.ent_cli_tel.get().strip() or "Nao informado"
        end = self.ent_cli_end.get().strip()
        if not nome or not cpf:
            messagebox.showwarning("Aviso", "Preencha nome e CPF.")
            return
        try:
            # Reaproveita a factory de texto usada pelo service
            texto = f"0, {nome}, {cpf}, {end}, {tel}"
            self.cliente_service.cadastrar_cliente_texto(texto)
            messagebox.showinfo("Sucesso", "Cliente cadastrado.")
            for e in (self.ent_cli_nome, self.ent_cli_cpf, self.ent_cli_tel, self.ent_cli_end):
                e.delete(0, tk.END)
            self._atualizar_lista_clientes()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _atualizar_lista_clientes(self):
        self.lista_clientes.delete("1.0", tk.END)
        try:
            clientes = self.cliente_service.listar_clientes()
        except Exception as e:
            self.lista_clientes.insert(tk.END, f"Erro ao carregar: {e}")
            return
        if not clientes:
            self.lista_clientes.insert(tk.END, "Nenhum cliente cadastrado.")
            return
        for c in clientes:
            self.lista_clientes.insert(
                tk.END,
                f"#{c.id_cliente}  {c.nome}  |  CPF: {c.cpf}  |  Tel: {c.telefone}  |  {c.endereco}\n"
            )

    # ------------------------------------------------------------------
    # TAB: AGENDAMENTOS
    # ------------------------------------------------------------------
    def _setup_tab_agendamentos(self):
        tab = self.tab_agendamentos_id

        form = ctk.CTkFrame(tab)
        form.pack(fill="x", padx=14, pady=14)

        ctk.CTkLabel(form, text="Reserva de Horarios", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=14, pady=(12, 4))

        botoes = ctk.CTkFrame(form, fg_color="transparent")
        botoes.pack(fill="x", padx=14, pady=(0, 8))
        ctk.CTkButton(botoes, text="Carregar dados", command=self._carregar_dados_agendamento).pack(side="left")

        grid = ctk.CTkFrame(form, fg_color="transparent")
        grid.pack(fill="x", padx=14, pady=(0, 8))

        self.combo_clientes = ctk.CTkComboBox(grid, width=260, state="readonly")
        self.combo_clientes.grid(row=0, column=0, padx=6, pady=6, sticky="ew")
        self.combo_espacos = ctk.CTkComboBox(grid, width=260, state="readonly")
        self.combo_espacos.grid(row=0, column=1, padx=6, pady=6, sticky="ew")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        grid2 = ctk.CTkFrame(form, fg_color="transparent")
        grid2.pack(fill="x", padx=14, pady=(0, 8))
        self.ent_data = ctk.CTkEntry(grid2, placeholder_text="Data (AAAA-MM-DD)", width=180)
        self.ent_data.grid(row=0, column=0, padx=6, pady=6)
        self.ent_hora_inicio = ctk.CTkEntry(grid2, placeholder_text="Inicio (HH:MM)", width=140)
        self.ent_hora_inicio.grid(row=0, column=1, padx=6, pady=6)
        self.ent_hora_fim = ctk.CTkEntry(grid2, placeholder_text="Fim (HH:MM)", width=140)
        self.ent_hora_fim.grid(row=0, column=2, padx=6, pady=6)

        ctk.CTkButton(form, text="Confirmar agendamento", command=self._confirmar_agendamento).pack(anchor="w", padx=14, pady=(0, 12))

        ctk.CTkLabel(tab, text="Agendamentos", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=14)
        self.lista_agendamentos = ctk.CTkTextbox(tab, height=160, font=ctk.CTkFont(size=13))
        self.lista_agendamentos.pack(fill="both", expand=True, padx=14, pady=(4, 14))

    def _carregar_dados_agendamento(self):
        try:
            clientes = self.cliente_service.listar_clientes()
            espacos = self.espaco_repo.listar_todos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados:\n{e}")
            return
        self.combo_clientes.configure(values=[f"{c.id_cliente} - {c.nome}" for c in clientes])
        self.combo_espacos.configure(values=[f"{e.id_espaco} - {e.nome}" for e in espacos])
        if clientes:
            self.combo_clientes.set(clientes[0].__class__.__name__ and f"{clientes[0].id_cliente} - {clientes[0].nome}")
        if espacos:
            self.combo_espacos.set(f"{espacos[0].id_espaco} - {espacos[0].nome}")
        messagebox.showinfo("Dados", f"{len(clientes)} cliente(s) e {len(espacos)} espaco(s) carregados.")

    def _confirmar_agendamento(self):
        cliente_sel = self.combo_clientes.get()
        espaco_sel = self.combo_espacos.get()
        data = self.ent_data.get().strip()
        h_ini = self.ent_hora_inicio.get().strip()
        h_fim = self.ent_hora_fim.get().strip()

        if not all([cliente_sel, espaco_sel, data, h_ini, h_fim]):
            messagebox.showwarning("Aviso", "Preencha todos os campos e clique em 'Carregar dados'.")
            return
        try:
            id_cliente = int(cliente_sel.split(" - ")[0])
            id_espaco = int(espaco_sel.split(" - ")[0])
            novo = Agendamento(0, data, h_ini, h_fim, id_cliente, id_espaco)
            self.agendamento_repo.inserir(novo)
            messagebox.showinfo("Sucesso", "Agendamento realizado.")
            for e in (self.ent_data, self.ent_hora_inicio, self.ent_hora_fim):
                e.delete(0, tk.END)
            self._atualizar_lista_agendamentos()
        except Exception as e:
            messagebox.showerror("Erro de Regra de Negocio", f"Falha no agendamento:\n{e}")

    def _atualizar_lista_agendamentos(self):
        self.lista_agendamentos.delete("1.0", tk.END)
        try:
            agendamentos = self.agendamento_repo.listar_todos()
        except Exception as e:
            self.lista_agendamentos.insert(tk.END, f"Erro ao carregar: {e}")
            return
        if not agendamentos:
            self.lista_agendamentos.insert(tk.END, "Nenhum agendamento.")
            return
        for a in agendamentos:
            self.lista_agendamentos.insert(
                tk.END,
                f"#{a['id_agendamento']}  {a['data_reserva']}  {a['hora_inicio']}-{a['hora_fim']}  |  "
                f"{a['cliente']} em {a['espaco']}  |  R$ {a['valor_hora']:.2f}\n"
            )

    # ------------------------------------------------------------------
    # TAB: PAGAMENTOS
    # ------------------------------------------------------------------
    def _setup_tab_pagamentos(self):
        tab = self.tab_pagamentos_id

        form = ctk.CTkFrame(tab)
        form.pack(fill="x", padx=14, pady=14)

        ctk.CTkLabel(form, text="Processamento de Pagamento", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=14, pady=(12, 4))

        linha = ctk.CTkFrame(form, fg_color="transparent")
        linha.pack(fill="x", padx=14, pady=(0, 8))

        self.forma_pagto_var = ctk.StringVar(value="PIX")
        ctk.CTkRadioButton(linha, text="PIX", variable=self.forma_pagto_var, value="PIX").pack(side="left", padx=(0, 12))
        ctk.CTkRadioButton(linha, text="Cartao de Credito", variable=self.forma_pagto_var, value="CARTAO").pack(side="left")

        ctk.CTkButton(form, text="Processar pagamento", command=self._processar_pagamento).pack(anchor="w", padx=14, pady=(0, 12))

        ctk.CTkLabel(tab, text="Pagamentos registrados", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=14)
        self.lista_pagamentos = ctk.CTkTextbox(tab, height=200, font=ctk.CTkFont(size=13))
        self.lista_pagamentos.pack(fill="both", expand=True, padx=14, pady=(4, 14))

    def _processar_pagamento(self):
        # No desktop usamos o repository diretamente. Exige um agendamento existente.
        try:
            agendamentos = self.agendamento_repo.listar_todos()
        except Exception as e:
            messagebox.showerror("Erro", f"Nao foi possivel carregar agendamentos:\n{e}")
            return
        if not agendamentos:
            messagebox.showwarning("Aviso", "Nenhum agendamento disponivel para pagamento.")
            return

        a = agendamentos[0]
        forma = self.forma_pagto_var.get()
        try:
            self.pagamento_repo.inserir(a["valor_hora"], forma, a["id_agendamento"], "Pago")
            messagebox.showinfo("Sucesso", f"Pagamento via {forma} de R$ {a['valor_hora']:.2f} processado.")
            self._atualizar_lista_pagamentos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _atualizar_lista_pagamentos(self):
        self.lista_pagamentos.delete("1.0", tk.END)
        try:
            pagamentos = self.pagamento_repo.listar_todos()
        except Exception as e:
            self.lista_pagamentos.insert(tk.END, f"Erro ao carregar: {e}")
            return
        if not pagamentos:
            self.lista_pagamentos.insert(tk.END, "Nenhum pagamento registrado.")
            return
        for p in pagamentos:
            self.lista_pagamentos.insert(
                tk.END,
                f"#{p['id_pagamento']}  {p['cliente']} | {p['espaco']}  |  {p['forma_pagamento']}  "
                f"|  R$ {p['valor_total']:.2f}  |  {p['status']}\n"
            )
