from flask import Blueprint, jsonify
from database.connection import get_connection

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard/stats", methods=["GET"])
def estatisticas():
    """Agrega totais para os cards do dashboard e proximos agendamentos."""
    conexao = get_connection()
    stats = {
        "total_espacos": 0,
        "total_clientes": 0,
        "reservas_hoje": 0,
        "faturamento": 0.0,
        "agendamentos_pagos": 0,
        "agendamentos_pendentes": 0,
    }
    proximos = []

    if not conexao:
        return jsonify(stats)

    try:
        cursor = conexao.cursor()

        cursor.execute("SELECT COUNT(*) FROM Espaco")
        stats["total_espacos"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Cliente")
        stats["total_clientes"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Agendamento WHERE data_reserva = CURRENT_DATE")
        stats["reservas_hoje"] = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(valor_total), 0) FROM Pagamento WHERE status = 'Pago'")
        stats["faturamento"] = float(cursor.fetchone()[0])

        cursor.execute("SELECT COUNT(*) FROM Pagamento WHERE status = 'Pago'")
        stats["agendamentos_pagos"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Pagamento WHERE status = 'Pendente'")
        stats["agendamentos_pendentes"] = cursor.fetchone()[0]

        # Proximos agendamentos (a partir de hoje)
        cursor.execute("""
            SELECT a.id_agendamento, a.data_reserva, a.hora_inicio, a.hora_fim,
                   c.nome AS cliente, e.nome AS espaco, p.status
            FROM Agendamento a
            JOIN Cliente c ON a.id_cliente = c.id_cliente
            JOIN Espaco e ON a.id_espaco = e.id_espaco
            LEFT JOIN Pagamento p ON p.id_agendamento = a.id_agendamento
            WHERE a.data_reserva >= CURRENT_DATE
            ORDER BY a.data_reserva ASC, a.hora_inicio ASC
            LIMIT 6
        """)
        for linha in cursor.fetchall():
            proximos.append({
                "id_agendamento": linha[0],
                "data_reserva": linha[1].isoformat() if linha[1] else None,
                "hora_inicio": linha[2].strftime("%H:%M") if linha[2] else None,
                "hora_fim": linha[3].strftime("%H:%M") if linha[3] else None,
                "cliente": linha[4],
                "espaco": linha[5],
                "status": linha[6] or "Sem pagamento",
            })

    finally:
        cursor.close()
        conexao.close()

    stats["proximos_agendamentos"] = proximos
    return jsonify(stats)
