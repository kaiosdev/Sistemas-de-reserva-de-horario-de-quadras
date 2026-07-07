from flask import Blueprint, request, jsonify
from services.pagamento_service import PagamentoService

pagamento_bp = Blueprint("pagamentos", __name__)
service = PagamentoService()


@pagamento_bp.route("/pagamentos", methods=["GET"])
def listar_pagamentos():
    return jsonify(service.listar_todos())


@pagamento_bp.route("/pagamentos", methods=["POST"])
def processar_pagamento():
    dados = request.get_json(silent=True) or {}
    try:
        id_pagamento = service.processar(
            id_agendamento=dados.get("id_agendamento"),
            valor_total=dados.get("valor_total"),
            forma_pagamento=dados.get("forma_pagamento", "PIX"),
            status=dados.get("status", "Pago"),
        )
        return jsonify({
            "mensagem": "Pagamento processado com sucesso.",
            "id_pagamento": id_pagamento,
        }), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@pagamento_bp.route("/pagamentos/<int:id_pagamento>", methods=["PUT"])
def atualizar_pagamento(id_pagamento):
    dados = request.get_json(silent=True) or {}
    try:
        ok = service.atualizar(
            id_pagamento=id_pagamento,
            valor_total=dados.get("valor_total"),
            forma_pagamento=dados.get("forma_pagamento"),
            status=dados.get("status"),
        )
        if ok:
            return jsonify({"mensagem": "Pagamento atualizado com sucesso."})
        return jsonify({"erro": "Pagamento nao encontrado."}), 404
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@pagamento_bp.route("/pagamentos/<int:id_pagamento>", methods=["DELETE"])
def deletar_pagamento(id_pagamento):
    try:
        ok = service.excluir(id_pagamento)
        if ok:
            return jsonify({"mensagem": "Pagamento excluido."})
        return jsonify({"erro": "Pagamento nao encontrado."}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
