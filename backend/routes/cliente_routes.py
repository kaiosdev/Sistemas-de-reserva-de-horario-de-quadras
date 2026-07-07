from flask import Blueprint, request, jsonify
from services.cliente_service import ClienteService

cliente_bp = Blueprint("clientes", __name__)
service = ClienteService()


@cliente_bp.route("/clientes", methods=["GET"])
def listar_clientes():
    # Se receber ?q=termo, faz busca por criterio (CPF ou nome)
    q = (request.args.get("q") or "").strip()
    if q:
        clientes = service.buscar(q)
    else:
        clientes = service.listar_clientes()
    return jsonify([
        {
            "id_cliente": c.id_cliente,
            "nome": c.nome,
            "cpf": c.cpf,
            "endereco": c.endereco,
            "telefone": c.telefone,
        }
        for c in clientes
    ])


@cliente_bp.route("/clientes", methods=["POST"])
def criar_cliente():
    dados = request.get_json(silent=True) or {}
    nome = (dados.get("nome") or "").strip()
    cpf = (dados.get("cpf") or "").strip()
    endereco = (dados.get("endereco") or "").strip()
    telefone = (dados.get("telefone") or "Nao informado").strip()

    if not nome or not cpf:
        return jsonify({"erro": "Nome e CPF sao obrigatorios."}), 400

    try:
        texto = f"0, {nome}, {cpf}, {endereco}, {telefone}"
        service.cadastrar_cliente_texto(texto)
        return jsonify({"mensagem": "Cliente cadastrado com sucesso."}), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@cliente_bp.route("/clientes/<int:id_cliente>", methods=["PUT"])
def atualizar_cliente(id_cliente):
    dados = request.get_json(silent=True) or {}
    try:
        ok = service.atualizar(
            id_cliente=id_cliente,
            nome=dados.get("nome"),
            cpf=dados.get("cpf"),
            endereco=dados.get("endereco"),
            telefone=dados.get("telefone"),
        )
        if ok:
            return jsonify({"mensagem": "Cliente atualizado com sucesso."})
        return jsonify({"erro": "Cliente nao encontrado."}), 404
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@cliente_bp.route("/clientes/<int:id_cliente>", methods=["DELETE"])
def deletar_cliente(id_cliente):
    try:
        ok = service.excluir(id_cliente)
        if ok:
            return jsonify({"mensagem": "Cliente excluido."})
        return jsonify({"erro": "Cliente nao encontrado."}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
