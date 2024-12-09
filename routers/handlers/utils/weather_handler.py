import asyncio
import aiohttp

from src.core import settings


async def share_weather():
    weather = dict()
    data = await parse_weather()
    weather.update(
        [
            ("desc", data["weather"][0]["description"]),
            ("temp", data["main"]["temp"]),
            ("feel_like", data["main"]["feels_like"]),
            ("wind", data["wind"]["speed"]),
        ]
    )
    return weather


async def parse_weather():
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": "Красноярск",
        "units": "metric",
        "lang": "ru",
        "appid": settings.weather_token
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params) as response:
            return await response.json()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(share_weather())
