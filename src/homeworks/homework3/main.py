import os
from argparse import ArgumentParser

import requests
from dotenv import load_dotenv
from matplotlib import pyplot as plt

from src.homeworks.homework3.dtclass_to_api import CurrentWeather, ForecastWeather

load_dotenv()
API_KEY = os.getenv("API_WEATHER_KEY")
URL = "https://api.openweathermap.org/data/2.5/"


class RequestError(Exception):
    pass


class APIKeyError(Exception):
    pass


def get_json_data(city: str, type_request: str) -> dict:
    try:
        json_data = requests.get(f"{URL}{type_request}?q={city}&appid={API_KEY}&units=metric").json()
    except requests.RequestException:
        raise ConnectionError("the server is not responding")
    cod = json_data.get("cod")
    if cod == 404:
        raise RequestError("incorrect request")
    elif cod == 401:
        raise APIKeyError("incorrect api_key")
    return json_data


def main_current_weather(city: str, request: str) -> None:
    json_dict = get_json_data(city, "weather")
    current_weather = CurrentWeather.bind_lazy_dict(json_dict)
    if request == "default":
        print(
            f"The current weather: {current_weather.weather.main}, description: {current_weather.weather.description}"
        )
    elif request == "temperature":
        print(
            f"The current temperature in {city}: {current_weather.main.temp}°C\n"
            f"Feels like: {current_weather.main.feels_like}°C"
            f"Max: {current_weather.main.temp_max}°C\n"
            f"Min: {current_weather.main.temp_min}°C"
        )
    elif request == "wind":
        print(
            f"The current wind speed in {city}: {current_weather.wind.speed}m/s\n"
            f"Wind direction: {current_weather.wind.deg} degrees\n"
            f"Gusts of wind: {current_weather.wind.gust}m/s"
        )
    elif request == "humidity":
        print(f"The current humidity: {current_weather.main.humidity}%")


def main_forecast_weather(city: str, plot_request: str, period: int) -> None:
    json_dict = get_json_data(city, "forecast")
    forecast_weather = ForecastWeather.bind_lazy_dict(json_dict)
    forecast_data = []
    for i in range(period * 8):
        if plot_request == "temperature":
            forecast_data.append(forecast_weather.list[i].main.temp)
        elif plot_request == "wind":
            forecast_data.append(forecast_weather.list[i].wind.speed)
    plot_forecast(forecast_data, period, plot_request)


def plot_forecast(forecast_data: list, period: int, plot_request: str) -> None:
    plt.plot(forecast_data)
    if plot_request == "temperature":
        title = f"temperature in the last {period} days"
        ylabel = "degrees Celsius"
    else:
        title = f"wind speed in the last {period} days"
        ylabel = "m/s"
    plt.title(title)
    plt.ylabel(ylabel)
    plt.show()


def parse_args() -> dict:
    parser = ArgumentParser()
    parser.add_argument("city", type=str, help="the city for the weather forecast")
    subparsers = parser.add_subparsers(dest="subcommand", help="forecast or current weather")
    weather_parser = subparsers.add_parser("weather")
    forecast_parser = subparsers.add_parser("forecast")
    weather_parser.add_argument(
        "request", type=str, nargs="?", default="default", choices=["default", "temperature", "wind", "humidity"]
    )
    forecast_parser.add_argument(
        "plot_request", type=str, nargs="?", default="temperature", choices=["temperature", "wind"]
    )
    forecast_parser.add_argument("period", type=int, nargs="?", default=5, choices=[1, 2, 3, 4, 5])
    my_args = parser.parse_args()
    return vars(my_args)


def main(args: dict) -> None:
    subcommand = args["subcommand"]
    if subcommand == "weather":
        del args["subcommand"]
        main_current_weather(**args)
    elif subcommand == "forecast":
        del args["subcommand"]
        main_forecast_weather(**args)


if __name__ == "__main__":
    my_args = parse_args()
    main(my_args)
