from flask import g
from datetime import datetime
from auth.dto.ticket_dto import TicketDTO


class TicketDAO:
    @staticmethod
    def get_all_tickets():
            conn = g.mysql.connection  # Отримуємо підключення до бази даних із глобального контексту Flask
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tickets')
            tickets = cursor.fetchall()
            cursor.close()

            # Повертаємо список об'єктів TicketDTO
            return [TicketDTO(ticket[0], ticket[1], ticket[2], ticket[3], ticket[4]) for ticket in tickets]
    @staticmethod
    def update_ticket(ticket_id, user_id, flight_id, purchase_date, price):
        conn = g.mysql.connection
        cursor = conn.cursor()

        cursor.execute(
            '''
            UPDATE tickets
            SET user_id = %s, flight_id = %s, purchase_date = %s, price = %s
            WHERE ticket_id = %s
            ''',
            (user_id, flight_id, purchase_date, price, ticket_id)
        )
        conn.commit()
        cursor.close()

        return TicketDTO(ticket_id, user_id, flight_id, purchase_date, price)

    @staticmethod
    def get_flights_for_user(user_id):
        conn = g.mysql.connection
        cursor = conn.cursor()

        query = '''
                SELECT flights.flight_number, flights.departure_time, flights.arrival_time, flights.departure_airport_id, flights.arrival_airport_id
                FROM flights
                JOIN tickets ON tickets.flight_id = flights.flight_id
                WHERE tickets.user_id = %s
            '''
        cursor.execute(query, (user_id,))
        flights = cursor.fetchall()

        cursor.close()

        return [
            {
                'flight_number': flight[0],
                'departure_time': flight[1],
                'arrival_time': flight[2],
                'departure_airport_id': flight[3],
                'arrival_airport_id': flight[4]
            }
            for flight in flights
        ]

    @staticmethod
    def get_users_for_flight(flight_id):
        conn = g.mysql.connection
        cursor = conn.cursor()

        query = '''
                SELECT users.user_id, users.username, users.email
                FROM users
                JOIN tickets ON tickets.user_id = users.user_id
                WHERE tickets.flight_id = %s
            '''
        cursor.execute(query, (flight_id,))
        users = cursor.fetchall()

        cursor.close()

        return [
            {
                'user_id': user[0],
                'username': user[1],
                'email': user[2]
            }
            for user in users
        ]