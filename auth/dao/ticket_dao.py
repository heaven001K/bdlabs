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

        # Запит для отримання рейсів користувача, з включенням інформації про аеропорти та авіакомпанії
        query = '''
            SELECT f.flight_number, f.departure_time, f.arrival_time, a1.name AS departure_airport, a2.name AS arrival_airport, al.name AS airline
            FROM flights f
            JOIN tickets t ON t.flight_id = f.flight_id
            JOIN airports a1 ON f.departure_airport_id = a1.airport_id
            JOIN airports a2 ON f.arrival_airport_id = a2.airport_id
            JOIN airlines al ON f.airline_id = al.airline_id
            WHERE t.user_id = %s
        '''
        cursor.execute(query, (user_id,))
        flights = cursor.fetchall()

        cursor.close()

        # Формування списку результатів
        return [
            {
                'flight_number': flight[0],
                'departure_time': flight[1],
                'arrival_time': flight[2],
                'departure_airport': flight[3],
                'arrival_airport': flight[4],
                'airline': flight[5]
            }
            for flight in flights
        ]

    @staticmethod
    def get_users_for_flight(flight_id):
        conn = g.mysql.connection
        cursor = conn.cursor()

        # Запит для отримання всіх користувачів для конкретного рейсу
        query = '''
            SELECT u.user_id, u.username, u.email
            FROM users u
            JOIN tickets t ON t.user_id = u.user_id
            WHERE t.flight_id = %s
        '''
        cursor.execute(query, (flight_id,))
        users = cursor.fetchall()

        cursor.close()

        # Формування списку результатів
        return [
            {
                'user_id': user[0],
                'username': user[1],
                'email': user[2]
            }
            for user in users
        ]

    @staticmethod
    def get_tickets():
        conn = g.mysql.connection
        cursor = conn.cursor()

        # Запит на отримання всіх записів зі стикувальної таблиці
        query = '''
            SELECT tickets.ticket_id, tickets.user_id, tickets.flight_id
            FROM tickets
        '''
        cursor.execute(query)
        tickets = cursor.fetchall()

        cursor.close()

        # Повертаємо список, який містить всі записи з таблиці tickets
        return [
            {
                'ticket_id': ticket[0],
                'user_id': ticket[1],
                'flight_id': ticket[2]
            }
            for ticket in tickets
        ]
