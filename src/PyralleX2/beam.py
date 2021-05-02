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
            source=None,
            xray_wvl=None,
            el_energy=None,
            beam_vec=None,
    ):
        """
        Initialise the beam.

        ARGS:
           source (str): source of beam
           xray_wvl (float): wavelength (in ANGSTROMS) if xray 
           el_energy (float): energy (in eV) of beam if electron
           beam_vec (list/nparray): beam vector s0 (i.e. direction of beam)

        """

        self.beam_vec = normalize(np.array(beam_vec, dtype=np.float32).reshape(1, -1))[0]
        if source == 'xray':
            self.wavelength = xray_wvl
        elif source == 'electron':
            self.wavelength = 12398.4193 / np.sqrt(2.*el_energy*0.511e6)

            
def create_beam(
        source=None,
        xray_wvl=None,
        el_energy=None,
        beam_vec=None,
):
    """
    Create a new beam.

    ARGS:
        source (str): source of beam
        xray_wvl (float): wavelength (in ANGSTROMS) if xray 
        el_energy (float): energy (in eV) of beam if electron
        beam_vec (list/nparray): beam vector s0 (i.e. direction of beam)


    RETURNS:
        object: a Beam object
    """

    return Beam(source,
                xray_wvl,
                el_energy,
                beam_vec)
