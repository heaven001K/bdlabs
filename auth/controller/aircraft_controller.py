from flask import Blueprint, jsonify,request
from auth.dao.aircraft_dao import AircraftDAO

aircrafts_bp = Blueprint('aircrafts_bp', __name__)

@aircrafts_bp.route('/aircrafts/<int:aircraft_id>', methods=['DELETE'])
def delete_aircraft(aircraft_id):
    try:
        # Викликаємо метод DAO для видалення літака
        AircraftDAO.delete_aircraft(aircraft_id)
        return jsonify({'message': 'Aircraft deleted successfully'}), 200
    except Exception as e:
        # Обробка помилок
        return jsonify({'error': str(e)}), 500

@aircrafts_bp.route('/aircraft', methods=['GET'])
def get_aircraft():
    try:
        # Викликаємо метод DAO для отримання даних з БД
        aircraft = AircraftDAO.get_aircraft()

        # Перевірка, чи є дані
        if not aircraft:
            return jsonify({'message': 'No aircraft found'}), 404

        return jsonify(aircraft), 200  # Повертаємо список літаків у форматі JSON

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@aircrafts_bp.route('/aircrafts', methods=['POST'])
def add_aircraft():
    data = request.get_json()  # Отримуємо дані з запиту

    model = data.get('model')
    capacity = data.get('capacity')
    airlines_airline_id = data.get('airlines_airline_id')

    # Перевірка, чи всі необхідні поля надано
    if not all([model, capacity, airlines_airline_id]):
        return jsonify({'error': 'Missing required fields'}), 400

    # Викликаємо метод DAO для додавання нового літака
    result = AircraftDAO.add_aircraft(model, capacity, airlines_airline_id)

    if result is True:
        return jsonify({'message': 'Aircraft added successfully'}), 201
    else:
        return jsonify({'error': f'Failed to add aircraft: {result[1]}'}), 500

@aircrafts_bp.route('/aircrafts/<int:aircraft_id>', methods=['PUT'])
def update_aircraft(aircraft_id):
    try:
        # Отримуємо дані з тіла запиту
        data = request.get_json()

        model = data.get('model')
        capacity = data.get('capacity')
        airline_id = data.get('airlines_airline_id')

        # Перевірка, чи всі необхідні поля присутні
        if not all([model, capacity, airline_id]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Викликаємо метод DAO для оновлення літака
        AircraftDAO.update_aircraft(aircraft_id, model, capacity, airline_id)

        return jsonify({'message': 'Aircraft updated successfully'}), 200

    except Exception as e:
        # Обробка помилок
        return jsonify({'error': str(e)}), 500


