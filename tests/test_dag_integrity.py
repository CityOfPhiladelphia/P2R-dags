from airflow.models import DagBag
import os


# =========== MONKEYPATCH OS.ENVIRON DIRECTLY ===========
# We are doing this because dags will sometimes read environment variables
# to configure their structure, but those environment variables don't exist in
# the test environment. This will overwrite the core os.environ[] method to
# return a mock value instead of an error.
_orig_getitem = os.environ.__class__.__getitem__
_orig_get = os.environ.__class__.get


def mock_getitem(self, key):
    try:
        return _orig_getitem(self, key)
    except KeyError:
        # Mock Airflow connection env
        if key.upper().startswith("AIRFLOW_CONN_"):
            return f"scheme://MOCKED_{key.upper()}_VALUE:abcd@host.tld:1234"
        raise KeyError


def mock_get(self, key, default=None):
    if key.upper().startswith("AIRFLOW_CONN_"):
        return f"scheme://MOCKED_{key.upper()}_VALUE:abcd@host.tld:1234"

    return _orig_get(self, key, default)


# Apply the patches
os.environ.__class__.__getitem__ = mock_getitem
os.environ.__class__.get = mock_get
# =========== /MONKEYPATCH OS.ENVIRON ===========


def test_dagbag_has_no_import_errors():
    # Setting include_examples to False keeps the test fast
    dag_bag = DagBag(include_examples=False)

    # If there are any syntax errors or missing packages, import_errors will not be empty
    assert len(dag_bag.import_errors) == 0, (
        f"DAG import errors: {dag_bag.import_errors}"
    )
    # Iterate through all loaded DAGs and validate their structure
    validated_dags = 0
    for dag_id, dag in dag_bag.dags.items():
        # Validate the DAG
        assert dag.validate() is None, f"DAG failed validation test: {dag_id}"
        validated_dags += 1
    print(f"Validated {str(validated_dags)} DAGs.")
    if validated_dags < 400:
        raise Exception("Too few dags! Did dag factory fail?")
