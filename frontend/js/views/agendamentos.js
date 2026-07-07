/* View: Agendamentos — tabela + criar/editar/excluir */
const AgendamentosView = {
  async render() {
    const root = document.getElementById("viewRoot");
    root.innerHTML = `
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">📅 Agendamentos</div>
            <div class="card-subtitle">Reservas de horário nas quadras</div>
          </div>
          <button class="btn btn-primary btn-sm" id="btnNovaReserva">+ Nova reserva</button>
        </div>
        <div class="table-wrap">
          <table class="data-table">
            <thead>
              <tr><th>Data</th><th>Horário</th><th>Cliente</th><th>Espaço</th><th>Valor</th><th>Ações</th></tr>
            </thead>
            <tbody id="agBody">${Helpers.skeletonRows(4, 6)}</tbody>
          </table>
        </div>
      </div>
    `;
    document.getElementById("btnNovaReserva").addEventListener("click", () => this._abrirModal());
    await this._load();
  },

  async _load() {
    try {
      const lista = await Api.agendamentos();
      const tbody = document.getElementById("agBody");
      if (!lista.length) {
        tbody.innerHTML = `<tr><td colspan="6">${Helpers.empty("📅", "Nenhuma reserva", "Crie o primeiro agendamento.").replace(/<div class="empty-state">|<\/div>/g, "")}</td></tr>`;
        return;
      }
      tbody.innerHTML = lista.map(a => `
        <tr>
          <td class="cell-strong">${Helpers.formatarData(a.data_reserva)}</td>
          <td>${a.hora_inicio} – ${a.hora_fim}</td>
          <td>${Helpers.escapar(a.cliente)}</td>
          <td class="cell-muted">🏟️ ${Helpers.escapar(a.espaco)}</td>
          <td class="cell-strong">${Helpers.formatarMoeda(a.valor_hora)}</td>
          <td>${Helpers.acoes(a.id_agendamento)}</td>
        </tr>`).join("");
      this._bindBotoes(lista);
    } catch (e) {
      Toast.error(e.message);
    }
  },

  _bindBotoes(lista) {
    const tbody = document.getElementById("agBody");
    tbody.querySelectorAll(".btn-edit").forEach(btn => {
      btn.addEventListener("click", () => {
        const ag = lista.find(x => String(x.id_agendamento) === btn.dataset.id);
        if (ag) this._abrirModal(ag);
      });
    });
    tbody.querySelectorAll(".btn-delete").forEach(btn => {
      btn.addEventListener("click", async () => {
        const id = btn.dataset.id;
        if (!confirm(`Tem certeza que deseja excluir o agendamento #${id}? O pagamento vinculado tambem sera removido.`)) return;
        btn.disabled = true; btn.innerHTML = '<span class="spinner"></span>';
        try {
          await Api.deletarAgendamento(id);
          Toast.success("Agendamento excluido.");
          await this._load();
        } catch (e) { Toast.error(e.message); }
      });
    });
  },

  async _abrirModal(agEdit = null) {
    let clientes = [], espacos = [];
    try {
      [clientes, espacos] = await Promise.all([Api.clientes(), Api.espacos()]);
    } catch (e) { Toast.error("Nao foi possivel carregar clientes/espacos. " + e.message); return; }
    if (!clientes.length || !espacos.length) {
      Toast.info("Cadastre ao menos 1 cliente e 1 espaco antes de agendar.");
      return;
    }

    const editando = !!agEdit;
    const a = agEdit || {};
    const hoje = new Date().toISOString().slice(0, 10);

    const html = `
      <div class="modal-backdrop" id="modalBackdrop">
        <div class="modal">
          <div class="modal-header">
            <h2>${editando ? "Editar reserva" : "Nova reserva"}</h2>
            <button class="modal-close" data-fechar>×</button>
          </div>
          <form id="formAg">
            <div class="modal-body">
              <div class="form-grid">
                <div class="field full">
                  <label>Cliente *</label>
                  <select name="id_cliente" required>
                    ${clientes.map(c => `<option value="${c.id_cliente}" ${String(c.id_cliente) === String(a.id_cliente || "") ? "selected" : ""}>${Helpers.escapar(c.nome)} · ${Helpers.escapar(c.cpf)}</option>`).join("")}
                  </select>
                </div>
                <div class="field full">
                  <label>Espaço / Quadra *</label>
                  <select name="id_espaco" required>
                    ${espacos.map(e => `<option value="${e.id_espaco}" ${String(e.id_espaco) === String(a.id_espaco || "") ? "selected" : ""}>${Helpers.escapar(e.nome)} — ${Helpers.formatarMoeda(e.valor_hora)}/h</option>`).join("")}
                  </select>
                </div>
                <div class="field">
                  <label>Data *</label>
                  <input type="date" name="data_reserva" value="${a.data_reserva || hoje}" required />
                </div>
                <div class="field"><label>Horário</label><div style="color:var(--text-muted);font-size:12px">Selecione início e fim</div></div>
                <div class="field"><label>Hora início *</label><input type="time" name="hora_inicio" value="${a.hora_inicio || ""}" required /></div>
                <div class="field"><label>Hora fim *</label><input type="time" name="hora_fim" value="${a.hora_fim || ""}" required /></div>
              </div>
              <div style="margin-top:10px;font-size:12px;color:var(--text-muted)">ℹ️ O sistema valida automaticamente choques de horário (double-booking).</div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-ghost" data-fechar>Cancelar</button>
              <button type="submit" class="btn btn-primary">📅 ${editando ? "Salvar alterações" : "Confirmar reserva"}</button>
            </div>
          </form>
        </div>
      </div>`;
    document.body.insertAdjacentHTML("beforeend", html);

    const fechar = () => document.getElementById("modalBackdrop").remove();
    document.querySelectorAll("#modalBackdrop [data-fechar]").forEach(b => b.addEventListener("click", fechar));
    document.getElementById("modalBackdrop").addEventListener("click", (ev) => { if (ev.target.id === "modalBackdrop") fechar(); });

    document.getElementById("formAg").addEventListener("submit", async (ev) => {
      ev.preventDefault();
      const dados = Object.fromEntries(new FormData(ev.target).entries());
      if (dados.hora_inicio >= dados.hora_fim) { Toast.error("A hora final deve ser maior que a hora inicial."); return; }
      const payload = {
        id_cliente: parseInt(dados.id_cliente), id_espaco: parseInt(dados.id_espaco),
        data_reserva: dados.data_reserva, hora_inicio: dados.hora_inicio, hora_fim: dados.hora_fim,
      };
      const btn = ev.target.querySelector('button[type=submit]');
      btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Salvando...';
      try {
        if (editando) {
          await Api.atualizarAgendamento(a.id_agendamento, payload);
          Toast.success("Reserva atualizada!");
        } else {
          await Api.criarAgendamento(payload);
          Toast.success("Reserva confirmada!");
        }
        fechar(); await this._load();
      } catch (e) { Toast.error(e.message); btn.disabled = false; btn.innerHTML = editando ? "📅 Salvar alterações" : "📅 Confirmar reserva"; }
    });
  },
};
