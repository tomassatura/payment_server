from orinoco.entities import ActionConfig, Signature
from orinoco.typed_action import TypedAction

from src.weather_prediction.weather_prediction import DummyWeatherModel


class GetWeatherInformation(TypedAction):
    CONFIG = ActionConfig(
        INPUT={
            "date": Signature(key="date"),
            "city": Signature(key="city"),
        },
        OUTPUT=Signature(key="weather_information"),
    )

    def __call__(self,  date,  city):
        return DummyWeatherModel().get_weather(date, city)