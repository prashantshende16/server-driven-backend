from typing import Any, Optional, Dict

def success_response(data: Any = None, message: str = None) -> Dict[str, Any]:
    return {
        "success": True,
        "data": data if data is not None else {},
        "message": message
    }

def error_response(message: str, errors: list = None) -> Dict[str, Any]:
    return {
        "success": False,
        "data": None,
        "message": message,
        "errors": errors or []
    }

