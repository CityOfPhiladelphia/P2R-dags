"""
In Airflow, xcoms just refer to a way to share data between tasks.
In newer versions of Airflow, it can automatically handle doing the xcoms
for you behind the scene, like in the `xcom_etl_simple_example` function.
Notice how we can simply pass the output of one function as an input to the
next and it figures out the backend for us.
"""

from airflow.sdk import dag, task
import random


@dag(tags=["example"], schedule=None)
def xcom_etl_simple_example():
    @task
    def extract():
        """
        We simulate extracting data by generating a random number.
        In reality, we would likely be calling some api
        or scraping data.
        """
        return random.randrange(1, 100)

    @task
    def transform(raw_data):
        """
        Here we would probably parse JSON dictionaries or
        perform some calculations
        """
        return {"number": raw_data}

    @task
    def load(transformed_data):
        """
        Here we would likely load the data into a database
        or use some other API, we will just print out the final data
        for this sample
        """
        print(transformed_data)

    # You can run these one by one but it also works
    # to just use a one-liner
    load(transform(extract()))


xcom_etl_simple_example()
