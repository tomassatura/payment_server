import abc
import json
import os
from datetime import datetime


class WeatherModelBase(abc.ABC):
    @abc.abstractmethod
    def get_weather(self, date: datetime.date, city: str) -> [dict]:
        pass


class DummyWeatherModel(WeatherModelBase):
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        self.weather_source = self._load_weather_file_json(
            os.path.join(self._BASE_DIR, "resources/weather_source.json")
        )

    def get_weather(self, date: datetime.date, city: str) -> [dict]:
        try:
            return self.weather_source[str(date)][city]
        except KeyError:
            raise KeyError(
                "No weather information for this combination of date and city"
            )

    @staticmethod
    def _load_weather_file_json(file_path):
        with open(file_path) as weather_file:
            return json.load(weather_file)
