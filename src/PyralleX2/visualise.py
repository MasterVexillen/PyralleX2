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
        gamma,
        figsize,
        cmap,
):
    """
    Plot image using matplotlib

    Args:
    mrc_in (ndarray): array containing intensities
    gamma (float): gamma correction of image
    figsize (float): size (in inches) of displayed figure
    cmap (str): colour map code in matplotlib
    """

    # Check if input file is valid
    assert (os.path.isfile(mrc_in)), \
        "Error in visualise.extract_image: File not found."

    with mrcfile.open(mrc_in) as mrc:
        data = mrc.data

    # apply gamma correction
    data = data**(gamma)

    fig, ax = plt.subplots(1, 1, figsize=(figsize, figsize))
    fig.subplots_adjust(left=0.05, bottom=0.15, right=0.95, top=0.95)

    # set default to slice 0
    image = data[0]
    show_obj = ax.imshow(image.T, cmap=cmap)

    # define slider
    ax = fig.add_axes([0.15, 0.05, 0.75, 0.03])
    slider = Slider(ax, 'Image index:', 0, data.shape[0]-1, valinit=0, valfmt='%i')

    def update(val):
        """
        Method to update image according to slider value
        """
        ind = int(slider.val)
        image = data[ind]
        show_obj.set_data(image.T)
        fig.canvas.draw()

    slider.on_changed(update)
#    plt.tight_layout()
    plt.show()
