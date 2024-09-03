from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from main import execute  # Importa la función desde src/main.py

# Define los argumentos por defecto del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define el DAG
dag = DAG(
    'daily_script_execution',
    default_args=default_args,
    description='Un DAG para ejecutar un script diariamente',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 9, 1),  # Ajusta la fecha de inicio según sea necesario
    catchup=False,
)

# Define el operador Python para ejecutar la función
run_script = PythonOperator(
    task_id='run_my_function',
    python_callable=execute,
    dag=dag,
)

# Define el flujo de trabajo (en este caso, solo una tarea)
run_script