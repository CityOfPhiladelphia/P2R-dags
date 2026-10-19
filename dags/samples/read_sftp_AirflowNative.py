from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
from airflow.providers.sftp.hooks.sftp import SFTPHook
from io import BytesIO
from airflow.sdk import dag, task
import lib.helpers


@dag(
    tags=["example"]
)
def check_sftp_example():
    # Default task is a Python task which just executes Python
    @task
    def check_sftp_read(
        SFTP_test
    ):
        # 1. Download file from SFTP (in-memory)
        sftp = SFTPHook(ftp_conn_id=SFTP_test)
        file_bytes = BytesIO()
    
        sftp.retrieve_file('/PRISM_Test/opa_properties_public.csv', file_bytes)
        file_bytes.seek(0)
    
        # 2. Read file (CSV example)
        df = pd.read_csv(file_bytes)
        print("File read successfully!")
        print(df.head(5))

    check_sftp_read()

check_sftp_example()
