from datetime import datetime
import logging

from flask import Flask, render_template

from lib import garbage_fetcher, weather_fetcher


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


@app.route("/")
def hello_world():
    # HERE
    garbage = garbage_fetcher.get_schedule('X', '193')

    weather = weather_fetcher.get_current_weather()

    return render_template(
        'index.html',
        **garbage,
        **weather
    )
