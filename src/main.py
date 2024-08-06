import requests
import os
import psycopg2
from datetime import datetime, timezone

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


class WeatherRepo:
    def __init__(self):
        db_name = os.getenv('DB_NAME', '')
        db_user = os.getenv('DB_USER', '')
        db_password = os.getenv('DB_PASSWORD', '')
        db_host = os.getenv('DB_HOST', '')
        db_port = os.getenv('DB_PORT', '')
        self.conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    
    def insert_weather_data(self, api_response):
        # Extract data from the API response
        location = api_response.get('location', {})
        current = api_response.get('current', {})
        
        # Preparing the parameterized SQL query
        insert_query = """
        INSERT INTO isabido86_coderhouse.weather_data (
            name, region, country, lat, lon, tz_id, localtime_epoch, local_time,
            current_last_updated_epoch, current_last_updated, current_temp_c,
            current_temp_f, current_is_day, current_condition_text, current_condition_icon,
            current_condition_code, current_humidity, current_cloud, current_feelslike_c,
            current_feelslike_f, current_wind_mph, current_wind_kph, current_wind_degree,
            current_wind_dir
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
        );
        """

        # Prepare the values ​​to be inserted
        values = (
            location.get('name', ''),
            location.get('region', ''),
            location.get('country', ''),
            location.get('lat', 0),
            location.get('lon', 0),
            location.get('tz_id', ''),
            location.get('localtime_epoch', 0),
            datetime.fromtimestamp(location.get('localtime_epoch', 0), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
            current.get('last_updated_epoch', 0),
            datetime.fromtimestamp(current.get('last_updated_epoch', 0), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
            current.get('temp_c', 0),
            current.get('temp_f', 0),
            current.get('is_day', 0),
            current.get('condition', {}).get('text', ''),
            current.get('condition', {}).get('icon', ''),
            current.get('condition', {}).get('code', 0),
            current.get('humidity', 0),
            current.get('cloud', 0),
            current.get('feelslike_c', 0),
            current.get('feelslike_f', 0),
            current.get('wind_mph', 0),
            current.get('wind_kph', 0),
            current.get('wind_degree', 0),
            current.get('wind_dir', '')
        )
        # Execute the query in the database
        with self.conn.cursor() as cursor:
            cursor.execute(insert_query, values)
            self.conn.commit()


if __name__ == "__main__":
    api = WeatherAPI()
    cities = ['Merida', 'Telchac Pueblo', 'Motul']
    for city in cities:
        resp = api.getCurrent(city)
        print(resp)
        repo = WeatherRepo()
        repo.insert_weather_data(resp)