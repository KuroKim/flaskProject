from flask import Flask, render_template
from tools.calculator import calculator_bp
from tools.pressure_converter import pressure_converter_bp
from tools.currency import currency_bp
from tools.fuel_calculator import fuel_calculator_bp
from tools.converter import converter_bp
from tools.weather import weather_bp
from tools.qr_code import qr_code_bp
from tools.timer import timer_bp
import requests
from cachetools import TTLCache

app = Flask(__name__)

# Настройка кэша с TTL (Time To Live) — 1 час
cache = TTLCache(maxsize=1, ttl=3600)  # 3600 секунд = 1 час


def get_exchange_rates():
    if 'exchange_rates' not in cache:
        try:
            response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
            response.raise_for_status()
            data = response.json()
            rates = {
                'USD': data['Valute']['USD']['Value'] / data['Valute']['USD']['Nominal'],
                'EUR': data['Valute']['EUR']['Value'] / data['Valute']['EUR']['Nominal'],
                'RUB': 1.0
            }
            cache['exchange_rates'] = rates
            print(f"Курсы валют обновлены: {rates}")
        except Exception as e:
            print(f"Ошибка загрузки курсов: {e}")
            # Условные курсы на случай ошибки
            rates = {'USD': 96.0, 'EUR': 105.0, 'RUB': 1.0}
            cache['exchange_rates'] = rates
    return cache['exchange_rates']


# Регистрация Blueprint'ов
app.register_blueprint(calculator_bp)
app.register_blueprint(pressure_converter_bp)
app.register_blueprint(currency_bp)
app.register_blueprint(fuel_calculator_bp)
app.register_blueprint(converter_bp)
app.register_blueprint(weather_bp)
app.register_blueprint(qr_code_bp)
app.register_blueprint(timer_bp)


@app.route('/')
def index():
    tools = [
        {"name": "Калькулятор", "url": "/calculator", "icon": "calculator"},
        {"name": "Конвертер валют", "url": "/currency", "icon": "currency"},
        {"name": "Конвертер величин", "url": "/converter", "icon": "converter"},
        {"name": "BAR ↔ PSI", "url": "/pressure_converter", "icon": "pressure"},
        {"name": "Таймер", "url": "/timer", "icon": "timer"},
        {"name": "Погода", "url": "/weather", "icon": "weather"},
        {"name": "QR-код", "url": "/qr-code", "icon": "qr"},
        {"name": "Калькулятор бензина", "url": "/fuel-calculator", "icon": "fuel"}
    ]
    return render_template('index.html', tools=tools)


if __name__ == '__main__':
    app.run(debug=True)
