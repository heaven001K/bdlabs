from collections import defaultdict
from auth.dao.flight_dao import FlightDAO
from auth.dao.ticket_dao import TicketDAO

class Service:
    @staticmethod
    def get_all_flights():
        return FlightDAO.get_all_flights()

    @staticmethod
    def delete_flight(flight_id):
        return FlightDAO.delete_flight(flight_id)

    @staticmethod
    def get_flights_grouped_by_city():
        """Отримуємо рейси, згруповані по містах через DAO."""
        return FlightDAO.get_flights_grouped_by_city()

    @staticmethod
    def get_flights_for_user(user_id):
        return TicketDAO.get_flights_for_user(user_id)

    @staticmethod
    def get_users_for_flight(flight_id):
        return TicketDAO.get_users_for_flight(flight_id)