"""
PyralleX2.params.py

Author: Neville B.-y. Yee
Date: 19-Feb-2021

Version: 0.1
"""

import os
import yaml

def create_config(args_in):
    """
    Create a new config file

    Args:
    args_in (str) :: Input arguments
    """

    config_dict = {
        'sample': {
            'sample_file': str(args_in.sample_file.value),
            'sample_crystal': args_in.sample_crystal.value,
            'cell_type': args_in.cell_type.value,
            'cell_vec': list(args_in.cell_vec.value),
        },

        'beam': {
            'wavelength': args_in.beam_type.value.value,
            'vector': args_in.beam_vector.value,
        },

        'screen': {
            'pixels': args_in.screen_size_px.value,
            'shape': args_in.screen_shape.value,
            'dimensions': args_in.screen_dims_A.value,
            'max_2_theta': args_in.screen_max2theta.value,
        },

        'simulation': {
            'run_tomo': args_in.tomo.value,
            'rotational_axis': args_in.rot_axis.value,
            'angle_step': args_in.angle_step.value,
            'max_angle': args_in.max_angle.value,
        },

        'output': {
            'backstop_coverage': args_in.bs_coverage.value,
            'format': 'mrc',
            'output_file': str(args_in.output_file.value),
            'spectra_file': '',
        },

        'display': {
            'source': '',
            'spec_source': '',
            'figsize': 9.,
            'cmap': 'gist_yarg',
        }
    }

    with open(str(args_in.config_file.value), 'w') as f:
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
    """

    params = read_config(filename_in)

    # Check sample cell file
    assert (len(params['sample']['sample_file']) > 0),\
        "Error in params.validate: sample_file must be valid file name for cell file."
    assert (os.path.isfile(params['sample']['sample_file'])),\
        "Error in params.validate: Input Cell file not found."

    # Check beam group params
    assert (isinstance(params['beam']['wavelength'], float) and \
            params['beam']['wavelength'] > 0),\
        "Error in params.validate: Wavelength must be a float > 0."
    assert (isinstance(params['beam']['vector'], list) and \
            len(params['beam']['vector'])==3),\
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
    assert (len(params['output']['output_file']) > 0),\
        "Error in params.validate: output_file must be valid file name for the output."
    assert (len(params['output']['spectra_file']) > 0),\
        "Error in params.validate: spectra_file must be valid file name for the output."
