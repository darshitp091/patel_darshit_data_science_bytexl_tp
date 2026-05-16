import os
import requests
import pandas as pd


API_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "bd5e378503939ddaee76f12ad7a97608"


def fetch_weather(city: str, country: str, api_key: str) -> dict:
    """Fetch weather data from OpenWeather API."""
    params = {
        "q": f"{city},{country}",
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(API_URL, params=params, timeout=15)

    # Show incoming API call details
    request_info = pd.DataFrame([{
        "method": response.request.method,
        "url": response.request.url,
        "status_code": response.status_code
    }])

    print("\n=== API REQUEST DETAILS ===")
    print(request_info.to_string(index=False))

    print("\n=== RESPONSE HEADERS ===")
    headers_df = pd.DataFrame(list(response.headers.items()), columns=["header", "value"])
    print(headers_df.to_string(index=False))

    response.raise_for_status()
    return response.json()


def weather_to_table(data: dict) -> pd.DataFrame:
    """Convert API JSON response to a readable table."""
    row = {
        "city": data.get("name"),
        "country": data.get("sys", {}).get("country"),
        "weather": data.get("weather", [{}])[0].get("description"),
        "temperature_c": data.get("main", {}).get("temp"),
        "feels_like_c": data.get("main", {}).get("feels_like"),
        "temp_min_c": data.get("main", {}).get("temp_min"),
        "temp_max_c": data.get("main", {}).get("temp_max"),
        "humidity_%": data.get("main", {}).get("humidity"),
        "pressure_hpa": data.get("main", {}).get("pressure"),
        "wind_speed_mps": data.get("wind", {}).get("speed"),
        "wind_deg": data.get("wind", {}).get("deg"),
        "cloudiness_%": data.get("clouds", {}).get("all"),
        "sunrise": pd.to_datetime(data.get("sys", {}).get("sunrise"), unit="s"),
        "sunset": pd.to_datetime(data.get("sys", {}).get("sunset"), unit="s"),
    }

    df = pd.DataFrame([row])
    return df.sort_index(axis=1)


def main():
    print("OpenWeather Weather Lookup")
    city = input("Enter city: ").strip()
    country = input("Enter country code/name (example: IN, US): ").strip()

    api_key = os.getenv("OPENWEATHER_API_KEY") or API_KEY

    if not api_key:
        print("OpenWeather API key is missing.")
        return

    try:
        data = fetch_weather(city, country, api_key)

        print("\n=== RAW API JSON KEYS ===")
        print(list(data.keys()))

        print("\n=== WEATHER DATA IN TABLE FORMAT ===")
        weather_df = weather_to_table(data)
        print(weather_df.to_string(index=False))

        print("\n=== HOW DATA IS FETCHED ===")
        fetch_steps = pd.DataFrame([
            {"step": 1, "action": "Read city and country from user"},
            {"step": 2, "action": "Build GET request with q=city,country and API key"},
            {"step": 3, "action": "Send request using requests.get()"},
            {"step": 4, "action": "Convert JSON response to Python dictionary"},
            {"step": 5, "action": "Use pandas DataFrame to display data in table form"},
        ])
        print(fetch_steps.to_string(index=False))

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        try:
            print("API response:", e.response.json())
        except Exception:
            print("API response text:", e.response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()