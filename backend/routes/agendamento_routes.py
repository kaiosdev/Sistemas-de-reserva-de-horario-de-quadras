from flask import Blueprint, request, jsonify
from services.agendamento_service import AgendamentoService

agendamento_bp = Blueprint("agendamentos", __name__)
service = AgendamentoService()


@agendamento_bp.route("/agendamentos", methods=["GET"])
def listar_agendamentos():
    return jsonify(service.listar_todos())


@agendamento_bp.route("/agendamentos", methods=["POST"])
def criar_agendamento():
    dados = request.get_json(silent=True) or {}
    try:
        novo_id = service.criar(
            id_cliente=dados.get("id_cliente"),
            id_espaco=dados.get("id_espaco"),
            data_reserva=dados.get("data_reserva"),
            hora_inicio=dados.get("hora_inicio"),
            hora_fim=dados.get("hora_fim"),
        )
        return jsonify({
            "mensagem": "Agendamento realizado com sucesso.",
            "id_agendamento": novo_id,
        }), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@agendamento_bp.route("/agendamentos/<int:id_agendamento>", methods=["PUT"])
def atualizar_agendamento(id_agendamento):
    dados = request.get_json(silent=True) or {}
    try:
        ok = service.atualizar(
            id_agendamento=id_agendamento,
            id_cliente=dados.get("id_cliente"),
            id_espaco=dados.get("id_espaco"),
            data_reserva=dados.get("data_reserva"),
            hora_inicio=dados.get("hora_inicio"),
            hora_fim=dados.get("hora_fim"),
        )
        if ok:
            return jsonify({"mensagem": "Agendamento atualizado com sucesso."})
        return jsonify({"erro": "Agendamento nao encontrado."}), 404
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@agendamento_bp.route("/agendamentos/<int:id_agendamento>", methods=["DELETE"])
def deletar_agendamento(id_agendamento):
    try:
        ok = service.excluir(id_agendamento)
        if ok:
            return jsonify({"mensagem": "Agendamento excluido."})
        return jsonify({"erro": "Agendamento nao encontrado."}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
