/* View: Clientes — tabela + criar/editar/excluir */
const ClientesView = {
  async render() {
    const root = document.getElementById("viewRoot");
    root.innerHTML = `
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">👥 Clientes</div>
            <div class="card-subtitle">Cadastro e gestão de clientes</div>
          </div>
          <div style="display:flex;gap:10px;align-items:center">
            <div class="field" style="margin:0;min-width:240px">
              <input type="text" id="buscaCliente" placeholder="🔍 Buscar por nome ou CPF..." style="padding:9px 13px" />
            </div>
            <button class="btn btn-primary btn-sm" id="btnNovoCliente">+ Novo cliente</button>
          </div>
        </div>
        <div class="table-wrap">
          <table class="data-table">
            <thead>
              <tr><th>ID</th><th>Nome</th><th>CPF</th><th>Endereço</th><th>Telefone</th><th>Ações</th></tr>
            </thead>
            <tbody id="clientesBody">${Helpers.skeletonRows(4, 6)}</tbody>
          </table>
        </div>
      </div>
    `;
    document.getElementById("btnNovoCliente").addEventListener("click", () => this._abrirModal());

    // Busca em tempo real (com debounce)
    let timer;
    document.getElementById("buscaCliente").addEventListener("input", (ev) => {
      clearTimeout(timer);
      timer = setTimeout(() => this._load(ev.target.value), 300);
    });

    await this._load();
  },

  async _load(termo = "") {
    try {
      const lista = await Api.clientes(termo);
      const tbody = document.getElementById("clientesBody");
      if (!lista.length) {
        const msg = termo ? "Nenhum cliente encontrado para esta busca." : "Cadastre o primeiro cliente.";
        tbody.innerHTML = `<tr><td colspan="6">${Helpers.empty("👤", "Nenhum cliente", msg).replace(/<div class="empty-state">|<\/div>/g, "")}</td></tr>`;
        return;
      }
      tbody.innerHTML = lista.map(c => `
        <tr>
          <td class="cell-muted">#${c.id_cliente}</td>
          <td class="cell-strong">${Helpers.escapar(c.nome)}</td>
          <td>${Helpers.escapar(c.cpf)}</td>
          <td class="cell-muted">${Helpers.escapar(c.endereco || "—")}</td>
          <td>${Helpers.escapar(c.telefone || "—")}</td>
          <td>${Helpers.acoes(c.id_cliente)}</td>
        </tr>`).join("");
      this._bindBotoes(lista);
    } catch (e) {
      Toast.error(e.message);
    }
  },

  _bindBotoes(lista) {
    const tbody = document.getElementById("clientesBody");
    tbody.querySelectorAll(".btn-edit").forEach(btn => {
      btn.addEventListener("click", () => {
        const cli = lista.find(x => String(x.id_cliente) === btn.dataset.id);
        if (cli) this._abrirModal(cli);
      });
    });
    tbody.querySelectorAll(".btn-delete").forEach(btn => {
      btn.addEventListener("click", async () => {
        const id = btn.dataset.id;
        if (!confirm(`Tem certeza que deseja excluir o cliente #${id}?`)) return;
        btn.disabled = true; btn.innerHTML = '<span class="spinner"></span>';
        try {
          await Api.deletarCliente(id);
          Toast.success("Cliente excluido.");
          await this._load();
        } catch (e) { Toast.error(e.message); }
      });
    });
  },

  _abrirModal(clienteEdit = null) {
    const editando = !!clienteEdit;
    const c = clienteEdit || {};
    const html = `
      <div class="modal-backdrop" id="modalBackdrop">
        <div class="modal">
          <div class="modal-header">
            <h2>${editando ? "Editar cliente" : "Cadastrar cliente"}</h2>
            <button class="modal-close" data-fechar>×</button>
          </div>
          <form id="formCliente">
            <div class="modal-body">
              <div class="form-grid">
                <div class="field full">
                  <label>Nome completo *</label>
                  <input type="text" name="nome" placeholder="João da Silva" required value="${Helpers.escapar(c.nome || "")}" />
                </div>
                <div class="field">
                  <label>CPF * <span style="color:var(--text-muted)">(11 dígitos)</span></label>
                  <input type="text" name="cpf" maxlength="14" placeholder="12345678901" required value="${Helpers.escapar(c.cpf || "")}" />
                </div>
                <div class="field">
                  <label>Telefone</label>
                  <input type="text" name="telefone" placeholder="(92) 99999-9999" value="${Helpers.escapar(c.telefone || "")}" />
                </div>
                <div class="field full">
                  <label>Endereço</label>
                  <input type="text" name="endereco" placeholder="Rua, número, bairro" value="${Helpers.escapar(c.endereco || "")}" />
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-ghost" data-fechar>Cancelar</button>
              <button type="submit" class="btn btn-primary">💾 ${editando ? "Salvar alterações" : "Cadastrar"}</button>
            </div>
          </form>
        </div>
      </div>`;
    document.body.insertAdjacentHTML("beforeend", html);

    const fechar = () => document.getElementById("modalBackdrop").remove();
    document.querySelectorAll("#modalBackdrop [data-fechar]").forEach(b => b.addEventListener("click", fechar));
    document.getElementById("modalBackdrop").addEventListener("click", (ev) => { if (ev.target.id === "modalBackdrop") fechar(); });

    const cpfInput = document.querySelector('#formCliente [name=cpf]');
    cpfInput.addEventListener("input", () => { cpfInput.value = cpfInput.value.replace(/\D/g, "").slice(0, 11); });

    document.getElementById("formCliente").addEventListener("submit", async (ev) => {
      ev.preventDefault();
      const dados = Object.fromEntries(new FormData(ev.target).entries());
      const btn = ev.target.querySelector('button[type=submit]');
      btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Salvando...';
      try {
        if (editando) {
          await Api.atualizarCliente(c.id_cliente, dados);
          Toast.success("Cliente atualizado!");
        } else {
          await Api.criarCliente(dados);
          Toast.success("Cliente cadastrado!");
        }
        fechar();
        await this._load();
      } catch (e) {
        Toast.error(e.message);
        btn.disabled = false; btn.innerHTML = editando ? "💾 Salvar alterações" : "💾 Cadastrar";
      }
    });
  },
};
