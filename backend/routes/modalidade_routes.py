from flask import Blueprint, request, jsonify
from services.modalidade_service import ModalidadeService

modalidade_bp = Blueprint("modalidades", __name__)
service = ModalidadeService()


@modalidade_bp.route("/modalidades", methods=["GET"])
def listar_modalidades():
    modalidades = service.listar_todos()
    return jsonify([
        {"id_modalidade": m.id_modalidade, "nome": m.nome}
        for m in modalidades
    ])


@modalidade_bp.route("/modalidades", methods=["POST"])
def criar_modalidade():
    dados = request.get_json(silent=True) or {}
    try:
        nova = service.cadastrar(dados.get("nome"))
        return jsonify({
            "mensagem": "Modalidade cadastrada.",
            "id_modalidade": nova.id_modalidade,
            "nome": nova.nome,
        }), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
