import asyncio
import os
import logging
import tomllib

from quart import Quart, render_template

from den_display import garbage_fetcher, weatherapi_fetcher

logging.basicConfig(level=logging.DEBUG)
app = Quart(__name__)


@app.errorhandler(500)
async def page_not_found(_e: Exception) -> tuple[str, int]:
    return await render_template('500.html'), 500


@app.route("/")
async def hello_world() -> str:
    garbage = await garbage_fetcher.get_schedule(app.config["GARBAGE_LOCATION"], '193')

    weather = await weatherapi_fetcher.get_current_weather(
        api_key=app.config['WEATHER_API_KEY'],
        location=app.config['WEATHER_LOCATION'],
    )

    return await render_template(
        'index.html',
        **garbage,
        **weather
    )

def get_config() -> dict[str, str]:
    return {
        'GARBAGE_LOCATION': os.environ['GARBAGE_LOCATION'],
        'WEATHER_LOCATION': os.environ['WEATHER_LOCATION'],
        'WEATHER_API_KEY': os.environ['WEATHER_API_KEY'],
    }


if __name__ == "__main__":
    app.config.from_mapping(get_config())
    app.run()
