# P2R-dags

Please see samples and documentation in [dags/samples](dags/samples).

## Secrets

DO NOT WRITE SECRETS DIRECTLY INTO DAG CODE, if you do please immediately contact Ryan Weast or Roland MacDavid for assistance.

Secrets are stored in the Airflow UI as Connections. Example in [dags/samples/secrets.py](dags/samples/secrets.py)

## Shared functions

For any shared functions or Python modules, place them in the
lib folder. Then, they can be imported like `import lib.file_name`
or `import lib.folder_name.file_name`. There is already an assortment
of generic helper functions in `lib.helpers`
