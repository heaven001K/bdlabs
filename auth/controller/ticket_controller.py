from flask import Blueprint, request, jsonify
from datetime import datetime
from auth.dao.ticket_dao import TicketDAO  # Імпортуйте TicketDAO
from auth.service.flight_service import Service
tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/', methods=['GET'])
def get_all_tickets():
    tickets = TicketDAO.get_all_tickets()
    # Перетворюємо кожен квиток у словник за допомогою to_dict()
    tickets_dict = [ticket.to_dict() for ticket in tickets]
    return jsonify({"tickets": tickets_dict}), 200


@tickets_bp.route('/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    data = request.json
    user_id = data.get('user_id')
    flight_id = data.get('flight_id')
    purchase_date = data.get('purchase_date')
    price = data.get('price')

    # Перевірка необхідних полів
    if not all([user_id, flight_id, purchase_date, price]):
        return jsonify({"error": "Missing required fields"}), 400

    # Конвертація purchase_date у формат datetime
    try:
        purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Оновлення квитка через DAO
    updated_ticket = TicketDAO.update_ticket(ticket_id, user_id, flight_id, purchase_date, price)

    return jsonify({"message": "Ticket updated successfully", "updated_ticket": updated_ticket.to_dict()}), 200

@tickets_bp.route('/user/<int:user_id>/flights', methods=['GET'])
def get_flights_for_user(user_id):
    flights = Service.get_flights_for_user(user_id)
    return jsonify(flights)

# Отримати всіх користувачів для рейсу
@tickets_bp.route('/flight/<int:flight_id>/users', methods=['GET'])
def get_users_for_flight(flight_id):
    users = Service.get_users_for_flight(flight_id)
    return jsonify(users)