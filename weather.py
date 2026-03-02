import os
import requests
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Celsius directly (no Kelvin conversion needed)
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code != 200:
        raise Exception(data.get("message", "Unknown error"))

    return data


def format_weather(data: dict) -> str:
    city = data["name"]
    country = data["sys"]["country"]

    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    temp_min = data["main"]["temp_min"]
    temp_max = data["main"]["temp_max"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]

    weather_main = data["weather"][0]["main"]
    weather_desc = data["weather"][0]["description"]

    wind_speed = data["wind"]["speed"]
    wind_deg = data["wind"].get("deg", 0)

    clouds = data["clouds"]["all"]

    weather_emoji = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️"
    }.get(weather_main, "")

    timezone_offset = data.get("timezone", 0)

    sunrise = datetime.datetime.fromtimestamp(
        data["sys"]["sunrise"] + timezone_offset,
        datetime.timezone.utc
    ).strftime("%H:%M:%S")

    sunset = datetime.datetime.fromtimestamp(
        data["sys"]["sunset"] + timezone_offset,
        datetime.timezone.utc
    ).strftime("%H:%M:%S")

    updated = datetime.datetime.fromtimestamp(
        data["dt"] + timezone_offset,
        datetime.timezone.utc
    ).strftime("%Y-%m-%d %H:%M:%S")

    return f"""
--- Weather in {city}, {country} ---
{weather_emoji} Weather: {weather_main} ({weather_desc})
🌡️ Temperature: {temp:.1f}°C (feels like: {feels_like:.1f}°C)
🔻/🔺 Min/Max: {temp_min:.1f}°C / {temp_max:.1f}°C
💧 Humidity: {humidity}%
⚖️ Pressure: {pressure} hPa
💨 Wind: {wind_speed} m/s, direction: {wind_deg}°
☁️ Cloudiness: {clouds}%
🌅 Sunrise: {sunrise}
🌇 Sunset: {sunset}
⏰ Last updated: {updated}
"""


if __name__ == "__main__":
    city_input = input("Enter city name: ")

    try:
        weather_data = get_weather(city_input)
        print(format_weather(weather_data))
    except Exception as e:
        print("Error:", e)