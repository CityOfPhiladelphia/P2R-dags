"""
Receiving an email on the failure of a dag (or success) is a great
way to keep track of your DAGs without having to constantly login
to the Airflow UI.

This method is designed only for sending emails to ourselves (the data
engineers), and not for sending emails to a third party who may
be relevant to the process. For that purpose, you'll want to write a custom
email.
"""

from airflow.sdk import dag, task
import lib.helpers
import random


@dag(
    tags=["example"],
    # This sends an email when this dag fails only on prod
    # on_failure_callback=lib.helpers.dag_email(to="Ryan.Weast@phila.gov"),
    # To send an email on prod or dev, just do
    on_failure_callback=lib.helpers.dag_email(to="Ryan.Weast@phila.gov", dev=True),
    # Or to send an email just on dev
    # on_failure_callback=lib.helpers.dag_email(to="Ryan.Weast@phila.gov", prod=False, dev=True)
    #
    # Most likely, you are interested in receiving an email
    # when a dag fails, but you can technically receive an
    # email on a success too. This may be useful for DAGs
    # that run once a month or so
    on_success_callback=lib.helpers.dag_email(to="Ryan.Weast@phila.gov"),
)
def send_email_status_example():
    # This task exits randomly as either failure or success
    # to test both the on failure and on success email
    @task.bash
    def sample_task():
        return f"exit {random.randint(0, 1)}"

    sample_task()


send_email_status_example()
