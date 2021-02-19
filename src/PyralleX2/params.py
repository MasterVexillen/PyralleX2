"""
PyralleX2.params.py

Author: Neville B.-y. Yee
Date: 19-Feb-2021

Version: 0.1
"""

import os
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

    assert (os.path.isfile(filename_in)), \
        "Error in params.read_config: File not found."

    with open(filename_in, 'r') as f:
        params = yaml.load(f, Loader=yaml.FullLoader)

    return params


def validate_config(filename_in):
    """
    Validate parameters from yaml file

    Args:
    filename_in (str): filename of the input yaml file

    Output:
    bool
    """

    params = read_config(filename_in)

    # Check sample cell file
    assert (len(params['sample']['sample_file']) > 0),\
        "Error in params.validate: sample_file must be valid file name for cell file."
    assert (os.path.isfile(params['sample']['sample_file'])),\
        "Error in params.validate: Input Cell file not found."

    # Check beam group params
    assert (isinstance(params['beams']['wavelength'], float) and \
            params['beams']['wavelength'] > 0),\
        "Error in params.validate: Wavelength must be a float > 0."
    assert (isinstance(params['beams']['vector'], list) and \
            len(params['beams']['vector'])==3),\
        "Error in params.validate: Beam vector must be a list of length 3."

    # Check screen group params
    assert (isinstance(params['screen']['pixels'], int) and \
            params['screen']['pixels'] > 0),\
        "Error in params.validate: Screen pixels must be an int > 0."
    assert (params['screen']['shape'] in ['cylindrical', 'flat']),\
        "Error in params.validate: Screen shape must be either 'cylindrical' or 'flat'."
    assert (isinstance(params['screen']['dimensions'], float) \
            and params['screen']['dimensions'] > 0),\
            "Error in params.validate: Screen dimensions must be a float > 0."
    assert (isinstance(params['screen']['max_2_theta'], float) and \
            params['screen']['max_2_theta'] > 0),\
            "Error in params.validate: Screen dimensions must be a float > 0."

    # Check simulation group params
    assert (isinstance(params['simulation']['run_tomo'], bool)),\
        "Error in params.validate: run_tomo must be either 'true' or 'false'."
    assert (isinstance(params['simulation']['rotational_axis'], list) and \
            len(params['simulation']['rotational_axis'])==3),\
            "Error in params.validate: Rotational axis must be a list of length 3."
    assert (isinstance(params['simulation']['angle_step'], int) and \
            params['simulation']['angle_step'] > 0), \
            "Error in params.validate: angle_step must be an int > 0."
    assert (isinstance(params['simulation']['max_angle'], int) and \
            params['simulation']['max_angle'] >= params['simulation']['angle_step'] and \
            params['simulation']['max_angle'] % params['simulation']['angle_step'] == 0), \
            "Error in params.validate: max_angle must be an integral multiple of angle_step."

    # Check output group params
    assert (isinstance(params['output']['backstop_coverage'], float) and \
            params['output']['backstop_coverage'] > 0),\
            "Error in params.validate: backstop_coverage must be a float > 0."
    assert (isinstance(params['output']['gamma_correction'], float) and \
            0 <= params['output']['gamma_correction'] < 1),\
            "Error in params.validate: backstop_coverage must be a float and between 0 and 1."
    assert (len(params['output']['output_file']) > 0),\
        "Error in params.validate: output_file must be valid file name for the output."
