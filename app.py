from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = 'e3216ff472e7061394d5ca8a98423016'

@app.route('/', methods=['GET', 'POST'])
def index():
    city = "Hyderabad"  # Default city
    weather_data = None  # Default to None if no data fetched

    if request.method == 'POST':
        city = request.form.get('city', 'Hyderabad')  # Get city from form, default to 'Hyderabad'

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()

        # Convert the sunrise and sunset Unix timestamps to human-readable format
        sunrise_time = datetime.utcfromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M:%S')
        sunset_time = datetime.utcfromtimestamp(data["sys"]["sunset"]).strftime('%H:%M:%S')

        weather_data = {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "feels_like": data["main"]["feels_like"],
            "sunrise": sunrise_time,
            "sunset": sunset_time
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        weather_data = None  # Handle the error gracefully

    return render_template('index.html', weather_data=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
