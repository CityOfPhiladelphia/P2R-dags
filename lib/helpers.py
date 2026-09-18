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


def dag_email(to: str, prod: bool = True, dev: bool = False):
    """
    Minimal helper function to simplify emailing DAG status on either prod or dev
    This is only for emailing the data engineers ourselves,and contains internal
    information about the dag status. Not for sending out emails to third parties.
    To be used in an Airflow callback

    Args:
        to: Who to send the email to
        prod: Should the email be sent on prod, default True
        dev: Should the email be sent on dev, default False
    """
    from airflow.providers.smtp.notifications.smtp import SmtpNotifier

    if prod and os.environ["ENVIRONMENT"] == "prod":
        return SmtpNotifier(to=to)
    elif dev and os.environ["ENVIRONMENT"] == "dev":
        return SmtpNotifier(to=to)
    else:
        return None
