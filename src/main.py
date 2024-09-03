import requests
import os
import pandas as pd
from datetime import datetime, timezone
import time

from db import WeatherRepo

class WeatherAPI:
    def __init__(self) -> None:
        key = os.getenv('API_WEATHER_KEY', '')
        self.__url = f'https://api.weatherapi.com/v1/current.json?key={key}'
    
    def getCurrent(self, city):
        current_weather_url = self.__url + f'&q={city}'
        response = requests.get(current_weather_url)
        if response.status_code == 200:
            return response.json()
        raise Exception(f'Error {response.status_code}: {response.text}')
    
    def get_df(self, data):
        location = data.get('location', {})
        current = data.get('current', {})

        data = {
            "name": location["name"],
            "region": location["region"],
            "country": location["country"],
            "lat": location["lat"],
            "lon": location["lon"],
            "tz_id":location["tz_id"],
            "localtime_epoch":location.get('localtime_epoch', 0),
            "local_time": location["localtime"],
            "current_last_updated_epoch": current.get('last_updated_epoch', 0),
            "current_last_updated": current["last_updated"],
            "current_temp_c": current["temp_c"],
            "current_temp_f": current["temp_f"],
            "current_is_day":current["is_day"],
            "current_condition_text": current["condition"]["text"],
            "current_condition_icon": current["condition"]["icon"],
            "current_condition_code": current["condition"]["code"],
            "current_humidity": current["humidity"],
            "current_cloud": current["cloud"],
            "current_feelslike_c": current["feelslike_c"],
            "current_feelslike_f": current["feelslike_f"],
            "current_wind_mph": current["wind_mph"],
            "current_wind_kph": current["wind_kph"],
            "current_wind_degree": current["wind_degree"],
            "current_wind_dir": current["wind_dir"]
        }
        df = pd.DataFrame([data])
        return df


def execute():
    api = WeatherAPI()
    cities = ['Merida', 'Telchac Pueblo', 'Motul']
    for city in cities:
        resp = api.getCurrent(city)
        print(resp)
        df = api.get_df(resp)
        repo = WeatherRepo()
        repo.insert(df)
