from flask import Flask, jsonify,g
from flask_mysqldb import MySQL
from auth.dao.user_dao import UserDAO
from auth.controller.user_controller import user_bp
from auth.controller.flight_controller import flight_bp
from auth.controller.ticket_controller import tickets_bp
from auth.controller.aircraft_controller import aircrafts_bp
from auth.controller.procedure_controller import procedure_bp
from auth.controller.staff_controller import staff_bp
from auth.controller.airport_controller import airports_bp
# Реєстрація контролера staff


app = Flask(__name__)

# Налаштування бази даних
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'  # Замініть на ваше ім'я користувача
app.config['MYSQL_PASSWORD'] = 'kunica001_K'  # Замініть на ваш пароль
app.config['MYSQL_DB'] = 'airlinedb'  # Замініть на вашу базу даних

mysql = MySQL(app)


@app.before_request
def before_request():
    g.mysql = mysql

@app.route('/')
def home():
    return "Welcome to the Airline Database API!"


app.register_blueprint(aircrafts_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(flight_bp, url_prefix='/api')
app.register_blueprint(tickets_bp, url_prefix='/api/tickets')
app.register_blueprint(procedure_bp, url_prefix='/api/procedures')
app.register_blueprint(staff_bp, url_prefix='/api')
app.register_blueprint(airports_bp, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True)






