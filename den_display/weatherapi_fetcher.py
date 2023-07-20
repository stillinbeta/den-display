import logging
import aiohttp


# https://www.weatherapi.com/docs/weather_conditions.json
API_URL_SCAFFOLD = "https://api.weatherapi.com/v1/{0}.json"


async def get_current_weather(api_key: str, location: str) -> dict:
    query = {
        'q': location
    }

    response = await _get_weather('current', query, api_key)

    logging.debug(f'Retrieved weather data: {response}')

    precipitation = response['current']['precip_mm']
    temperature = response['current']['temp_c']
    code = response['current']['condition']['code']
    phase = response['current']['is_day']
    humidity = response['current']['humidity']

    weather = {
        'precipitation_icon': _get_rain_icon(precipitation),
        'precipitation': f'{precipitation} mm',
        'temperature_icon': _get_temperature_icon(temperature),
        'temperature': f'{temperature}°C',
        'condition_icon': _get_condition_icon(code, phase),
        'humidity': f'{humidity}%'
    }

    logging.info(f'Generated weather state: {weather}')

    return weather

def _get_rain_icon(precipitation: float) -> str:
    if precipitation == 0.0:
        icon = 'droplet-slash'
    else:
        icon = 'droplet'

    return icon

def _get_temperature_icon(temperature: float) -> str:
    if temperature < 5:
        icon = 'temperature-low'
    elif temperature < 4:
        icon = 'temperature-quarter'
    elif temperature < 12:
        icon = 'temperature-half'
    elif temperature < 21:
        icon = 'temperature-three-quarters'
    elif temperature < 28:
        icon = 'temperature-full'
    else:
        icon = 'temperature-high'

    return icon

def _get_condition_icon(code: int, phase: int) -> str:
    if phase == 1:
        phase_text = 'sun'
    else:
        phase_text = 'moon'

    if code in [1000]:
        icon = phase_text
    elif code in [1003]:
        icon = f'cloud-{phase_text}'
    elif code in [1006, 1009]:
        icon = 'cloud'
    elif code in [1030, 1135, 1147]:
        icon = 'mist'
    elif code in [1063, 1069, 1072, 1150, 1153, 1168, 1180, 1186, 1198, 1204, 1240, 1249, 1264, 1273]:
        icon = 'cloud-rain'
    elif code in [1171, 1189, 1192, 1195, 1201, 1207, 1243, 1246, 1252, 1276]:
        icon = 'cloud-showers-heavy'
    elif code in [1114, 1117, 1210, 1213, 1216, 1219, 1222, 1225, 1237, 1255, 1258, 1261, 1264, 1279, 1282]:
        icon = 'snowflake'
    elif code in [1087]:
        icon = 'cloud-bolt'
    else:
        icon = 'poo-storm'

    return icon


async def _get_weather(period: str, query: dict, api_key: str) -> dict:
    url = API_URL_SCAFFOLD.format(period)
    # HERE
    auth = { 'key': api_key}

    async with aiohttp.ClientSession() as s:
            async with s.get(url, params={**auth, **query}) as r:
                return await r.json()
