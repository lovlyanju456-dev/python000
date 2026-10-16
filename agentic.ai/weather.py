
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Free weather API - no API key required
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Heavy Drizzle",
    61: "Light Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    71: "Light Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    80: "Rain Showers",
    81: "Moderate Rain Showers",
    82: "Heavy Rain Showers",
    95: "Thunderstorm",
    96: "Thunderstorm with Hail",
    99: "Heavy Thunderstorm"
}

# HTML and CSS are included inside this Python file.
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WeatherNow - Weather Report</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 30px 15px;
            min-height: 100vh;
            font-family: Arial, sans-serif;
            color: #172554;
            background: linear-gradient(
                135deg, #dbeafe, #eff6ff, #f8fafc
            );
        }

        .container {
            max-width: 850px;
            margin: auto;
        }

        header {
            text-align: center;
            margin-bottom: 30px;
        }

        .logo {
            font-size: 48px;
        }

        h1 {
            margin: 8px 0;
            font-size: 38px;
        }

        .subtitle {
            color: #64748b;
        }

        .card {
            background: white;
            padding: 30px;
            border-radius: 22px;
            box-shadow: 0 15px 45px rgba(37, 99, 235, 0.12);
        }

        form {
            display: flex;
            gap: 10px;
        }

        input {
            flex: 1;
            min-width: 0;
            padding: 15px;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            font-size: 16px;
        }

        button {
            padding: 15px 22px;
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #1d4ed8;
        }

        .error {
            background: #fff1f2;
            color: #be123c;
            padding: 14px;
            margin-top: 20px;
            border-radius: 10px;
        }

        .report {
            margin-top: 30px;
        }

        .location {
            color: #64748b;
            font-size: 14px;
        }

        .main-weather {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
            margin-top: 15px;
        }

        .condition {
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .temperature {
            font-size: 65px;
            font-weight: bold;
        }

        .feels {
            color: #64748b;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-top: 25px;
        }

        .metric {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 16px;
            border-radius: 12px;
        }

        .metric-label {
            font-size: 13px;
            color: #64748b;
            margin-bottom: 10px;
        }

        .metric-value {
            font-size: 18px;
            font-weight: bold;
            overflow-wrap: anywhere;
        }

        h3 {
            margin-top: 28px;
        }

        .footer {
            text-align: center;
            color: #64748b;
            font-size: 12px;
            margin-top: 22px;
            line-height: 1.6;
        }

        @media (max-width: 600px) {
            .card {
                padding: 20px;
            }

            form {
                flex-direction: column;
            }

            .grid {
                grid-template-columns: repeat(2, 1fr);
            }

            .temperature {
                font-size: 48px;
            }
        }
    </style>
</head>

<body>
<div class="container">

    <header>
        <div class="logo">🌤️</div>
        <h1>WeatherNow</h1>
        <p class="subtitle">
            Get current weather reports for cities around the world.
        </p>
    </header>

    <div class="card">

        <form method="POST">
            <input
                type="text"
                name="city"
                placeholder="Enter city name, e.g. Bengaluru"
                value="{{ city }}"
                required
            >
            <button type="submit">Get Weather</button>
        </form>

        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}

        {% if weather %}
        <div class="report">

            <div class="location">
                CURRENT WEATHER · {{ weather.location }}
            </div>

            <div class="main-weather">
                <div>
                    <div class="condition">
                        {{ weather.condition }}
                    </div>
                    <div class="feels">
                        Feels like {{ weather.feels }}{{ weather.unit }}
                    </div>
                </div>

                <div class="temperature">
                    {{ weather.temperature }}{{ weather.unit }}
                </div>
            </div>

            <h3>Weather Details</h3>

            <div class="grid">

                <div class="metric">
                    <div class="metric-label">💧 Humidity</div>
                    <div class="metric-value">
                        {{ weather.humidity }}%
                    </div>
                </div>

                <div class="metric">
                    <div class="metric-label">💨 Wind Speed</div>
                    <div class="metric-value">
                        {{ weather.wind }} km/h
                    </div>
                </div>

                <div class="metric">
                    <div class="metric-label">☁️ Cloud Cover</div>
                    <div class="metric-value">
                        {{ weather.cloud }}%
                    </div>
                </div>

                <div class="metric">
                    <div class="metric-label">🌧️ Precipitation</div>
                    <div class="metric-value">
                        {{ weather.precip }} mm
                    </div>
                </div>

                <div class="metric">
                    <div class="metric-label">🔽 Today's Low</div>
                    <div class="metric-value">
                        {{ weather.low }}{{ weather.unit }}
                    </div>
                </div>

                <div class="metric">
                    <div class="metric-label">🔺 Today's High</div>
                    <div class="metric-value">
                        {{ weather.high }}{{ weather.unit }}
                    </div>
                </div>

                <div class="metric">
                    <div class="metric-label">🌦️ Rain Probability</div>
                    <div class="metric-value">
                        {{ weather.rain_chance }}%
                    </div>
                </div>

                <div class="metric">
                    <div class="metric-label">🌅 Sunrise</div>
                    <div class="metric-value">
                        {{ weather.sunrise }}
                    </div>
                </div>

                <div class="metric">
                    <div class="metric-label">🌇 Sunset</div>
                    <div class="metric-value">
                        {{ weather.sunset }}
                    </div>
                </div>

            </div>

            <p class="subtitle">
                Local observation time: {{ weather.time }}
            </p>
        </div>
        {% endif %}

    </div>

    <div class="footer">
        Weather data provided by Open-Meteo.<br>
        Free API for non-commercial use. No API key required.
    </div>

