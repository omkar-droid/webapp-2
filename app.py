from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime, timedelta

# Flask app setup
app = Flask(__name__)
CORS(app)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.String(10), nullable=False)
    end_date = db.Column(db.String(10), nullable=False)
    weather_data = db.Column(db.Text, nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

# Fetch weather data from OpenWeatherMap API
API_KEY = '67577b891172d02c6219e50e499ffe5e'
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"


def fetch_weather(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Routes
@app.route('/weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    location = data.get("location")

    try:
        # Fetch forecast data
        response = requests.get(BASE_URL, params={
            "q": location,
            "appid": API_KEY,
            "units": "metric"
        })

        if response.status_code == 200:
            forecast_data = response.json()
            weather_results = []

            for item in forecast_data["list"]:
                weather_results.append({
                    "date": item["dt_txt"],
                    "temp": item["main"]["temp"],
                    "condition": item["weather"][0]["description"]
                })

            return jsonify({"data": weather_results})

        else:
            return jsonify({"error": "Location not found or API limit exceeded."}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/weather', methods=['GET'])
def read_weather_records():
    records = Weather.query.all()
    return jsonify([{
        'id': record.id,
        'location': record.location,
        'start_date': record.start_date,
        'end_date': record.end_date,
        'weather_data': record.weather_data
    } for record in records])

@app.route('/weather/<int:id>', methods=['PUT'])
def update_weather_record(id):
    record = Weather.query.get_or_404(id)
    data = request.json

    record.location = data.get('location', record.location)
    record.start_date = data.get('start_date', record.start_date)
    record.end_date = data.get('end_date', record.end_date)
    db.session.commit()

    return jsonify({'message': 'Weather record updated'})

@app.route('/weather/<int:id>', methods=['DELETE'])
def delete_weather_record(id):
    record = Weather.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Weather record deleted'})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

