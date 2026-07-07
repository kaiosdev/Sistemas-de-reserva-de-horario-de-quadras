from flask import Blueprint, request, jsonify
from services.espaco_service import EspacoService

espaco_bp = Blueprint("espacos", __name__)
service = EspacoService()


@espaco_bp.route("/espacos", methods=["GET"])
def listar_espacos():
    espacos = service.listar_todos()
    return jsonify([
        {
            "id_espaco": e.id_espaco,
            "nome": e.nome,
            "descricao": e.descricao,
            "tamanho_quadra": e.tamanho_quadra,
            "valor_hora": e.valor_hora,
            "id_modalidade": e.id_modalidade,
            "modalidade": e.modalidade_nome or "Geral",
        }
        for e in espacos
    ])


@espaco_bp.route("/espacos", methods=["POST"])
def criar_espaco():
    dados = request.get_json(silent=True) or {}
    try:
        service.cadastrar(
            nome=dados.get("nome"),
            valor_hora=dados.get("valor_hora"),
            descricao=dados.get("descricao"),
            tamanho_quadra=dados.get("tamanho_quadra"),
            id_modalidade=dados.get("id_modalidade", 1),
        )
        return jsonify({"mensagem": "Espaco cadastrado com sucesso."}), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@espaco_bp.route("/espacos/<int:id_espaco>", methods=["PUT"])
def atualizar_espaco(id_espaco):
    dados = request.get_json(silent=True) or {}
    try:
        ok = service.atualizar(
            id_espaco=id_espaco,
            nome=dados.get("nome"),
            valor_hora=dados.get("valor_hora"),
            descricao=dados.get("descricao"),
            tamanho_quadra=dados.get("tamanho_quadra"),
            id_modalidade=dados.get("id_modalidade", 1),
        )
        if ok:
            return jsonify({"mensagem": "Espaco atualizado com sucesso."})
        return jsonify({"erro": "Espaco nao encontrado."}), 404
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@espaco_bp.route("/espacos/<int:id_espaco>", methods=["DELETE"])
def deletar_espaco(id_espaco):
    try:
        ok = service.excluir(id_espaco)
        if ok:
            return jsonify({"mensagem": "Espaco excluido."})
        return jsonify({"erro": "Espaco nao encontrado."}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
