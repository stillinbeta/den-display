from datetime import date, datetime
from datetime import timedelta
import logging
import requests


# Many thanks to https://github.com/bachya/aiorecollect for the key info needed
# to decipher the Recollect API.
#
API_URL_SCAFFOLD = "https://api.recollect.net/api/places/{0}/services/{1}/events"


def get_schedule(place, service):
    today = date.today()
    three_weeks = today + timedelta(days=21)

    url = API_URL_SCAFFOLD.format(place, service)
    params = {
        'after': str(today),
        'before': str(three_weeks)
    }

    resp = requests.get(url=url, params=params)
    data = resp.json()

    logging.debug(f'Retrieved garbage data: {data}')

    schedule = {
        'compost_date': _find_next_event(data, 'compost'),
        'garbage_date': _find_next_event(data, 'garbage'),
        'recycling_date': _find_next_event(data, 'recycling_cov_curbside')
    }

    logging.info(f'Generated garbage schedule: {schedule}')

    return schedule


def _find_next_event(schedule, event_type):
    relevant_events = [
        event
        for event in schedule['events']
        if 'is_holiday' not in event
    ]

    for event in relevant_events:
        day = event['day']

        for flag in event['flags']:
            if flag['name'] == event_type:
                return _convert_date(day)

def _convert_date(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%d')

    if date_object.date() == date.today():
        friendly_date = 'today'
    elif date_object.date() == date.today() + timedelta(days=1):
        friendly_date = 'tomorrow'
    else:
        friendly_date = date_object.strftime("%B %-d")

    return friendly_date


if __name__ == '__main__':
    print(get_schedule())
