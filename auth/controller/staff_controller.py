from flask import Blueprint, request, jsonify, g
from auth.dao.staff_dao import StaffDAO

# Створення Blueprint для staff
staff_bp = Blueprint('staff', __name__)

# Отримуємо всіх співробітників
@staff_bp.route('/staff', methods=['GET'])
def get_all_staff():
    staff = StaffDAO.get_all_staff()
    return jsonify(staff), 200

# Додаємо нового співробітника
@staff_bp.route('/staff', methods=['POST'])
def add_staff():
    try:
        data = request.get_json()

        # Отримуємо значення з запиту
        airline_id = data.get('airline_id')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        position = data.get('position')
        hire_date = data.get('hire_date')

        # Перевірка, чи всі необхідні поля надіслані
        if not all([airline_id, first_name, last_name, position, hire_date]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Викликаємо метод DAO для вставки даних
        result = StaffDAO.insert_staff(airline_id, first_name, last_name, position, hire_date)

        if result is True:
            return jsonify({'message': 'Staff member added successfully!'}), 201
        else:
            # Якщо вставка не вдалася, повертаємо помилку з описом
            return jsonify({'error': f'Failed to add staff member: {result[1]}'}), 500

    except Exception as e:
        # Обробка помилок сервера
        return jsonify({'error': f"Server error: {str(e)}"}), 500


# Видаляємо співробітника
@staff_bp.route('/staff/<int:staff_id>', methods=['DELETE'])
def delete_staff(staff_id):
    result = StaffDAO.delete_staff(staff_id)
    if result is True:
        return jsonify({'message': 'Staff member deleted successfully!'}), 200
    else:
        return jsonify({'error': f'Failed to delete staff member: {result[1]}'}), 500

# Отримуємо список співробітників разом з авіакомпаніями
@staff_bp.route('/airlines_with_staff', methods=['GET'])
def get_airlines_with_staff():
    """
    Повертає всі авіакомпанії з їхніми працівниками.
    """
    airlines_with_staff = StaffDAO.get_airlines_with_staff()
    return jsonify(airlines_with_staff), 200
