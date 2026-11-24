from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
from airflow.providers.sftp.hooks.sftp import SFTPHook
from airflow.hooks.base import BaseHook
from io import BytesIO
import base64
from airflow.sdk import dag, task
import lib.helpers


@dag(
    tags=["example"]
)
def ETL_AirflowNativeHooks_XCom():
    # Default task is a Python task which just executes Python
    @task
    def extract() -> str:
        # Download file from SFTP
        sftp = SFTPHook(ssh_conn_id="SFTP_test")
        file_bytes = BytesIO()
        remote_path = '/PRISM_Test/opa_properties_public.csv'
        print("Connecting to ", BaseHook.get_connection("SFTP_test").host, remote_path)
        sftp.retrieve_file(remote_path, file_bytes)
        file_bytes.seek(0)
        return base64.b64encode(file_bytes.getvalue()).decode('utf-8')

    @task
    def transform(b64_data: str):
        # Read file
        buffer = base64.b64decode(b64_data)
        df = pd.read_csv(BytesIO(buffer))
        print("File read successfully!")
        print(df.head(5))

    transform(extract())

ETL_AirflowNativeHooks_XCom()