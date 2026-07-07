/* ============================================================
   ATHLETIX — Roteador SPA (hash routing) + bootstrap
   ============================================================ */

const VIEWS = {
  dashboard: { titulo: "Dashboard", subtitulo: "Visão geral do complexo esportivo", modulo: DashboardView },
  modalidades: { titulo: "Modalidades", subtitulo: "Categorias esportivas das quadras", modulo: ModalidadesView },
  espacos: { titulo: "Espaços & Quadras", subtitulo: "Quadras disponíveis para reserva", modulo: EspacosView },
  clientes: { titulo: "Clientes", subtitulo: "Cadastro e gestão de clientes", modulo: ClientesView },
  agendamentos: { titulo: "Agendamentos", subtitulo: "Reservas de horário nas quadras", modulo: AgendamentosView },
  pagamentos: { titulo: "Pagamentos", subtitulo: "Histórico e processamento de pagamentos", modulo: PagamentosView },
};

const Router = {
  current: null,

  init() {
    // Navegação pela sidebar
    document.querySelectorAll(".nav-item").forEach(item => {
      item.addEventListener("click", () => this.navigate(item.dataset.view));
    });

    // Atualizar
    document.getElementById("refreshBtn").addEventListener("click", () => {
      if (this.current) this.navigate(this.current);
    });

    // Menu mobile
    const sidebar = document.getElementById("sidebar");
    const backdrop = document.getElementById("backdropNav");
    document.getElementById("mobileMenuBtn").addEventListener("click", () => {
      sidebar.classList.add("open");
      backdrop.classList.add("show");
    });
    backdrop.addEventListener("click", () => {
      sidebar.classList.remove("open");
      backdrop.classList.remove("show");
    });

    // Rota inicial (hash ou dashboard)
    const hash = (location.hash || "#dashboard").replace("#", "");
    this.navigate(VIEWS[hash] ? hash : "dashboard");

    window.addEventListener("hashchange", () => {
      const h = (location.hash || "#dashboard").replace("#", "");
      if (VIEWS[h] && h !== this.current) this.navigate(h);
    });
  },

  navigate(viewName) {
    if (!VIEWS[viewName]) viewName = "dashboard";
    this.current = viewName;

    // Atualiza sidebar ativa
    document.querySelectorAll(".nav-item").forEach(i => {
      i.classList.toggle("active", i.dataset.view === viewName);
    });

    // Atualiza títulos
    const meta = VIEWS[viewName];
    document.getElementById("pageTitle").textContent = meta.titulo;
    document.getElementById("pageSubtitle").textContent = meta.subtitulo;

    // Fecha sidebar mobile
    document.getElementById("sidebar").classList.remove("open");
    document.getElementById("backdropNav").classList.remove("show");

    // Atualiza hash e renderiza
    location.hash = viewName;
    meta.modulo.render();
  },
};

document.addEventListener("DOMContentLoaded", () => Router.init());
