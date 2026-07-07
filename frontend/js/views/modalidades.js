/* View: Modalidades — listagem em cards + criar nova modalidade */
const ModalidadesView = {
  async render() {
    const root = document.getElementById("viewRoot");
    root.innerHTML = `
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">🏷️ Modalidades</div>
            <div class="card-subtitle">Categorias esportivas vinculadas às quadras</div>
          </div>
          <button class="btn btn-primary btn-sm" id="btnNovaMod">+ Nova modalidade</button>
        </div>
        <div id="modalidadeContent">
          <div class="skeleton" style="height:60px;border-radius:12px"></div>
        </div>
      </div>
    `;
    document.getElementById("btnNovaMod").addEventListener("click", () => this._abrirModal());
    await this._load();
  },

  async _load() {
    try {
      const [lista, espacos] = await Promise.all([Api.modalidades(), Api.espacos().catch(() => [])]);
      const cont = document.getElementById("modalidadeContent");

      if (!lista.length) {
        cont.innerHTML = Helpers.empty("🏷️", "Nenhuma modalidade", "A modalidade padrão é criada ao executar o schema.sql.");
        return;
      }

      cont.innerHTML = `
        <div class="grid-cards">
          ${lista.map(m => {
            const count = espacos.filter(e => String(e.id_modalidade) === String(m.id_modalidade)).length;
            return `
              <div class="quadra-card">
                <div class="quadra-thumb">${this._icone(m.nome)}</div>
                <div class="quadra-body">
                  <h3>${Helpers.escapar(m.nome)}</h3>
                  <div class="quadra-meta">ID #${m.id_modalidade} · ${count} quadra(s) vinculada(s)</div>
                </div>
              </div>`;
          }).join("")}
        </div>
      `;
    } catch (e) {
      Toast.error(e.message);
    }
  },

  _icone(nome) {
    const n = (nome || "").toLowerCase();
    if (n.includes("fut")) return "⚽";
    if (n.includes("basq")) return "🏀";
    if (n.includes("vol") || n.includes("tenis")) return "🏐";
    if (n.includes("pad")) return "🏓";
    return "🏟️";
  },

  _abrirModal() {
    const html = `
      <div class="modal-backdrop" id="modalBackdrop">
        <div class="modal" style="max-width:420px">
          <div class="modal-header">
            <h2>Nova modalidade</h2>
            <button class="modal-close" data-fechar>×</button>
          </div>
          <form id="formMod">
            <div class="modal-body">
              <div class="field full">
                <label>Nome da modalidade *</label>
                <input type="text" name="nome" placeholder="Ex.: Futsal, Basquete, Vôlei..." required />
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-ghost" data-fechar>Cancelar</button>
              <button type="submit" class="btn btn-primary">🏷️ Cadastrar</button>
            </div>
          </form>
        </div>
      </div>`;
    document.body.insertAdjacentHTML("beforeend", html);

    const fechar = () => document.getElementById("modalBackdrop").remove();
    document.querySelectorAll("#modalBackdrop [data-fechar]").forEach(b => b.addEventListener("click", fechar));
    document.getElementById("modalBackdrop").addEventListener("click", (ev) => { if (ev.target.id === "modalBackdrop") fechar(); });

    document.getElementById("formMod").addEventListener("submit", async (ev) => {
      ev.preventDefault();
      const dados = Object.fromEntries(new FormData(ev.target).entries());
      const btn = ev.target.querySelector('button[type=submit]');
      btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Salvando...';
      try {
        await Api.criarModalidade({ nome: dados.nome });
        Toast.success("Modalidade cadastrada!");
        fechar();
        await this._load();
      } catch (err) {
        Toast.error(err.message);
        btn.disabled = false; btn.innerHTML = "🏷️ Cadastrar";
      }
    });
  },
};
