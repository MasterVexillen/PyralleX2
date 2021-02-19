"""
PyralleX2.params.py

Author: Neville B.-y. Yee
Date: 19-Feb-2021

Version: 0.1
"""

import yaml

def create_config(filename_in):
    """
    Create a new config file

    Args:
    filename_in (str): filename of the output yaml file
    """

    config_dict = {
        'sample': {
            'sample_file': '',
        },

        'beam': {
            'wavelength': 1.5418,
            'vector': [1, 0, 0],
        },

        'screen': {
            'pixels': 120,
            'shape': 'cylindrical',
            'dimensions': 50,
            'max_2_theta': 80,
        },

        'simulation': {
            'run_tomo': False,
            'rotational_axis': [0, 0, 1],
            'angle_step': 3,
            'max_angle': 180,
        },

        'output': {
            'backstop_coverage': 5,
            'gamma_correction': 0.5,
            'format': 'mrc',
            'output_file': '',
        }
    }

    with open(filename_in, 'w') as f:
        yaml.dump(config_dict, f, indent=4, sort_keys=False)


def read_config(filename_in):
    """
    Read parameters from yaml file

    Args:
    filename_in (str): filename of the input yaml file

    Output:
    dict
    """

    with open(filename_in, 'r') as f:
        params = yaml.load(f, Loader=yaml.FullLoader)

    return params
