from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Load API key from environment or replace with your key
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "YOUR_API_KEY_HERE")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Crop advisory logic based on temperature & conditions
def crop_advisory(temp_c, weather_desc):
    if "rain" in weather_desc.lower():
        return "Good time for rice, jute, and sugarcane crops."
    elif temp_c > 30:
        return "Ideal for cotton, maize, and millets."
    elif 20 <= temp_c <= 30:
        return "Suitable for wheat, barley, and vegetables."
    else:
        return "Consider frost-resistant crops like mustard and peas."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather", methods=["POST"])
def weather():
    city = request.form.get("city")
    if not city:
        return jsonify({"error": "City is required"}), 400

    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("cod") != 200:
        return jsonify({"error": data.get("message", "City not found")}), 404

    temp_c = data["main"]["temp"]
    weather_desc = data["weather"][0]["description"]
    advisory = crop_advisory(temp_c, weather_desc)

    return jsonify({
        "city": city,
        "temperature": temp_c,
        "weather": weather_desc,
        "advisory": advisory
    })

if __name__ == "__main__":
    app.run(debug=True)
