from flask import g

class AirportDAO:
    @staticmethod
    def add_airport(name, location):
        try:
            conn = g.mysql.connection
            cursor = conn.cursor()

            # Вставка даних у таблицю airports
            cursor.execute(
                'INSERT INTO airports (name, location) VALUES (%s, %s)', (name, location)
            )
            conn.commit()
            cursor.close()

        except Exception as e:
            raise Exception(f"Failed to add airport: {str(e)}")
