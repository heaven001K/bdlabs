from flask import Blueprint, jsonify, request
from auth.dao.airport_dao import AirportDAO

airports_bp = Blueprint('airports_bp', __name__)


@airports_bp.route('/test_airport_trigger', methods=['POST'])
def test_airport_trigger():
    try:
        # Отримуємо дані з POST запиту
        data = request.get_json()
        name = data.get('name')
        location = data.get('location')

        # Перевірка наявності обов'язкових параметрів
        if not name or not location:
            return jsonify({'error': 'Missing required fields'}), 400

        # Викликаємо метод DAO для додавання аеропорту
        AirportDAO.add_airport(name, location)

        return jsonify({'message': 'Airport added successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
