"""
pyrallex2.beam.py
Version: 0.1

AUTHOR: Neville Yee
Date: 4-Feb-2021
"""

import numpy as np
from sklearn.preprocessing import normalize

class Beam:
    """
    Class encapsulating a Beam object
    """

    def __init__(
            self,
            wavelength=None,
            beam_vec=None,
    ):
        """
        Initialise the beam.

        ARGS:
           wavelength (float): wavelength of beam (in ANGSTROMS)
           beam_vec (list/nparray): beam vector s0 (i.e. direction of beam)

        """

        self.wavelength = wavelength
        self.beam_vec = normalize(np.array(beam_vec, dtype=np.float32).reshape(1, -1))[0]


def create_beam(
        wavelength=None,
        beam_vec=None,
):
    """
    Create a new beam.

    ARGS:
        wavelength (float): wavelength of beam (in ANGSTROMS)
        beam_vec (list/nparray): beam vector (i.e. direction of beam)

    RETURNS:
        object: a Beam object
    """

    return Beam(wavelength,
                beam_vec)
