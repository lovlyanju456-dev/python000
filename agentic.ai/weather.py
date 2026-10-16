from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather App</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #102a43, #247ba0);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            color: white;
        }

        .container {
            width: 100%;
            max-width: 450px;
            padding: 30px;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.13);
            box-shadow: 0 10px 30px #102a4366;
        }

        h1, .subtitle {
            text-align: center;
        }

        .subtitle {
            color: #d8e9f3;
            margin-bottom: 25px;
        }

        input {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 8px;
            margin: 10px 0 15px;
            font-size: 16px;
        }

        button {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 8px;
            background: #ffcc70;
            color: #17324d;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #ffd994;
        }

        .result {
            margin-top: 25px;
            padding: 20px;
            background: #ffffff20;
            border-radius: 12px;
            text-align: center;
        }

        .temperature {
            font-size: 48px;
            font-weight: bold;
            margin: 15px 0;
        }

        .condition {
            font-size: 20px;
            margin-bottom: 20px;
        }

        .details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }

        .detail {
            padding: 12px 5px;
            background: #ffffff20;
            border-radius: 8px;
        }

        .detail p {
            font-weight: bold;
        }

        .error {
            margin-top: 20px;
            padding: 12px;
            background: #ffe5e5;
            color: #a40000;
            border-radius: 8px;
            text-align: center;
        }

        footer {
            text-align: center;
            margin-top: 20px;
            font-size: 12px;
            color: #d8e9f3;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>Weather App</h1>
        <p class="subtitle">Check the weather in your city</p>

        <form method="POST">
            <label for="city">Enter City Name</label>
            <input type="text" id="city" name="city"
                   placeholder="Example: Tirupati"
                   value="{{ city }}" required>
            <button type="submit">Get Weather</button>
        </form>

        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}

        {% if weather %}
            <div class="result">
                <h2>{{ weather.city }}, {{ weather.country }}</h2>
                <div class="temperature">
                    {{ weather.temperature }}°C
                </div>
                <div class="condition">{{ weather.condition }}</div>

                <div class="details">
                    <div class="detail">
                        Feels Like
                        <p>{{ weather.feels_like }}°C</p>
                    </div>
                    <div class="detail">
                        Humidity
                        <p>{{ weather.humidity }}%</p>
                    </div>
                    <div class="detail">
                        Wind Speed
                        <p>{{ weather.wind }} km/h</p>
                    </div>
                    <div class="detail">
                        Weather
                        <p>{{ weather.condition }}</p>
                    </div>
                </div>
            </div>
        {% endif %}

        <footer>Weather data by Open-Meteo</footer>
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None
    city = ""

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        try:
            if not city:
                error = "Please enter a city name."
            else:
                # Get city coordinates
                geo = requests.get(
                    "https://geocoding-api.open-meteo.com/v1/search",
                    params={"name": city, "count": 1, "language": "en"},
                    timeout=10
                )
                geo.raise_for_status()
                results = geo.json().get("results", [])

                if not results:
                    error = "City not found. Please try again."
                else:
                    location = results[0]

                    # Get current weather
                    response = requests.get(
                        "https://api.open-meteo.com/v1/forecast",
                        params={
                            "latitude": location["latitude"],
                            "longitude": location["longitude"],
                            "current": (
                                "temperature_2m,relative_humidity_2m,"
                                "apparent_temperature,wind_speed_10m,"
                                "weather_code"
                            )
                        },
                        timeout=10
                    )
                    response.raise_for_status()
                    current = response.json()["current"]

                    code = current["weather_code"]

                    if code == 0:
                        condition = "Clear Sky"
                    elif code in (1, 2, 3):
                        condition = "Partly Cloudy"
                    elif code in (45, 48):
                        condition = "Foggy"
                    elif code in (51, 53, 55, 56, 57):
                        condition = "Drizzle"
                    elif code in (61, 63, 65, 66, 67, 80, 81, 82):
                        condition = "Rainy"
                    elif code in (71, 73, 75, 77, 85, 86):
                        condition = "Snowy"
                    elif code in (95, 96, 99):
                        condition = "Thunderstorm"
                    else:
                        condition = "Variable Conditions"

                    weather = {
                        "city": location["name"],
                        "country": location.get("country", ""),
                        "temperature": current["temperature_2m"],
                        "feels_like": current["apparent_temperature"],
                        "humidity": current["relative_humidity_2m"],
                        "wind": current["wind_speed_10m"],
                        "condition": condition
                    }

        except requests.RequestException:
            error = "Unable to connect. Check your internet connection."
        except (KeyError, ValueError, TypeError):
            error = "Unable to retrieve weather data. Try again."

    return render_template_string(
        HTML, weather=weather, error=error, city=city
    )


if __name__ == "__main__":
    app.run(debug=True)
