"""
PyralleX2.main.py

Author: Neville B.-y. Yee
Date: 19-Feb-2021

Version: 0.4
"""

import sys
import os
import time

from icecream import ic

from . import sample as Sample
from . import beam as Beam
from . import screen as Screen
from . import simulation as Simulation
from . import params as Params
from . import visualise as Visualise
from . import magicgui as MagicGUI


def get_task():
    """
    Get task from user
    """

    task = sys.argv[1].lower()

    allowed_tasks = [
        'new_config',
        'validate',
        'simulate',
        'viewslice',
    ]
    assert (task in allowed_tasks), \
        "Error in main.get_task: input task not recognised."

    return task


def get_simulation_objs(params_in):
    """
    Prepare environment for simulation

    Arg:
    params_in (dict): dictionary containing parameters

    Returns:
    tuple
    """

    # Create sample for simulation
    my_sample = Sample.create_sample(coords_file=params_in['sample']['sample_file'],
                                     cell_type=params_in['sample']['cell_type'],
                                     cell_vec=params_in['sample']['cell_vec'],
                                     sample_crystal=params_in['sample']['sample_crystal'],
    )

    # Prepare X-ray beam
    my_beam = Beam.create_beam(
        wavelength=params_in['beam']['wavelength'],
        beam_vec=params_in['beam']['vector'],
    )

    # Prepare screen
    my_screen = Screen.create_screen(
        npix=params_in['screen']['pixels'],
        dims=params_in['screen']['dimensions'],
        screen_shape=params_in['screen']['shape'],
        max_twotheta=params_in['screen']['max_2_theta'],
        beam_axis=params_in['beam']['vector'],
    )

    # Create object for storing simulation data
    my_image = Simulation.create_simulation(
        my_sample,
        my_screen,
        my_beam,
        mct=params_in['simulation']['run_tomo'],
        mct_rot_axis=params_in['simulation']['rotational_axis'],
        mct_angle_step=params_in['simulation']['angle_step'],
        mct_max_angle=params_in['simulation']['max_angle'],
        bs_coverage=params_in['output']['backstop_coverage'],
    )

    return (my_sample, my_beam, my_screen, my_image)


def new_config():
    """
    Create new configuration file
    """
    args = MagicGUI.get_args_xray.show(run=True)

    # Check cell vector format
    if not isinstance(args.cell_vec.value, (list, tuple)):
        raise TypeError("Input error: cell vector must be either a list or a tuple")

    if args.cell_type.value=="Full":
        assert (len(args.cell_vec.value)==9), \
            "Input error: Full vector representation must have 9 components. USAGE: (ax, bx, cx, ay, by, cy, az, bz, cz)"
    elif args.cell_type.value=="Reduced":
        assert (len(args.cell_vec.value)==6), \
            "Input error: Reduced vector representation must have 6 components. USAGE: (a, b, c, alpha, beta, gamma)"

    Params.create_config(args)


def validate_config():
    """
    Validate given configuration file
    """
    assert (len(sys.argv)==2),\
        "Error: config file must be provided for task = 'validate'."
    config_name = sys.argv[1]
    assert (os.path.isfile(config_name)),\
        "Error: Config file not found."

    Params.validate_config(config_name)


def simulate():
    """
    Simulate system specified in configuration file
    """
    assert (len(sys.argv)==2),\
        "Error: config file must be provided for task = 'simulate'."
    config_name = sys.argv[1]
    assert (os.path.isfile(config_name)),\
        "Error: Config file not found."

    params = Params.read_config(config_name)
    sample, beam, screen, image = get_simulation_objs(params)

    # Let there be light (...x-ray)
    image.full_scan()

    # Export file
    mrc_name = params['output']['output_file']
    spectra_name = params['output']['spectra_file']
    Simulation.export_mrc(mrc_name, image)
    if len(spectra_name) > 0:
        Simulation.export_spectra(spectra_name, image)


def viewslice():
    """
    View simulated system according to configuration file
    """
    assert (len(sys.argv)==2),\
        "Error: config file must be provided for task = 'visualise'."
    config_name = sys.argv[1]
    assert (os.path.isfile(config_name)),\
        "Error: Config file not found."

    params = Params.read_config(config_name)
    mrc_file = params['display']['source']
    spec_file = params['display']['spec_source']

    assert (os.path.isfile(mrc_file)),\
        "Error: mrc file not found."

    Visualise.display_image(
        mrc_in=mrc_file,
        spec_in=spec_file,
        figsize=params['display']['figsize'],
        cmap=params['display']['cmap'],
    )


def clear():
    """
    Clear previous result files
    """
    user_input = input("This will erase all existing images and spectral data in this folder. Proceed? ([y]/n)) ").lower()

    if len(user_input)==0 or user_input=='y':
        os.system("rm *.mrc *.spec")
    elif user_input=='n':
        pass
    else:
        raise ValueError('Error in main.clear: Invalid input.')
