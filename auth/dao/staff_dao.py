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
    def get_all_staff_with_airline():
        """
        Повертає всіх співробітників із деталями авіакомпанії.
        """
        conn = g.mysql.connection
        cursor = conn.cursor()
        query = """
        SELECT 
            staff.staff_id, 
            staff.airline_id, 
            airlines.name AS airline_name, 
            staff.first_name, 
            staff.last_name, 
            staff.position, 
            staff.hire_date, 
            staff.created_at
        FROM 
            staff
        INNER JOIN 
            airlines ON staff.airline_id = airlines.airline_id
        """
        cursor.execute(query)
        staff = cursor.fetchall()
        cursor.close()

        return [
            {
                "staff_id": row[0],
                "airline_id": row[1],
                "airline_name": row[2],
                "first_name": row[3],
                "last_name": row[4],
                "position": row[5],
                "hire_date": row[6],
                "created_at": row[7]
            } for row in staff
        ]