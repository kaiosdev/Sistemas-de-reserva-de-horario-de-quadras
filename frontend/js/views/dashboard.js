/* View: Dashboard — visão geral com stat cards e proximos agendamentos */
const DashboardView = {
  async render() {
    const root = document.getElementById("viewRoot");
    root.innerHTML = `
      <div class="hero">
        <h2>Bem-vindo ao painel Athletix 🏆</h2>
        <p>Gerencie quadras, clientes, reservas e pagamentos em um só lugar. O fluxo segue o encadeamento: Modalidade → Espaço → Cliente → Agendamento → Pagamento.</p>
      </div>

      <div class="stats-grid" id="statsGrid">
        ${this._skeletonStats()}
      </div>

      <div class="card" style="margin-top:24px">
        <div class="card-header">
          <div>
            <div class="card-title">Próximos agendamentos</div>
            <div class="card-subtitle">Reservas a partir de hoje</div>
          </div>
          <span class="badge badge-neutral" id="proxCount">—</span>
        </div>
        <div class="table-wrap">
          <table class="data-table">
            <thead>
              <tr><th>Data</th><th>Horário</th><th>Cliente</th><th>Espaço</th><th>Status</th></tr>
            </thead>
            <tbody id="proxBody">
              ${Helpers.skeletonRows(4, 5)}
            </tbody>
          </table>
        </div>
      </div>
    `;
    await this._load();
  },

  async _load() {
    try {
      const s = await Api.dashboard();
      document.getElementById("statsGrid").innerHTML = this._statCards(s);

      const tbody = document.getElementById("proxBody");
      const prox = s.proximos_agendamentos || [];
      document.getElementById("proxCount").textContent = `${prox.length} reserva(s)`;

      if (!prox.length) {
        tbody.innerHTML = `<tr><td colspan="5">${Helpers.empty("📅", "Nenhuma reserva futura", "Crie um agendamento para vê-lo aqui.").replace(/<div class="empty-state">/, '').replace(/<\/div>$/,'')}</td></tr>`;
        return;
      }
      tbody.innerHTML = prox.map(a => `
        <tr>
          <td class="cell-strong">${Helpers.formatarDataLonga(a.data_reserva)}</td>
          <td>${a.hora_inicio} – ${a.hora_fim}</td>
          <td>${Helpers.escapar(a.cliente)}</td>
          <td class="cell-muted">🏟️ ${Helpers.escapar(a.espaco)}</td>
          <td>${Helpers.badgeStatus(a.status)}</td>
        </tr>
      `).join("");
    } catch (e) {
      Toast.error(e.message);
    }
  },

  _skeletonStats() {
    const tipos = ["green", "blue", "purple", "amber"];
    return tipos.map(t => `
      <div class="stat-card ${t}">
        <div class="skeleton" style="width:46px;height:46px;border-radius:13px;margin-bottom:14px"></div>
        <div class="skeleton" style="height:30px;width:60%;margin-bottom:8px"></div>
        <div class="skeleton" style="height:13px;width:80%"></div>
      </div>`).join("");
  },

  _statCards(s) {
    return `
      <div class="stat-card green">
        <div class="stat-icon">🏟️</div>
        <div class="stat-value">${s.total_espacos}</div>
        <div class="stat-label">Espaços cadastrados</div>
      </div>
      <div class="stat-card blue">
        <div class="stat-icon">👥</div>
        <div class="stat-value">${s.total_clientes}</div>
        <div class="stat-label">Clientes ativos</div>
      </div>
      <div class="stat-card purple">
        <div class="stat-icon">📅</div>
        <div class="stat-value">${s.reservas_hoje}</div>
        <div class="stat-label">Reservas hoje</div>
      </div>
      <div class="stat-card amber">
        <div class="stat-icon">💰</div>
        <div class="stat-value">${Helpers.formatarMoeda(s.faturamento)}</div>
        <div class="stat-label">Faturamento (pagos)</div>
      </div>
    `;
  },
};
