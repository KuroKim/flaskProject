from flask import Blueprint, render_template

fuel_calculator_bp = Blueprint('fuel_calculator', __name__, template_folder='templates')


@fuel_calculator_bp.route('/fuel-calculator')
def fuel_calculator():
    # Получаем курсы валют из глобального кэша
    from app import get_exchange_rates  # Импортируем функцию из app.py
    exchange_rates = get_exchange_rates()
    return render_template('fuel_calculator.html', exchange_rates=exchange_rates)
