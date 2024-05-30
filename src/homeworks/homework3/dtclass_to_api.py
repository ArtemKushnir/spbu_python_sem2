from src.homeworks.homework3.json_orm import *


@dataclass
class Coord(ORM):
    lon: float
    lat: float


@dataclass
class Weather(ORM):
    id: int
    main: str
    description: str
    icon: str


@dataclass
class Main(ORM):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int


@dataclass
class Wind(ORM):
    speed: float
    deg: int
    gust: float


@dataclass
class Clouds(ORM):
    all: int


@dataclass
class Sys(ORM):
    type: int
    id: int
    country: str
    sunrise: int
    sunset: int


@dataclass
class CurrentWeather(ORM):
    coord: Coord
    weather: Weather
    base: str
    main: Main
    visibility: int
    wind: Wind
    clouds: Clouds
    dt: int
    sys: Sys
    timezone: int
    id: int
    name: str
    cod: int


@dataclass
class ForecastWeather(ORM):
    list: list[CurrentWeather]


@dataclass
class A:
    all: int
