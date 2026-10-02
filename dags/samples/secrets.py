from airflow.sdk import dag, task, BaseHook
import lib.helpers

# You can use print or logging
import logging


@dag(
    tags=["example"],
)
def secrets_example():
    @task
    def secrets_example():
        # Always retrieve secrets inside of tasks!
        # Do not retrieve them at the dag level
        test_secret = BaseHook.get_connection("TestConnection")
        logging.info(f"Test secret username: {test_secret.login}")
        logging.info(f"Test secret password (auto-masked): {test_secret.password}")

    @task
    def secrets_example2():
        # If two tasks use the same secret, you should retrieve the
        # secret individually in each task, do not pass secrets
        # between tasks or place them in XCOM
        test_secret = BaseHook.get_connection("TestConnection")
        logging.info(f"Test secret username: {test_secret.login}")
        logging.info(f"Test secret password (auto-masked): {test_secret.password}")

    secrets_example() >> secrets_example2()


# You ultimately have to call the dag function directly for
# it to actually be created
secrets_example()
