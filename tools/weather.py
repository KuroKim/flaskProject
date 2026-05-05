from flask import Blueprint, render_template, request
import os
import requests

weather_bp = Blueprint('weather', __name__)


@weather_bp.route('/weather', methods=['GET', 'POST'])
def weather():
    weather_data = None
    error_message = None
    city = ''
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        api_key = os.environ.get('OPENWEATHER_API_KEY')

        if not city:
            error_message = "Введите город."
        elif not api_key:
            error_message = "Погода пока не настроена: нужен OPENWEATHER_API_KEY."
        else:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": api_key,
                "units": "metric",
                "lang": "ru",
            }

            try:
                response = requests.get(url, params=params, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    weather_data = {
                        "temp": data["main"]["temp"],
                        "description": data["weather"][0]["description"],
                        "city": data["name"]
                    }
                elif response.status_code == 404:
                    error_message = "Город не найден. Проверьте название и попробуйте еще раз."
                else:
                    error_message = "Не удалось получить погоду. Попробуйте позже."
            except requests.Timeout:
                error_message = "Сервис погоды не ответил вовремя. Попробуйте позже."
            except requests.RequestException:
                error_message = "Сейчас не получается связаться с сервисом погоды."

    return render_template(
        'weather.html',
        weather_data=weather_data,
        error_message=error_message,
        city=city,
    )
