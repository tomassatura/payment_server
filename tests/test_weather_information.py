import unittest
from datetime import date

from src.weather_prediction.weather_prediction import DummyWeatherModel
from src.actions import GetWeatherInformation


class WeatherInformationTestCase(unittest.TestCase):
    def test_dummy_weather_model(self):
        self.assertEqual(
            DummyWeatherModel().get_weather(date(2021, 10, 21), "London"),
            {"clouds": "CLOUDY", "temperature": 21, "wind_direction": "S"},
        )

    def test_get_weather_information_action(self):
        action = GetWeatherInformation()
        action_run_result = action.run_with_data(date=date(2021, 10, 21), city="London")
        self.assertEqual(action_run_result.get("weather_information"),
                         {"clouds": "CLOUDY", "temperature": 21, "wind_direction": "S"})
