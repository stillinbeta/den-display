import asyncio
import os
import logging
import tomllib

from quart import Quart, render_template

from lib import garbage_fetcher # , weather_fetcher

logging.basicConfig(level=logging.DEBUG)
app = Quart(__name__)


@app.errorhandler(500)
async def page_not_found(e):
    return await render_template('500.html'), 500


@app.route("/")
async def hello_world() -> str:
    garbage = await garbage_fetcher.get_schedule(app.config["GARBAGE_LOCATION"], '193')

    # weather = await weather_fetcher.get_current_weather()

    return await render_template(
        'index.html',
        **garbage,
        # **weather
    )

def get_config() -> dict[str, str]:
    return {
        'GARBAGE_LOCATION': os.environ['GARBAGE_LOCATION'],
    }

app.config.from_mapping(get_config())


if __name__ == "__main__":
    app.run()
