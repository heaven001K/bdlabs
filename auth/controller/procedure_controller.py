from flask import Blueprint, jsonify, request
from auth.dao.procedure_dao import ProcedureDao

procedure_bp = Blueprint('procedure_bp', __name__)

@procedure_bp.route('/test/insert_nonames', methods=['GET'])
def test_insert_nonames():
    try:
        ProcedureDao.insert_nonames()  # Викликає процедуру без параметрів
        return jsonify({"success": True, "message": "Procedure insert_nonames виконана успішно!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@procedure_bp.route('/procedure/insert_ticket_flight', methods=['POST'])
def call_insert_ticket_flight():
    from flask import request

    # Отримуємо дані з тіла запиту
    data = request.get_json()
    ticket_id = data.get('ticket_id')
    flight_id = data.get('flight_id')

    # Перевіряємо, чи всі необхідні параметри передані
    if not all([ticket_id, flight_id]):
        return jsonify({"success": False, "error": "Missing required parameters: ticket_id or flight_id"}), 400

    # Викликаємо DAO
    success, error_message = ProcedureDao.insert_ticket_flight(ticket_id, flight_id)

    if success:
        return jsonify({"success": True, "message": "Procedure InsertTicketFlight виконана успішно!"}), 200
    else:
        return jsonify({"success": False, "error": error_message}), 500

@procedure_bp.route('/get_column_aggregate', methods=['GET'])
def get_column_aggregate():
    try:
        # Отримуємо параметри з запиту
        table_name = request.args.get('table_name')
        column_name = request.args.get('column_name')
        operation = request.args.get('operation')

        # Вивести значення параметрів для перевірки
        print(f"Table: {table_name}, Column: {column_name}, Operation: {operation}")

        # Перевірка на наявність параметрів
        if not table_name or not column_name or not operation:
            return jsonify({"success": False, "error": "Missing parameters"}), 400

        # Викликаємо процедуру через DAO
        result = ProcedureDao.get_column_aggregate(table_name.strip(), column_name.strip(), operation.strip().upper())

        if result is not None:
            return jsonify({"success": True, "result": result})
        else:
            return jsonify({"success": False, "error": "Error occurred while fetching aggregate result"}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@procedure_bp.route('/create_databases_and_tables', methods=['POST'])
def create_databases_and_tables():
    try:
        # Викликаємо метод DAO для запуску процедури
        result, error = ProcedureDao.create_databases_and_tables()

        if result:
            return jsonify({'message': 'Databases and tables created successfully!'}), 200
        else:
            return jsonify({'error': f'Failed to create databases and tables: {error}'}), 500

    except Exception as e:
        return jsonify({'error': f"Server error: {str(e)}"}), 500

