import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from routes.modalidade_routes import modalidade_bp
from routes.espaco_routes import espaco_bp
from routes.cliente_routes import cliente_bp
from routes.agendamento_routes import agendamento_bp
from routes.pagamento_routes import pagamento_bp
from routes.dashboard_routes import dashboard_bp

# Diretório do frontend (um nível acima de backend/)
FRONTEND_DIR = PROJECT_ROOT / "frontend"


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(modalidade_bp, url_prefix="/api")
    app.register_blueprint(espaco_bp, url_prefix="/api")
    app.register_blueprint(cliente_bp, url_prefix="/api")
    app.register_blueprint(agendamento_bp, url_prefix="/api")
    app.register_blueprint(pagamento_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp, url_prefix="/api")

    # ---------- Servir o frontend diretamente ----------
    @app.route("/")
    def index():
        return send_from_directory(str(FRONTEND_DIR), "index.html")

    @app.route("/<path:caminho>")
    def servir_frontend(caminho):
        return send_from_directory(str(FRONTEND_DIR), caminho)

    @app.route("/api")
    def api_root():
        return jsonify({
            "sistema": "Athletix API",
            "status": "online",
            "endpoints": [
                "/api/modalidades",
                "/api/espacos",
                "/api/clientes",
                "/api/agendamentos",
                "/api/pagamentos",
                "/api/dashboard/stats",
            ],
        })

    @app.errorhandler(404)
    def nao_encontrado(_):
        return jsonify({"erro": "Recurso nao encontrado"}), 404

    return app


if __name__ == "__main__":
    app = create_app()
    print("=" * 60)
    print("  ATHLETIX rodando em http://127.0.0.1:5000")
    print("  Abra no navegador: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, port=5000)
