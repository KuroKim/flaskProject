from flask import Blueprint, render_template, request
import requests

weather_bp = Blueprint('weather', __name__)


@weather_bp.route('/weather', methods=['GET', 'POST'])
def weather():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city', '')
        api_key = "YOUR_OPENWEATHER_API_KEY"  # Замените на ваш ключ OpenWeather
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "temp": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "city": data["name"]
            }
    return render_template('weather.html', weather_data=weather_data)
