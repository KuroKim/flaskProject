from flask import Blueprint, render_template

currency_bp = Blueprint('currency', __name__, template_folder='templates')


@currency_bp.route('/currency')
def currency():
    from app import get_exchange_rates  # Импортируем функцию из app.py
    exchange_rates = get_exchange_rates()
    return render_template('currency.html', exchange_rates=exchange_rates)
