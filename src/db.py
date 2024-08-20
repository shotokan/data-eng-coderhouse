import psycopg2
import os


class WeatherRepo:
    def __init__(self):
        db_type = 'redshift+redshift_connector'
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

    
    def insert(self, df):
        df.to_sql(name='isabido86_coderhouse.weather_data', con=self.conn, index=False, if_exists='replace')
            
