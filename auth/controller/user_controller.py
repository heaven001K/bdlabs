# У файлі auth/controller/user_controller.py

from flask import Blueprint, jsonify, request
from auth.dao.user_dao import UserDAO

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user_dto = UserDAO.create_user(data['username'], data['email'], data['password'])
    return jsonify(user_dto.to_dict()), 201

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = UserDAO.get_all_users()  # This now returns a list of UserDTO instances
    return jsonify([user.to_dict() for user in users]), 200  # Convert to dictionary for JSON

@user_bp.route('/users/insert', methods=['POST'])
def insert_user():
    try:
        # Очікуємо отримання JSON-запиту
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password_hash = data.get("password_hash")

        # Перевірка вхідних даних
        if not all([username, email, password_hash]):
            return jsonify({"success": False, "message": "All fields are required"}), 400

        # Виклик процедури через DAO
        result = UserDAO.insert_into_users(username, email, password_hash)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
