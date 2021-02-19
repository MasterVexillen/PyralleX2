"""
PyralleX2.main.py

Author: Neville B.-y. Yee
Date: 19-Feb-2021

Version: 0.1
"""

import sys
import os
import time

# import PyralleX2.sample as sample
# import PyralleX2.beam as beam
# import PyralleX2.screen as screen
# import PyralleX2.simulation as simulation
import PyralleX2.src.PyralleX2.params as params


def get_task():
    """
    Get task from user
    """

    task = sys.argv[1].lower()

    allowed_tasks = [
        'new_config',
        'validate',
        'simulate',
        'visualise',
    ]
    assert (task in allowed_tasks), \
        "Error in main.get_task: input task not recognised."

    return task


def main():
    """
    Main interface of PyralleX2
    """

    # Get task from user first
    task = get_task()

    if task == 'new_config':
        config_name = input("Name of new config file? (Default: config.yaml) ")
        if len(config_name) == 0:
            config_name = "config.yaml"
        params.create_config(config_name)

    elif task == 'validate':
        assert (len(sys.argv)==3),\
            "Error: config file must be provided for task = 'validate'."
        config_name = sys.argv[2]
        assert (os.path.isfile(config_name)),\
            "Error: Config file not found."

        params.validate_config(config_name)


if __name__ == '__main__':
    main()
