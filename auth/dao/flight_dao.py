from auth.dto.flight_dto import FlightDTO

from flask import g
from collections import defaultdict
from itertools import groupby

from auth.dto.user_dto import UserDTO


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
    def get_flights_by_aircraft_and_country():
        conn = g.mysql.connection
        with conn.cursor() as cursor:
            query = '''
                    SELECT 
                        flight_number,
                        departure.location AS departure_city,
                        departure.location AS departure_country
                    FROM flights
                    JOIN airports AS departure ON flights.departure_airport_id = departure.airport_id
                    ORDER BY departure.location
                '''
            cursor.execute(query)
            flights = cursor.fetchall()

        # Перетворення результатів у список словників
        flights_list = [
            {
                'flight_number': flight[0],
                'departure_country': flight[2].split(',')[-1].strip()  # Отримуємо країну з location
            }
            for flight in flights if flight
        ]

        # Групуємо за країною відправлення
        grouped_flights = defaultdict(list)
        for flight in flights_list:
            grouped_flights[flight['departure_country']].append(flight)

        return dict(grouped_flights)