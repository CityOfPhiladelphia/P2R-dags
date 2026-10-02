"""
Python venv operator is a simple way to install extra python packages
that aren't available in the base image. However, it can lead to
inefficiencies for large packages that take a while to import.
"""

from airflow.sdk import dag, task
import importlib.metadata


@dag(tags=["example"], schedule=None)
def python_venv_example():
    # This first virtualenv example doesn't use caching, which means that
    # literally every time it runs, it creates the venv from scratch, which
    # for some big python packages could add a lot of extra time
    @task.virtualenv(
        # Packages to install
        requirements=["polars==1.38.1"],
        # Whether or not to load system packages available to the host,
        # typically you want false since the whole point of a virtual env
        # is to set up a special set of packages, but you can technically set
        # this to true to also have access to every package on the airflow system
        system_site_packages=False,
    )
    def polars_venv_uncached():
        # Imports must happen inside the task, not outside
        import polars as pl

        # Create a sample dataframe
        df = pl.DataFrame({"test": [1, 2, 3], "status": ["hello", "world", "!"]})
        print(df)
        print("Hello world from Python virtual env!")

    # This second virtualenv example does use caching, which means that
    # it only has to download new packages the first time it runs. It will still
    # have a noticeable performance impact compared to a regular Python task
    # because it has to establish the virtualenv and import libraries, but that
    # may not be an issue.
    @task.virtualenv(
        requirements=["polars==1.38.1"],
        system_site_packages=False,
        # Every venv_cache_path must start with "~/venvs/", as this is the path
        # to a shared folder. Each path must be unique for separate venvs. So,
        # if one task needs slightly different requirements than another,
        # you will need separate venvs for each, with different paths
        venv_cache_path="~/venvs/polars-example",
    )
    def polars_venv_cached():
        # Imports must happen inside the task, not outside
        import polars as pl

        # Create a sample dataframe
        df = pl.DataFrame({"test": [1, 2, 3], "status": ["hello", "world", "!"]})
        print(df)
        print("Hello world from Python virtual env!")

    # This third virtualenv example installs the apache-airflow-task-sdk, and
    # uses some clever code to make sure it installs the same version as Airflow
    # has installed, which allows you to retrieve connections
    @task.virtualenv(
        requirements=[
            f"polars==1.38.1, apache-airflow-task-sdk=={importlib.metadata.version('apache-airflow-task-sdk')}"
        ],
        system_site_packages=False,
        # Every venv_cache_path must start with "~/venvs/", as this is the path
        # to a shared folder. Each path must be unique for separate venvs. So,
        # if one task needs slightly different requirements than another,
        # you will need separate venvs for each, with different paths
        venv_cache_path="~/venvs/polars-example-2",
    )
    def polars_venv_with_task_sdk_cached():
        # Imports must happen inside the task, not outside
        import polars as pl

        # Now we can import from airflow.sdk
        from airflow.sdk import BaseHook
        import logging

        # Create a sample dataframe
        df = pl.DataFrame({"test": [1, 2, 3], "status": ["hello", "world", "!"]})
        print(df)
        print("Hello world from Python virtual env!")
        # Retrieve a connection
        test_secret = BaseHook.get_connection("TestConnection")
        logging.info(f"Test secret username (auto-masked): {test_secret.login}")
        logging.info(f"Test secret password (auto-masked): {test_secret.password}")

    polars_venv_uncached()
    polars_venv_cached()
    polars_venv_with_task_sdk_cached()


python_venv_example()
