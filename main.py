"""
PyralleX2.main.py

Author: Neville B.-y. Yee
Date: 19-Feb-2021

Version: 0.4
"""

import sys
import os
import time

import PyralleX2.src.PyralleX2.sample as Sample
import PyralleX2.src.PyralleX2.beam as Beam
import PyralleX2.src.PyralleX2.screen as Screen
import PyralleX2.src.PyralleX2.simulation as Simulation
import PyralleX2.src.PyralleX2.params as Params
import PyralleX2.src.PyralleX2.visualise as Visualise


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
    my_sample = Sample.create_sample(params_in['sample']['sample_file'])

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
        Params.create_config(config_name)

    elif task == 'validate':
        assert (len(sys.argv)==3),\
            "Error: config file must be provided for task = 'validate'."
        config_name = sys.argv[2]
        assert (os.path.isfile(config_name)),\
            "Error: Config file not found."

        Params.validate_config(config_name)

    elif task == 'simulate':
        assert (len(sys.argv)==3),\
            "Error: config file must be provided for task = 'simulate'."
        config_name = sys.argv[2]
        assert (os.path.isfile(config_name)),\
            "Error: Config file not found."

        params = Params.read_config(config_name)
        sample, beam, screen, image = get_simulation_objs(params)

        # Let there be light (...x-ray)
        image.full_scan()

        # Export file
        mrc_name = params['output']['output_file']
        Simulation.export_mrc(mrc_name, image)

    elif task == 'viewslice':
        assert (len(sys.argv)==3),\
            "Error: config file must be provided for task = 'visualise'."
        config_name = sys.argv[2]
        assert (os.path.isfile(config_name)),\
            "Error: Config file not found."

        params = Params.read_config(config_name)
        mrc_file = params['display']['source']

        assert (os.path.isfile(mrc_file)),\
            "Error: mrc file not found."

        Visualise.display_image(
            mrc_in=mrc_file,
            gamma=params['display']['gamma_correction'],
            figsize=params['display']['figsize'],
            cmap=params['display']['cmap'],
        )

if __name__ == '__main__':
    main()
