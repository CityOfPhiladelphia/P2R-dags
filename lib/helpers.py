import os


def schedule(cron: str, prod: bool = False, dev: bool = False):
    """
    Minimal helper function to simplify scheduling a DAG on either prod or dev

    Args:
        cron: Cron schedule string
        prod: Should this be scheduled on prod
        dev: Should this be scheduled on dev
    """
    if prod and os.environ["ENVIRONMENT"] == "prod":
        return cron
    elif dev and os.environ["ENVIRONMENT"] == "dev":
        return cron
    else:
        return None


def is_prod() -> bool:
    """
    Minimal helpful function to determine if Airflow is production
    """
    return os.environ["ENVIRONMENT"] == "prod"
