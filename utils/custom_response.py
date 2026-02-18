from flask import jsonify

def custom_response(message, status_code, data=None):
    return jsonify({
        "status": f"{status_code}" if status_code < 400 else f"{status_code}",
        "message": message,
        "data": data
    }), status_code