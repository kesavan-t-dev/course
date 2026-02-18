from flask import Blueprint, request
from .services import staff_availability

staff_avail_bp = Blueprint('staff_avail_bp', __name__)

@staff_avail_bp.route('/staff-availability', methods=['POST'])
def add_availability():
    data = request.get_json(force=True)
    return staff_availability(data)