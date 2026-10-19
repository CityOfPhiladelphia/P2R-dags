from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
from airflow.providers.sftp.hooks.sftp import SFTPHook
from io import BytesIO

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



with DAG(
    dag_id="check_sftp_read_dag",
    start_date=datetime(2026,10,19),
    schedule_interval=None,
    catchup=False,
):

    test_read = PythonOperator(
        task_id="test_read_file",
        python_callable=check_sftp_read,
        op_kwargs={"sftp_conn_id": "SFTP_test"},
    )

    test_read