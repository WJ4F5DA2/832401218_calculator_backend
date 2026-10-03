"""HTTP API routes for the calculator back end."""
from flask import Blueprint, jsonify, request

from src.service.history_service import (
    CalculationError,
    calculate,
    clear_history,
    delete_history,
    get_history,
)

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/health", methods=["GET"])
def health():
    """Simple health check used to verify the service is running."""
    return jsonify({"success": True, "message": "Calculator back end is running"})


@bp.route("/calculate", methods=["POST"])
def calculate_route():
    """Evaluate an expression sent by the front end and store the record."""
    body = request.get_json(silent=True) or {}
    expression = body.get("expression")
    try:
        record = calculate(expression)
    except CalculationError as exc:
        return jsonify({"success": False, "message": exc.message}), 400
    return (
        jsonify(
            {
                "success": True,
                "expression": record["expression"],
                "result": record["result"],
                "id": record["id"],
                "created_at": record["created_at"],
            }
        ),
        200,
    )


@bp.route("/history", methods=["GET"])
def history_route():
    """Return all calculation history records, newest first."""
    return jsonify({"success": True, "history": get_history()}), 200


@bp.route("/history/<int:record_id>", methods=["DELETE"])
def delete_history_route(record_id):
    """Delete one history record by id."""
    try:
        delete_history(record_id)
    except CalculationError as exc:
        return jsonify({"success": False, "message": exc.message}), 404
    return "", 204


@bp.route("/history", methods=["DELETE"])
def clear_history_route():
    """Delete all history records."""
    deleted = clear_history()
    return jsonify({"success": True, "deleted": deleted}), 200
