from airflow.sdk import dag, task
import lib.helpers


@dag(
    tags=["example"],
    schedule=lib.helpers.schedule(
        "30 2 * * *", dev=True, prod=False
    ),  # Run daily at 2:30am, only on dev
    catchup=False,
)
def hello_world_example():
    # Default task is a Python task which just executes Python
    @task
    def hello_world_python():
        print("Hello world from Python!")

    # A bash task ultimately runs a bash script but you can still use Python
    # inside of it to build out the bash script command
    @task.bash
    def hello_world_bash():
        message_to_the_world = "Hello world from Bash!"
        return f'echo "{message_to_the_world}"'

    hello_world1 = hello_world_python()
    hello_world2 = hello_world_bash()

    # Run hello_world2 after hello_world1
    hello_world1 >> hello_world2
    # Could also just do `hello_world_python() >> hello_world_bash()`


# You ultimately have to call the dag function directly for
# it to actually be created
hello_world_example()
