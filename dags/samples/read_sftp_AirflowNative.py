import pandas as pd
from airflow.providers.sftp.hooks.sftp import SFTPHook
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from io import BytesIO

def load_sftp_file_to_sql(
    sftp_conn_id,
    table_name,
):
    # 1. Download file from SFTP (in-memory)
    sftp = SFTPHook(ftp_conn_id=sftp_conn_id)
    file_bytes = BytesIO()

    sftp.retrieve_file('https://secure-ftp.phila.gov/#/PRISM_Test/opa_properties_public.csv', file_bytes)
    file_bytes.seek(0)

    # 2. Read file (CSV example)
    df = pd.read_csv(file_bytes)

    print(df.head(5))