/* View: Espacos & Quadras — grid de cards + modalidades visiveis + criar/editar/excluir */
const EspacosView = {
  async render() {
    const root = document.getElementById("viewRoot");
    root.innerHTML = `
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">🏟️ Espaços & Quadras</div>
            <div class="card-subtitle">Quadras disponíveis para reserva · agrupadas por modalidade</div>
          </div>
          <button class="btn btn-primary btn-sm" id="btnNovaQuadra">+ Nova quadra</button>
        </div>
        <div id="espacosContent">
          <div class="skeleton" style="height:200px;border-radius:16px"></div>
        </div>
      </div>
    `;
    document.getElementById("btnNovaQuadra").addEventListener("click", () => this._abrirModal());
    await this._load();
  },

  async _load() {
    try {
      const lista = await Api.espacos();
      const cont = document.getElementById("espacosContent");

      if (!lista.length) {
        cont.innerHTML = Helpers.empty("🏟️", "Nenhuma quadra cadastrada", "Clique em \"Nova quadra\" para adicionar o primeiro espaço.");
        return;
      }

      cont.innerHTML = `
        <div class="grid-cards">
          ${lista.map(e => `
            <div class="quadra-card">
              <div class="quadra-thumb">${this._icone(e.modalidade)} <span style="position:absolute;top:10px;right:12px;font-size:11px;background:rgba(0,0,0,0.4);padding:3px 9px;border-radius:999px;color:#fff;backdrop-filter:blur(4px)">${Helpers.escapar(e.modalidade || "Geral")}</span></div>
              <div class="quadra-body">
                <h3>${Helpers.escapar(e.nome)}</h3>
                <div class="quadra-meta">${Helpers.escapar(e.descricao || "")} · ${Helpers.escapar(e.tamanho_quadra || "")}</div>
                <div class="quadra-price">${Helpers.formatarMoeda(e.valor_hora)} <small>/ hora</small></div>
                <div style="margin-top:12px">${Helpers.acoes(e.id_espaco)}</div>
              </div>
            </div>`).join("")}
        </div>
      `;
      this._bindBotoes(lista);
    } catch (e) {
      Toast.error(e.message);
    }
  },

  _icone(mod) {
    const n = (mod || "").toLowerCase();
    if (n.includes("fut")) return "⚽";
    if (n.includes("basq")) return "🏀";
    if (n.includes("vol") || n.includes("tenis")) return "🏐";
    if (n.includes("pad")) return "🏓";
    return "🏟️";
  },

  _bindBotoes(lista) {
    const cont = document.getElementById("espacosContent");
    cont.querySelectorAll(".btn-edit").forEach(btn => {
      btn.addEventListener("click", () => {
        const esp = lista.find(x => String(x.id_espaco) === btn.dataset.id);
        if (esp) this._abrirModal(esp);
      });
    });
    cont.querySelectorAll(".btn-delete").forEach(btn => {
      btn.addEventListener("click", async () => {
        const id = btn.dataset.id;
        if (!confirm(`Tem certeza que deseja excluir a quadra #${id}? Agendamentos vinculados tambem serao removidos.`)) return;
        btn.disabled = true; btn.innerHTML = '<span class="spinner"></span>';
        try {
          await Api.deletarEspaco(id);
          Toast.success("Quadra excluida.");
          await this._load();
        } catch (e) { Toast.error(e.message); }
      });
    });
  },

  async _abrirModal(espacoEdit = null) {
    let modalidades = [];
    try { modalidades = await Api.modalidades(); } catch (_) {}
    const editando = !!espacoEdit;
    const e = espacoEdit || {};

    const html = `
      <div class="modal-backdrop" id="modalBackdrop">
        <div class="modal">
          <div class="modal-header">
            <h2>${editando ? "Editar quadra" : "Cadastrar quadra"}</h2>
            <button class="modal-close" data-fechar>×</button>
          </div>
          <form id="formQuadra">
            <div class="modal-body">
              <div class="form-grid">
                <div class="field full">
                  <label>Nome da quadra *</label>
                  <input type="text" name="nome" placeholder="Ex.: Quadra Central" required value="${Helpers.escapar(e.nome || "")}" />
                </div>
                <div class="field">
                  <label>Valor por hora (R$) *</label>
                  <input type="number" step="0.01" min="0" name="valor_hora" placeholder="80,00" required value="${e.valor_hora || ""}" />
                </div>
                <div class="field">
                  <label>Modalidade</label>
                  <select name="id_modalidade">
                    ${modalidades.map(m => `<option value="${m.id_modalidade}" ${String(m.id_modalidade) === String(e.id_modalidade || 1) ? "selected" : ""}>${Helpers.escapar(m.nome)}</option>`).join("")}
                  </select>
                </div>
                <div class="field">
                  <label>Tamanho</label>
                  <input type="text" name="tamanho_quadra" placeholder="Oficial" value="${Helpers.escapar(e.tamanho_quadra || "Oficial")}" />
                </div>
                <div class="field">
                  <label>Descrição</label>
                  <input type="text" name="descricao" placeholder="Quadra poliesportiva" value="${Helpers.escapar(e.descricao || "Quadra Poliesportiva")}" />
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-ghost" data-fechar>Cancelar</button>
              <button type="submit" class="btn btn-primary">💾 ${editando ? "Salvar alterações" : "Salvar espaço"}</button>
            </div>
          </form>
        </div>
      </div>`;
    document.body.insertAdjacentHTML("beforeend", html);

    const fechar = () => document.getElementById("modalBackdrop").remove();
    document.querySelectorAll("#modalBackdrop [data-fechar]").forEach(b => b.addEventListener("click", fechar));
    document.getElementById("modalBackdrop").addEventListener("click", (ev) => { if (ev.target.id === "modalBackdrop") fechar(); });

    document.getElementById("formQuadra").addEventListener("submit", async (ev) => {
      ev.preventDefault();
      const dados = Object.fromEntries(new FormData(ev.target).entries());
      const payload = {
        nome: dados.nome,
        valor_hora: parseFloat(dados.valor_hora),
        tamanho_quadra: dados.tamanho_quadra,
        descricao: dados.descricao,
        id_modalidade: parseInt(dados.id_modalidade),
      };
      const btn = ev.target.querySelector('button[type=submit]');
      btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Salvando...';
      try {
        if (editando) {
          await Api.atualizarEspaco(e.id_espaco, payload);
          Toast.success("Quadra atualizada!");
        } else {
          await Api.criarEspaco(payload);
          Toast.success("Quadra cadastrada!");
        }
        fechar();
        await this._load();
      } catch (err) {
        Toast.error(err.message);
        btn.disabled = false; btn.innerHTML = editando ? "💾 Salvar alterações" : "💾 Salvar espaço";
      }
    });
  },
};
