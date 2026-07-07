/* View: Pagamentos — tabela + criar/editar/excluir */
const PagamentosView = {
  async render() {
    const root = document.getElementById("viewRoot");
    root.innerHTML = `
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">💳 Pagamentos</div>
            <div class="card-subtitle">Histórico e processamento de pagamentos</div>
          </div>
          <button class="btn btn-primary btn-sm" id="btnNovoPagto">+ Processar pagamento</button>
        </div>
        <div class="table-wrap">
          <table class="data-table">
            <thead>
              <tr><th>ID</th><th>Cliente</th><th>Espaço</th><th>Reserva</th><th>Forma</th><th>Valor</th><th>Status</th><th>Ações</th></tr>
            </thead>
            <tbody id="pagBody">${Helpers.skeletonRows(4, 8)}</tbody>
          </table>
        </div>
      </div>
    `;
    document.getElementById("btnNovoPagto").addEventListener("click", () => this._abrirModal());
    await this._load();
  },

  async _load() {
    try {
      const lista = await Api.pagamentos();
      const tbody = document.getElementById("pagBody");
      if (!lista.length) {
        tbody.innerHTML = `<tr><td colspan="8">${Helpers.empty("💳", "Nenhum pagamento", "Processe o pagamento de uma reserva.").replace(/<div class="empty-state">|<\/div>/g, "")}</td></tr>`;
        return;
      }
      tbody.innerHTML = lista.map(p => `
        <tr>
          <td class="cell-muted">#${p.id_pagamento}</td>
          <td class="cell-strong">${Helpers.escapar(p.cliente)}</td>
          <td class="cell-muted">🏟️ ${Helpers.escapar(p.espaco)}</td>
          <td>${Helpers.formatarData(p.data_reserva)} ${p.hora_inicio || ""}</td>
          <td>${this._badgeForma(p.forma_pagamento)}</td>
          <td class="cell-strong">${Helpers.formatarMoeda(p.valor_total)}</td>
          <td>${Helpers.badgeStatus(p.status)}</td>
          <td>${Helpers.acoes(p.id_pagamento)}</td>
        </tr>`).join("");
      this._bindBotoes(lista);
    } catch (e) { Toast.error(e.message); }
  },

  _bindBotoes(lista) {
    const tbody = document.getElementById("pagBody");
    tbody.querySelectorAll(".btn-edit").forEach(btn => {
      btn.addEventListener("click", () => {
        const pag = lista.find(x => String(x.id_pagamento) === btn.dataset.id);
        if (pag) this._abrirModalEdicao(pag);
      });
    });
    tbody.querySelectorAll(".btn-delete").forEach(btn => {
      btn.addEventListener("click", async () => {
        const id = btn.dataset.id;
        if (!confirm(`Tem certeza que deseja excluir o pagamento #${id}?`)) return;
        btn.disabled = true; btn.innerHTML = '<span class="spinner"></span>';
        try {
          await Api.deletarPagamento(id);
          Toast.success("Pagamento excluido.");
          await this._load();
        } catch (e) { Toast.error(e.message); }
      });
    });
  },

  _badgeForma(forma) {
    const f = (forma || "").toUpperCase();
    if (f.includes("PIX")) return '<span class="badge badge-neutral">⚡ PIX</span>';
    if (f.includes("CART")) return '<span class="badge badge-neutral">💳 Cartão</span>';
    return `<span class="badge badge-neutral">${Helpers.escapar(forma || "—")}</span>`;
  },

  _abrirModalEdicao(p) {
    const html = `
      <div class="modal-backdrop" id="modalBackdrop">
        <div class="modal" style="max-width:460px">
          <div class="modal-header">
            <h2>Editar pagamento #${p.id_pagamento}</h2>
            <button class="modal-close" data-fechar>×</button>
          </div>
          <form id="formPagEdit">
            <div class="modal-body">
              <div style="background:var(--bg-base);padding:12px;border-radius:10px;margin-bottom:14px;font-size:13px">
                <b>${Helpers.escapar(p.cliente)}</b> · ${Helpers.escapar(p.espaco)}<br>
                <span class="cell-muted">${Helpers.formatarData(p.data_reserva)} ${p.hora_inicio || ""}</span>
              </div>
              <div class="form-grid">
                <div class="field">
                  <label>Forma</label>
                  <select name="forma_pagamento">
                    <option value="PIX" ${String(p.forma_pagamento).toUpperCase().includes("PIX") ? "selected" : ""}>⚡ PIX</option>
                    <option value="CARTAO" ${String(p.forma_pagamento).toUpperCase().includes("CART") ? "selected" : ""}>💳 Cartão</option>
                  </select>
                </div>
                <div class="field">
                  <label>Status</label>
                  <select name="status">
                    <option value="Pago" ${p.status === "Pago" ? "selected" : ""}>✅ Pago</option>
                    <option value="Pendente" ${p.status === "Pendente" ? "selected" : ""}>⏳ Pendente</option>
                    <option value="Cancelado" ${p.status === "Cancelado" ? "selected" : ""}>❌ Cancelado</option>
                  </select>
                </div>
                <div class="field full">
                  <label>Valor (R$)</label>
                  <input type="number" step="0.01" min="0" name="valor_total" value="${p.valor_total}" />
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-ghost" data-fechar>Cancelar</button>
              <button type="submit" class="btn btn-primary">💾 Salvar alterações</button>
            </div>
          </form>
        </div>
      </div>`;
    document.body.insertAdjacentHTML("beforeend", html);

    const fechar = () => document.getElementById("modalBackdrop").remove();
    document.querySelectorAll("#modalBackdrop [data-fechar]").forEach(b => b.addEventListener("click", fechar));
    document.getElementById("modalBackdrop").addEventListener("click", (ev) => { if (ev.target.id === "modalBackdrop") fechar(); });

    document.getElementById("formPagEdit").addEventListener("submit", async (ev) => {
      ev.preventDefault();
      const dados = Object.fromEntries(new FormData(ev.target).entries());
      const btn = ev.target.querySelector('button[type=submit]');
      btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Salvando...';
      try {
        await Api.atualizarPagamento(p.id_pagamento, {
          forma_pagamento: dados.forma_pagamento,
          status: dados.status,
          valor_total: parseFloat(dados.valor_total),
        });
        Toast.success("Pagamento atualizado!");
        fechar(); await this._load();
      } catch (e) { Toast.error(e.message); btn.disabled = false; btn.innerHTML = "💾 Salvar alterações"; }
    });
  },

  async _abrirModal() {
    let agendamentos = [];
    try { agendamentos = await Api.agendamentos(); } catch (e) { Toast.error("Nao foi possivel carregar agendamentos. " + e.message); return; }
    if (!agendamentos.length) { Toast.info("Crie um agendamento antes de processar pagamento."); return; }

    const html = `
      <div class="modal-backdrop" id="modalBackdrop">
        <div class="modal">
          <div class="modal-header">
            <h2>Processar pagamento</h2>
            <button class="modal-close" data-fechar>×</button>
          </div>
          <form id="formPag">
            <div class="modal-body">
              <div class="form-grid">
                <div class="field full">
                  <label>Agendamento *</label>
                  <select name="id_agendamento" id="selAg" required>
                    ${agendamentos.map(a => `<option value="${a.id_agendamento}" data-valor="${a.valor_hora}">${Helpers.escapar(a.cliente)} · ${Helpers.escapar(a.espaco)} · ${Helpers.formatarData(a.data_reserva)} ${a.hora_inicio}</option>`).join("")}
                  </select>
                </div>
                <div class="field">
                  <label>Forma de pagamento *</label>
                  <select name="forma_pagamento" required>
                    <option value="PIX">⚡ PIX</option>
                    <option value="CARTAO">💳 Cartão de Crédito</option>
                  </select>
                </div>
                <div class="field">
                  <label>Valor (R$) *</label>
                  <input type="number" step="0.01" min="0" name="valor_total" id="inpValor" required />
                </div>
              </div>
              <div style="margin-top:14px;padding:12px;background:var(--accent-primary-dim);border-radius:10px;font-size:13px;color:var(--accent-primary)">
                ✅ O pagamento será registrado com status <b>Pago</b> automaticamente.
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-ghost" data-fechar>Cancelar</button>
              <button type="submit" class="btn btn-primary">💳 Processar</button>
            </div>
          </form>
        </div>
      </div>`;
    document.body.insertAdjacentHTML("beforeend", html);

    const fechar = () => document.getElementById("modalBackdrop").remove();
    document.querySelectorAll("#modalBackdrop [data-fechar]").forEach(b => b.addEventListener("click", fechar));
    document.getElementById("modalBackdrop").addEventListener("click", (ev) => { if (ev.target.id === "modalBackdrop") fechar(); });

    const sel = document.getElementById("selAg");
    const inpValor = document.getElementById("inpValor");
    const sincronizar = () => { const opt = sel.options[sel.selectedIndex]; inpValor.value = opt ? Number(opt.dataset.valor).toFixed(2) : ""; };
    sincronizar();
    sel.addEventListener("change", sincronizar);

    document.getElementById("formPag").addEventListener("submit", async (ev) => {
      ev.preventDefault();
      const dados = Object.fromEntries(new FormData(ev.target).entries());
      const btn = ev.target.querySelector('button[type=submit]');
      btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Processando...';
      try {
        await Api.criarPagamento({
          id_agendamento: parseInt(dados.id_agendamento),
          forma_pagamento: dados.forma_pagamento,
          valor_total: parseFloat(dados.valor_total),
          status: "Pago",
        });
        Toast.success("Pagamento processado com sucesso!");
        fechar(); await this._load();
      } catch (e) { Toast.error(e.message); btn.disabled = false; btn.innerHTML = "💳 Processar"; }
    });
  },
};
