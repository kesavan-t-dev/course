from flask import Blueprint, request
from .services import get_all_staffs, update_staffs, delete_staffs, relieve_staffs

staff_bp = Blueprint('staff_bp', __name__)

@staff_bp.route('/staff', methods=['GET'])
def get_staff():
    return get_all_staffs()

@staff_bp.route('/staff/<string:staff_id>', methods=['PATCH'])
def update_staff(staff_id):
    data = request.get_json(force=True)
    return update_staffs(staff_id, data)

@staff_bp.route('/staff/<string:staff_id>', methods=['DELETE'])
def delete_staff(staff_id):
    return delete_staffs(staff_id)


@staff_bp.route('/staff/relieve', methods=['PATCH'])
def relieve_staff():
    data = request.get_json(force=True)
    return relieve_staffs(data)