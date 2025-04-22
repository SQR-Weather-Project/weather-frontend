import random
from datetime import datetime, timedelta

import pandas as pd


def get_mock_weather():
    return {
        "coord": {"lon": 44, "lat": 55},
        "weather": [
            {"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04d"}
        ],
        "base": "stations",
        "main": {
            "temp": 18.13,
            "feels_like": 17.15,
            "temp_min": 18.13,
            "temp_max": 18.13,
            "pressure": 1017,
            "humidity": 44,
            "sea_level": 1017,
            "grnd_level": 995,
        },
        "visibility": 10000,
        "wind": {"speed": 4.98, "deg": 228, "gust": 10.47},
        "clouds": {"all": 79},
        "dt": 1745301031,
        "sys": {"country": "RU", "sunrise": 1745286241, "sunset": 1745338838},
        "timezone": 10800,
        "id": 535672,
        "name": "Lesogorsk",
        "cod": 200,
    }


def get_mock_history():
    now = datetime.now()
    return pd.DataFrame(
        {
            "timestamp": [now - timedelta(hours=i) for i in range(24)],
            "temp": [random.uniform(10, 20) for _ in range(24)],
            "humidity": [random.randint(40, 80) for _ in range(24)],
        }
    )
