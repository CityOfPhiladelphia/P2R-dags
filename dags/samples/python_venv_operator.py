"""
Python venv operator is a simple way to install extra python packages
that aren't available in the base image. However, it can lead to
inefficiencies for large packages that take a while to import.
"""

from airflow.sdk import dag, task


@dag(tags=["example"], schedule=None)
def python_venv_example():
    # This first virtualenv example doesn't use caching, which means that
    # every time it runs, it creates the venv from scratch, which
    # for some big python packages could add a lot of extra time.
    # This is NOT RECOMMENDED, but will work. Please see the next
    # example for recommended practices.
    @task.virtualenv(
        # Packages to install
        requirements=[
            "polars==1.38.1",
            # Torch is a massive machine learning Python package
            # that takes 30-60 seconds to install. We are installing it
            # here just to showcase the performance impact of
            # not caching venvs.
            "torch",
        ],
        # Whether or not to load system packages available to the host,
        # typically you want `False`` since the whole point of a virtual env
        # is to set up a special set of packages, but you can technically set
        # this to true to also have access to every package on the airflow system
        system_site_packages=False,
    )
    def polars_venv_uncached():
        # Imports must happen inside the task, not outside
        import polars as pl

        # Sample polars code to illustrate that the package was installed correctly
        df = pl.DataFrame({"test": [1, 2, 3], "status": ["hello", "world", "!"]})
        print(df)
        print("Hello world from Python virtual env!")

    # This second virtualenv example does use caching, which means that
    # it only has to download new packages the first time it runs. It will still
    # have a noticeable performance impact compared to a regular Python task
    # because it has to establish the virtualenv and import libraries, but it's
    # much less noticeable
    @task.virtualenv(
        requirements=[
            "polars==1.38.1",
            "torch",
        ],
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

        # Sample polars code to illustrate that the package was installed correctly
        df = pl.DataFrame({"test": [1, 2, 3], "status": ["hello", "world", "!"]})
        print(df)
        print("Hello world from Python virtual env!")

    # This third virtualenv example uses the same cached venv from polars_venv_cached,
    # but illustrates how to pass secrets using templating.
    #
    # The normal way to retreive connections, using BaseHook, don't work in venvs because
    # the airflow package isn't installed. So it uses templating, documented here:
    # https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html#airflow-connections-in-templates
    @task.virtualenv(
        requirements=[
            "polars==1.38.1",
            "torch",
        ],
        system_site_packages=False,
        venv_cache_path="~/venvs/polars-example",
    )
    def polars_venv_cached_with_secret(secret_val):
        # Imports must happen inside the task, not outside
        import polars as pl

        # Sample polars code to illustrate that the package was installed correctly
        df = pl.DataFrame({"test": [1, 2, 3], "status": ["hello", "world", "!"]})
        print(df)
        print("Hello world from Python virtual env!")
        # Print the secret
        print(f"Test secret password (auto-masked): {secret_val}")

    polars_venv_uncached()
    polars_venv_cached()
    polars_venv_cached_with_secret(secret_val="{{ conn.TestConnection.password }}")


python_venv_example()
