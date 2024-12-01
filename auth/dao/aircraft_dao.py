from flask import g

class AircraftDAO:
    @staticmethod
    def delete_aircraft(aircraft_id):
        conn = g.mysql.connection
        cursor = conn.cursor()
        cursor.execute('DELETE FROM aircrafts WHERE idaircrafts = %s', (aircraft_id,))
        conn.commit()
        cursor.close()


    @staticmethod
    def get_aircraft():
            conn = g.mysql.connection
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM aircrafts')
            aircrafts = cursor.fetchall()
            cursor.close()

            # Перевірка результатів
            if not aircrafts:
                return []

            result = []
            for row in aircrafts:
                result.append({
                    "idaircrafts": row[0],  # Ідентифікатор літака
                    "model": row[1],  # Модель літака
                    "capacity": row[2],  # Місткість літака
                    "airlines_airline_id": row[3]  # Ідентифікатор авіакомпанії
                })

            return result

    @staticmethod
    def add_aircraft(model, capacity, airlines_airline_id):
        conn = g.mysql.connection
        cursor = conn.cursor()

        try:
            # Перевірка на довжину значення model
            if len(model) > 45:
                return False, "Model name is too long (max 45 characters)"

            # Перевірка типів даних
            if not isinstance(capacity, int) or not isinstance(airlines_airline_id, int):
                return False, "Capacity and airline ID must be integers"

            query = """
                INSERT INTO aircrafts (model, capacity, airlines_airline_id)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (model, capacity, airlines_airline_id))
            conn.commit()  # Збереження змін у базі
            return True
        except Exception as e:
            conn.rollback()  # Відкат змін у випадку помилки
            return False, f"Error: {str(e)}"
        finally:
            cursor.close()

    @staticmethod
    def update_aircraft(aircraft_id, model, capacity, airline_id):
        conn = g.mysql.connection
        cursor = conn.cursor()

        # Виконуємо запит на оновлення даних
        query = """
                UPDATE aircrafts
                SET model = %s, capacity = %s, airlines_airline_id = %s
                WHERE idaircrafts = %s
            """
        cursor.execute(query, (model, capacity, airline_id, aircraft_id))
        conn.commit()
        cursor.close()



