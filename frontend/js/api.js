/* ============================================================
   ATHLETIX — Cliente HTTP (API REST Flask)
   Usa URL relativa: o proprio Flask serve o frontend, entao
   nao ha problema de CORS nem de conexao.
   ============================================================ */

const API_BASE = "/api";

/* ---------- Toasts ---------- */
const Toast = {
  stack() { return document.getElementById("toastStack"); },

  show(mensagem, tipo = "info", duracao = 3800) {
    const el = document.createElement("div");
    el.className = `toast ${tipo}`;
    const icones = { success: "✅", error: "⛔", info: "ℹ️" };
    el.innerHTML = `<span class="t-ico">${icones[tipo] || icones.info}</span><span>${mensagem}</span>`;
    this.stack().appendChild(el);
    setTimeout(() => {
      el.style.opacity = "0";
      el.style.transform = "translateX(40px)";
      el.style.transition = "0.3s";
      setTimeout(() => el.remove(), 300);
    }, duracao);
  },

  success(m) { this.show(m, "success"); },
  error(m) { this.show(m, "error", 5200); },
  info(m) { this.show(m, "info"); },
};

/* ---------- API (GET, POST, DELETE) ---------- */
const Api = {
  async _request(metodo, caminho, corpo) {
    const opcoes = { method: metodo, headers: {} };
    if (corpo !== undefined) {
      opcoes.headers["Content-Type"] = "application/json";
      opcoes.body = JSON.stringify(corpo);
    }
    let resposta;
    try {
      resposta = await fetch(`${API_BASE}${caminho}`, opcoes);
    } catch (err) {
      throw new Error("Nao foi possivel conectar. Verifique se o backend esta rodando (python backend/app.py) e acesse http://127.0.0.1:5000");
    }

    let dados = null;
    try { dados = await resposta.json(); } catch (_) { /* corpo vazio */ }

    if (!resposta.ok) {
      const msg = (dados && dados.erro) || `Erro ${resposta.status}`;
      const limpa = msg.replace(/^[A-Z]+\s*:\s*/, "").split("\n")[0];
      throw new Error(limpa);
    }
    return dados;
  },

  get(caminho)    { return this._request("GET", caminho); },
  post(caminho, corpo) { return this._request("POST", caminho, corpo); },
  put(caminho, corpo)  { return this._request("PUT", caminho, corpo); },
  delete(caminho) { return this._request("DELETE", caminho); },

  // Endpoints de conveniencia
  dashboard:            () => Api.get("/dashboard/stats"),
  modalidades:          () => Api.get("/modalidades"),
  criarModalidade:      (d) => Api.post("/modalidades", d),
  espacos:              () => Api.get("/espacos"),
  criarEspaco:          (d) => Api.post("/espacos", d),
  atualizarEspaco:      (id, d) => Api.put(`/espacos/${id}`, d),
  deletarEspaco:        (id) => Api.delete(`/espacos/${id}`),
  clientes:             (q) => Api.get(q ? `/clientes?q=${encodeURIComponent(q)}` : "/clientes"),
  criarCliente:         (d) => Api.post("/clientes", d),
  atualizarCliente:     (id, d) => Api.put(`/clientes/${id}`, d),
  deletarCliente:       (id) => Api.delete(`/clientes/${id}`),
  agendamentos:         () => Api.get("/agendamentos"),
  criarAgendamento:     (d) => Api.post("/agendamentos", d),
  atualizarAgendamento: (id, d) => Api.put(`/agendamentos/${id}`, d),
  deletarAgendamento:   (id) => Api.delete(`/agendamentos/${id}`),
  pagamentos:           () => Api.get("/pagamentos"),
  criarPagamento:       (d) => Api.post("/pagamentos", d),
  atualizarPagamento:   (id, d) => Api.put(`/pagamentos/${id}`, d),
  deletarPagamento:     (id) => Api.delete(`/pagamentos/${id}`),
};

/* ---------- Helpers de UI ---------- */
const Helpers = {
  formatarMoeda(v) {
    return (Number(v) || 0).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
  },
  formatarData(iso) {
    if (!iso) return "—";
    const [y, m, d] = iso.split("-");
    return `${d}/${m}/${y}`;
  },
  formatarDataLonga(iso) {
    if (!iso) return "—";
    const dt = new Date(iso + "T00:00:00");
    return dt.toLocaleDateString("pt-BR", { weekday: "short", day: "2-digit", month: "short" });
  },
  badgeStatus(status) {
    const s = (status || "").toLowerCase();
    if (s.includes("pago")) return '<span class="badge badge-pago">Pago</span>';
    if (s.includes("pend")) return '<span class="badge badge-pendente">Pendente</span>';
    if (s.includes("cancel")) return '<span class="badge badge-cancelado">Cancelado</span>';
    return '<span class="badge badge-neutral">Sem pagamento</span>';
  },
  empty(icone, titulo, texto) {
    return `<div class="empty-state">
      <div class="ico">${icone}</div>
      <h3>${titulo}</h3>
      <p>${texto}</p>
    </div>`;
  },
  skeletonRows(n = 5, colunas = 4) {
    let html = "";
    for (let i = 0; i < n; i++) {
      html += "<tr>" + "<td>".repeat(colunas).replace(/<td>/g, '<td><div class="skeleton" style="height:14px;width:80%"></div>') + "</tr>";
    }
    return html.replace(/<td><\/td>/g, "");
  },
  escapar(texto) {
    const div = document.createElement("div");
    div.textContent = texto == null ? "" : String(texto);
    return div.innerHTML;
  },
  btnExcluir(id, label = "Excluir") {
    return `<button class="btn btn-sm btn-ghost btn-delete" data-id="${id}" style="color:var(--accent-red);border-color:rgba(239,68,68,0.25);font-size:11px;padding:4px 10px">🗑️ ${label}</button>`;
  },
  btnEditar(id) {
    return `<button class="btn btn-sm btn-ghost btn-edit" data-id="${id}" style="color:var(--accent-blue);border-color:rgba(59,130,246,0.25);font-size:11px;padding:4px 10px">✏️ Editar</button>`;
  },
  acoes(id) {
    return `<div style="display:flex;gap:6px">${this.btnEditar(id)}${this.btnExcluir(id)}</div>`;
  },
};
