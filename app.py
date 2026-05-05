from flask import Flask, abort, render_template, request
from tools.calculator import calculator_bp
from tools.pressure_converter import pressure_converter_bp
from tools.currency import currency_bp
from tools.fuel_calculator import fuel_calculator_bp
from tools.converter import converter_bp
from tools.weather import weather_bp
from tools.qr_code import qr_code_bp
from tools.timer import timer_bp
from tools.registry import (
    get_featured_tools,
    get_nav_tools,
    get_related_tools,
    get_tool_by_path,
    get_tools,
    get_tools_by_category,
)
from tools.usage_stats import configure_usage_db, get_usage_stats, increment_tool_view
import requests
from cachetools import TTLCache
import json
import os

app = Flask(__name__)
app.config["USAGE_DB_PATH"] = os.environ.get(
    "USAGE_DB_PATH",
    os.path.join(app.root_path, "data", "tool_usage.sqlite3"),
)
configure_usage_db(app.config["USAGE_DB_PATH"])

# Настройка кэша с TTL (Time To Live) — 1 час
cache = TTLCache(maxsize=1, ttl=3600)  # 3600 секунд = 1 час

# Путь к файлу для сохранения последних курсов
LAST_RATES_FILE = "last_rates.json"


def save_rates_to_file(rates):
    """Сохраняет курсы валют в файл last_rates.json"""
    try:
        with open(LAST_RATES_FILE, 'w', encoding='utf-8') as f:
            json.dump(rates, f, ensure_ascii=False, indent=4)
        print(f"Курсы валют успешно сохранены в {LAST_RATES_FILE}: {rates}")
    except Exception as e:
        print(f"Ошибка при сохранении курсов в файл: {e}")


def load_rates_from_file():
    """Загружает последние курсы валют из файла last_rates.json"""
    try:
        if os.path.exists(LAST_RATES_FILE):
            with open(LAST_RATES_FILE, 'r', encoding='utf-8') as f:
                rates = json.load(f)
            print(f"Курсы валют загружены из {LAST_RATES_FILE}: {rates}")
            return rates
        else:
            print(f"Файл {LAST_RATES_FILE} не найден.")
    except Exception as e:
        print(f"Ошибка при загрузке курсов из файла: {e}")
    return None


def get_exchange_rates():
    if 'exchange_rates' not in cache:
        try:
            print("Попытка загрузки курсов с API ЦБ РФ...")
            response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
            response.raise_for_status()
            data = response.json()
            rates = {}
            for currency in ['USD', 'EUR', 'GBP', 'CNY', 'JPY', 'CAD', 'AUD', 'CHF']:
                valute = data['Valute'][currency]
                rates[currency] = valute['Value'] / valute['Nominal']
            rates['RUB'] = 1.0
            cache['exchange_rates'] = rates
            print(f"Курсы валют успешно обновлены с API: {rates}")
            # Сохраняем курсы в файл
            save_rates_to_file(rates)
        except Exception as e:
            print(f"Ошибка загрузки курсов с API: {e}")
            # Пытаемся загрузить последние сохранённые курсы
            rates = load_rates_from_file()
            if rates is None:
                # Если файла нет, используем условные курсы
                rates = {
                    'USD': 96.0,
                    'EUR': 105.0,
                    'GBP': 125.0,
                    'CNY': 13.5,
                    'JPY': 0.0065,  # Условный курс за 1 JPY
                    'CAD': 70.0,
                    'AUD': 63.0,
                    'CHF': 110.0,
                    'RUB': 1.0
                }
                print("Используются условные курсы (файл не найден):", rates)
            else:
                print("Используются сохранённые курсы из файла:", rates)
            cache['exchange_rates'] = rates
    else:
        print("Курсы валют взяты из кэша:", cache['exchange_rates'])
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


@app.before_request
def track_tool_page_view():
    if request.method != "GET":
        return

    tool = get_tool_by_path(request.path)
    if tool:
        try:
            increment_tool_view(tool["slug"])
        except Exception as e:
            app.logger.warning("Usage counter failed for %s: %s", tool["slug"], e)


@app.context_processor
def inject_shell_context():
    current_tool = get_tool_by_path(request.path)
    related_tools = get_related_tools(current_tool["slug"]) if current_tool else []
    return {
        "nav_tools": get_nav_tools(),
        "featured_tools": get_featured_tools(),
        "current_tool": current_tool,
        "related_tools": related_tools,
    }


@app.route('/')
def index():
    return render_template(
        'index.html',
        tools=get_tools(),
        tool_groups=get_tools_by_category(),
        featured_tools=get_featured_tools(),
    )


@app.route('/admin/usage')
def admin_usage():
    admin_token = os.environ.get("ADMIN_USAGE_TOKEN")
    provided_token = request.args.get("token") or request.headers.get("X-Admin-Token")
    if not admin_token or provided_token != admin_token:
        abort(404)

    return render_template('admin_usage.html', stats=get_usage_stats(get_tools()))


if __name__ == '__main__':
    app.run(debug=True)