</div>
</body>
</html>
"""


def fetch_json(url, params):
    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    return response.json()


def get_weather(city):
    # Find the city's latitude and longitude.
    geo_data = fetch_json(
        GEOCODING_URL,
        {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }
    )

    places = geo_data.get("results", [])

    if not places:
        raise ValueError(
            "City not found. Please check the spelling and try again."
        )

    place = places[0]

    # Get current weather and today's forecast.
    data = fetch_json(
        WEATHER_URL,
        {
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "apparent_temperature,"
                "precipitation,"
                "weather_code,"
                "cloud_cover,"
                "wind_speed_10m"
            ),
            "daily": (
                "temperature_2m_max,"
                "temperature_2m_min,"
                "sunrise,"
                "sunset,"
                "precipitation_probability_max"
            ),
            "timezone": "auto",
            "forecast_days": 1
        }
    )

    current = data["current"]
    daily = data["daily"]
    units = data.get("current_units", {})

    location_parts = [
        place.get("name"),
        place.get("admin1"),
        place.get("country")
    ]

    location = ", ".join(
        dict.fromkeys(part for part in location_parts if part)
    )

    rain_chance = daily.get(
        "precipitation_probability_max", [0]
    )[0]

    return {
        "location": location,
        "condition": WEATHER_CODES.get(
            current.get("weather_code"),
            "Conditions unavailable"
        ),
        "temperature": current.get("temperature_2m", "N/A"),
        "feels": current.get("apparent_temperature", "N/A"),
        "unit": units.get("temperature_2m", "°C"),
        "humidity": current.get("relative_humidity_2m", "N/A"),
        "wind": current.get("wind_speed_10m", "N/A"),
        "cloud": current.get("cloud_cover", "N/A"),
        "precip": current.get("precipitation", "N/A"),
        "low": daily.get("temperature_2m_min", ["N/A"])[0],
        "high": daily.get("temperature_2m_max", ["N/A"])[0],
        "rain_chance": (
            rain_chance if rain_chance is not None else "N/A"
        ),
        "sunrise": daily.get("sunrise", ["N/A"])[0].split("T")[-1],
        "sunset": daily.get("sunset", ["N/A"])[0].split("T")[-1],
        "time": current.get("time", "N/A").replace("T", " ")
    }


@app.route("/", methods=["GET", "POST"])
def home():
    city = ""
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if not city:
            error = "Please enter a city name."
        else:
            try:
                weather = get_weather(city)

            except ValueError as exc:
                error = str(exc)

            except requests.RequestException:
                error = (
                    "Unable to connect to the weather service. "
                    "Check your internet connection and try again."
                )

            except (KeyError, IndexError, TypeError):
                error = (
                    "Unable to read weather data. Please try again."
                )

    return render_template_string(
        HTML,
        city=city,
        weather=weather,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
