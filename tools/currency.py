from flask import Blueprint, render_template, request
import requests

currency_bp = Blueprint('currency', __name__)


def get_exchange_rates():
    url = "http://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)
    data = response.json()
    rates = {"RUB": 1.0}
    rates["USD"] = data["Valute"]["USD"]["Value"]
    rates["EUR"] = data["Valute"]["EUR"]["Value"]
    return rates


@currency_bp.route('/currency', methods=['GET', 'POST'])
def currency_converter():
    rates = get_exchange_rates()
    currencies = ["RUB", "USD", "EUR"]
    amount = 1.0
    from_currency = "RUB"
    to_currency = "USD"
    result = None

    if request.method == 'POST':
        amount = float(request.form.get('amount', 1.0))
        from_currency = request.form.get('from_currency', 'RUB')
        to_currency = request.form.get('to_currency', 'USD')
        result = round((amount * rates[from_currency]) / rates[to_currency], 2)

    return render_template('currency.html', currencies=currencies, amount=amount,
                           from_currency=from_currency, to_currency=to_currency,
                           result=result, rates=rates)
