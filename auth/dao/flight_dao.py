from auth.dto.flight_dto import FlightDTO
from flask import g
from collections import defaultdict
from itertools import groupby

class FlightDAO:
    @staticmethod
    def get_all_flights():
        conn = g.mysql.connection  # Отримуємо з'єднання з базою даних
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM flights')
        flights = cursor.fetchall()  # Зберігаємо результати в змінну
        cursor.close()  # Закриваємо курсор

        return [
            FlightDTO(flight[0], flight[1], flight[2], flight[3], flight[4]) for flight in flights
        ]

    @staticmethod
    def delete_flight(flight_id):
            conn = g.mysql.connection
            cursor = conn.cursor()
            cursor.execute('DELETE FROM flights WHERE flight_id = %s', (flight_id,))
            conn.commit()
            cursor.close()

    @staticmethod
    def get_flights_grouped_by_city():
        conn = g.mysql.connection
        cursor = conn.cursor()

        query = '''
            SELECT 
                departure.location AS departure_city,
                arrival.location AS arrival_city,
                flight_number,
                departure_time,
                arrival_time
            FROM flights
            JOIN airports AS departure ON flights.departure_airport_id = departure.airport_id
            JOIN airports AS arrival ON flights.arrival_airport_id = arrival.airport_id
            ORDER BY departure.location, arrival.location
        '''
        cursor.execute(query)
        flights = cursor.fetchall()

        # Перетворення результатів у список словників
        flights_list = [
            {
                'departure_city': flight[0],
                'arrival_city': flight[1],
                'flight_number': flight[2],
                'departure_time': flight[3],
                'arrival_time': flight[4]
            }
            for flight in flights
        ]

        cursor.close()

        # Групуємо за містом відправлення
        grouped_flights = defaultdict(list)
        for flight in flights_list:
            grouped_flights[flight['departure_city']].append(flight)

        return dict(grouped_flights)