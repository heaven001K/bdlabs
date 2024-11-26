from flask import g

class ProcedureDao:
    """Клас для роботи із збереженими процедурами в базі даних."""

    @staticmethod
    def insert_nonames():
        conn = g.mysql.connection
        cursor = conn.cursor()
        cursor.execute('CALL insert_nonames()')  # Без параметрів
        conn.commit()
        cursor.close()

    @staticmethod
    def insert_into_users(username, email):
        """
        Викликає процедуру InsertIntoUsers.
        :param username: Ім'я користувача
        :param email: Електронна пошта користувача
        """
        conn = g.mysql.connection
        cursor = conn.cursor()
        cursor.execute('CALL InsertIntoUsers(%s, %s)', (username, email))
        conn.commit()
        cursor.close()

    @staticmethod
    def insert_ticket_flight(ticket_id, flight_id):
        conn = g.mysql.connection
        cursor = conn.cursor()

        try:
            # Викликаємо процедуру InsertTicketFlight
            cursor.callproc('InsertTicketFlight', [ticket_id, flight_id])
            conn.commit()  # Фіксуємо зміни
            return True, None  # Успішне виконання
        except Exception as e:
            conn.rollback()  # Відміняємо зміни у разі помилки
            return False, str(e)  # Повертаємо повідомлення про помилку
        finally:
            cursor.close()

    @staticmethod
    def get_column_aggregate(table_name, column_name, operation):
        try:
            conn = g.mysql.connection
            cursor = conn.cursor()

            # Виконання SQL запиту через підготовлений запит
            query = f"CALL GetColumnAggregate('{table_name}', '{column_name}', '{operation}', @result);"
            cursor.execute(query)
            cursor.execute("SELECT @result;")
            result = cursor.fetchone()[0]
            cursor.close()

            return result
        except Exception as e:
            print(f"Error in procedure execution: {str(e)}")
            return None

    @staticmethod
    def create_databases_and_tables():
        """Викликає процедуру для створення баз даних та таблиць з даними авіакомпаній."""
        conn = g.mysql.connection
        cursor = conn.cursor()

        try:
            # Викликаємо збережену процедуру
            cursor.callproc('CreateDatabasesAndTablesWithAirlinesData')

            # Якщо все пройшло успішно, робимо commit
            conn.commit()

            return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()