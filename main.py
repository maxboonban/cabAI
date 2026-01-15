from datetime import datetime
from typing import Any, Dict, Optional

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

def _safe_float(value: Optional[float], fallback: float = 0.0) -> float:
    if value is None:
        return fallback
    return float(value)


def geocode_location(location: str) -> Dict[str, Any]:
    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": location, "count": 1, "language": "en", "format": "json"},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    if not data.get("results"):
        raise ValueError("Location not found")
    result = data["results"][0]
    return {
        "name": result["name"],
        "country": result.get("country"),
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "timezone": result.get("timezone"),
    }


def fetch_weather(latitude: float, longitude: float) -> Dict[str, Any]:
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,precipitation,weather_code,wind_speed_10m",
            "timezone": "auto",
        },
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    current = data.get("current", {})
    return {
        "temperature": _safe_float(current.get("temperature_2m")),
        "precipitation": _safe_float(current.get("precipitation")),
        "wind_speed": _safe_float(current.get("wind_speed_10m")),
        "weather_code": current.get("weather_code"),
        "time": current.get("time"),
        "timezone": data.get("timezone"),
    }


def fetch_recent_earthquake(latitude: float, longitude: float) -> Dict[str, Any]:
    response = requests.get(
        "https://earthquake.usgs.gov/fdsnws/event/1/query",
        params={
            "format": "geojson",
            "latitude": latitude,
            "longitude": longitude,
            "maxradiuskm": 300,
            "orderby": "time",
            "limit": 1,
        },
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    features = data.get("features", [])
    if not features:
        return {"status": "No recent events", "magnitude": None, "place": None, "time": None}
    feature = features[0]
    props = feature.get("properties", {})
    event_time = None
    if props.get("time"):
        event_time = datetime.utcfromtimestamp(props["time"] / 1000).isoformat() + "Z"
    return {
        "status": "Recent event",
        "magnitude": props.get("mag"),
        "place": props.get("place"),
        "time": event_time,
    }


def classify_risk(value: float, thresholds: Dict[str, float]) -> str:
    for label, threshold in thresholds.items():
        if value >= threshold:
            return label
    return "Low"


def build_conditions_summary(weather: Dict[str, Any], earthquake: Dict[str, Any]) -> Dict[str, Any]:
    temperature = weather["temperature"]
    precipitation = weather["precipitation"]

    heat_wave = classify_risk(
        temperature,
        {"Extreme": 38, "High": 32, "Moderate": 28},
    )
    flood_risk = classify_risk(
        precipitation,
        {"High": 10, "Moderate": 3},
    )
    landslide_risk = classify_risk(
        precipitation,
        {"High": 15, "Moderate": 6},
    )

    earthquake_status = "Low"
    if earthquake.get("magnitude"):
        magnitude = earthquake["magnitude"]
        if magnitude >= 6:
            earthquake_status = "High"
        elif magnitude >= 4.5:
            earthquake_status = "Moderate"

    return {
        "temperature": temperature,
        "rainfall": precipitation,
        "wind_speed": weather["wind_speed"],
        "heat_wave": heat_wave,
        "flood": flood_risk,
        "landslide": landslide_risk,
        "earthquake": earthquake_status,
    }


@app.route("/")
def home() -> str:
    return render_template("index.html")


@app.route("/api/conditions")
def api_conditions():
    location = request.args.get("location", "San Francisco")
    try:
        geo = geocode_location(location)
        weather = fetch_weather(geo["latitude"], geo["longitude"])
        earthquake = fetch_recent_earthquake(geo["latitude"], geo["longitude"])
        summary = build_conditions_summary(weather, earthquake)
    except (requests.RequestException, ValueError) as error:
        return jsonify({"error": str(error)}), 502
    return jsonify(
        {
            "location": geo,
            "weather": weather,
            "earthquake": earthquake,
            "summary": summary,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
