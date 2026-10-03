"""Business logic for calculation history records."""
from src.model import database
from src.service.calculator_service import ExpressionError, evaluate


class CalculationError(Exception):
    """Raised when a calculation request is invalid or fails."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


def calculate(expression):
    """Validate, evaluate and persist one calculation.

    Returns:
        A dict with the stored record: id, expression, result, created_at.

    Raises:
        CalculationError: For empty input, invalid expressions or
            division by zero.
    """
    if not isinstance(expression, str) or not expression.strip():
        raise CalculationError("Empty expression")
    try:
        result = evaluate(expression)
    except ExpressionError as exc:
        raise CalculationError(str(exc)) from exc
    return database.insert_record(expression.strip(), result)


def get_history():
    """Return all calculation history records, newest first."""
    return database.fetch_all_records()


def delete_history(record_id):
    """Delete one history record.

    Returns:
        True if the record existed and was deleted.

    Raises:
        CalculationError: If no record exists with the given id.
    """
    if database.delete_record(record_id):
        return True
    raise CalculationError("History record not found: id=%s" % record_id)


def clear_history():
    """Delete all history records and return the number removed."""
    return database.clear_all_records()
