"""
PyralleX2.visualise.py

Author: Neville B.-y. Yee
Date: 20-Feb-2021

Version: 0.1
"""

import os
import mrcfile
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def extract_image(mrc_in, image_no):
    """
    Extracts image from stack

    Args:
    mrc_in (str): Name of mrc file including images
    image_no (int): Index of image in stack

    Returns:
    nparray
    """

    # Check if input file is valid
    assert (os.path.isfile(mrc_in)), \
        "Error in visualise.extract_image: File not found."

    with mrcfile.open(mrc_in) as mrc:
        data = mrc.data
        assert (image_no < data.shape[0]), \
            "Error in visualise.extract_image: input image index exceeds stack size ({}).".format(data.shape[0])

    return data[image_no, :, :]


def display_image(
        mrc_in,
        spec_in,
        figsize,
        cmap,
):
    """
    Plot image using matplotlib

    Args:
    mrc_in (str): file containing intensities
    spec_in (str): file containing spectral data
    figsize (float): size (in inches) of displayed figure
    cmap (str): colour map code in matplotlib
    """

    # Check if input file is valid
    assert (os.path.isfile(mrc_in)), \
        "Error in visualise.display_image: MRC file not found."

    with mrcfile.open(mrc_in) as mrc:
        data = mrc.data

    assert (os.path.isfile(spec_in)), \
        "Error in visualise.display_image: Spec file not found."

    with mrcfile.open(spec_in) as spec:
        spectra = spec.data

    fig, ax = plt.subplots(1, 2, figsize=(figsize*2+1, figsize))
    fig.subplots_adjust(left=0.05, bottom=0.18, right=0.95, top=0.95)

    # set default to slice 0 with gamma=0.5
    image = data[0]**0.5
    show_obj = ax[0].imshow(image.T, cmap=cmap)

    spec_x = spectra[0]
    spec_y = spectra[1]
    spec_plot, = ax[1].plot(spec_x, spec_y)

    # define slider for gamma correction
    ax = fig.add_axes([0.15, 0.05, 0.75, 0.03])
    gamma_slider = Slider(ax, 'Gamma:', 0, 1, valinit=0.5)

    # define slider for stacks
    ax = fig.add_axes([0.15, 0.1, 0.75, 0.03])
    slider = Slider(ax, 'Image index:', 0, data.shape[0]-1, valinit=0, valfmt='%i')

    def update(val):
        """
        Method to update image according to slider value
        """
        index = int(slider.val)
        gamma = float(gamma_slider.val)
        image = data[index]**gamma
        show_obj.set_data(image.T)
        spec_plot.set_ydata(spectra[index+1])
        fig.canvas.draw()

    slider.on_changed(update)
    gamma_slider.on_changed(update)

    plt.show()
