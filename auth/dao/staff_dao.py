from flask import g

class StaffDAO:
    @staticmethod
    def get_all_staff():
        conn = g.mysql.connection
        cursor = conn.cursor()
        query = "SELECT staff_id, airline_id, first_name, last_name, position, hire_date, created_at FROM staff"
        cursor.execute(query)
        staff = cursor.fetchall()
        cursor.close()

        return [
            {
                "staff_id": row[0],
                "airline_id": row[1],
                "first_name": row[2],
                "last_name": row[3],
                "position": row[4],
                "hire_date": row[5],
                "created_at": row[6]
            } for row in staff
        ]

    @staticmethod
    def insert_staff(airline_id, first_name, last_name, position, hire_date):
        conn = g.mysql.connection
        cursor = conn.cursor()

        try:
            query = """
                INSERT INTO staff (airline_id, first_name, last_name, position, hire_date)
                VALUES (%s, %s, %s, %s, %s)
                """
            cursor.execute(query, (airline_id, first_name, last_name, position, hire_date))
            conn.commit()
            return True  # Повертаємо True у разі успіху
        except Exception as e:
            conn.rollback()
            return False, str(e)  # Повертаємо False і повідомлення про помилку
        finally:
            cursor.close()

    @staticmethod
    def delete_staff(staff_id):
        conn = g.mysql.connection
        cursor = conn.cursor()

        try:
            query = "DELETE FROM staff WHERE staff_id = %s"
            cursor.execute(query, (staff_id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()

    @staticmethod
    def get_airlines_with_staff():
        """
        Повертає всі авіакомпанії з їхніми працівниками.
        """
        conn = g.mysql.connection
        cursor = conn.cursor()

        # Перший запит для отримання всіх авіакомпаній
        query_airlines = "SELECT airline_id, name FROM airlines"
        cursor.execute(query_airlines)
        airlines = cursor.fetchall()

        result = []

        # Для кожної авіакомпанії отримуємо працівників
        for airline in airlines:
            airline_id = airline[0]
            airline_name = airline[1]

            # Запит для отримання працівників авіакомпанії
            query_staff = """
                    SELECT staff_id, first_name, last_name, position, hire_date, created_at
                    FROM staff WHERE airline_id = %s
                """
            cursor.execute(query_staff, (airline_id,))
            staff = cursor.fetchall()

            # Формуємо структуру даних для відповіді
            staff_list = [
                {
                    "staff_id": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "position": row[3],
                    "hire_date": row[4],
                    "created_at": row[5]
                } for row in staff
            ]

            result.append({
                "airline_id": airline_id,
                "airline_name": airline_name,
                "staff": staff_list
            })

        cursor.close()
        return result
