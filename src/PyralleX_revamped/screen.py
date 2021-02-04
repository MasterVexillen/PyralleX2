"""
pyrallex.screen.py
Version: 0.1

AUTHOR: Neville Yee
Date: 4-Feb-2021
"""

import numpy as np
from sklearn.preprocessing import normalize

class Screen:
    """
    Class encapsulating a Screen object
    """

    def __init__(
            self,
            npix=None,
            screen_shape=None,
            max_twotheta=None,
    ):

        """
        Initialise the detector screen

        ARGS:
            npix (int): number of pixels along horizontal/vertical axis
            max_twotheta (float): maximum two-theta angle on horizontal/vertical axis
            screen_shape (str): shape of detector screen (spherical / flat)
        """

        self.npix = npix
        self.max_twotheta = max_twotheta
        self.screen_shape = screen_shape

        self.coords = (screen_shape, npix, max_twotheta)

        @property
        def coords(self):
            """
            Absolute coordinates (normalised) of pixels on screen (=s)
            """
            return self._coords

        @coords.setter
        def coords(self, vals):
            shape_in = vals[0]
            npix_in = vals[1]
            max_tt_in = vals[2]

            self._coords = np.empty((npix_in, npix_in, 3), dtype=np.float32)
            if shape_in == 'flat':
                # WLOG, assume centre of screen at unit distance from geometric centroid of sample
                self._coords[:, :, 0] = 1
                dx = np.tan(max_tt_in*0.5) * 2 / (npix_in-1)
                imin = -0.5*(npix_in-1)
                jmin = -0.5*(npix_in-1)

                for icount in range(npix_in):
                    self._coords[icount, :, 1] = (imin + icount)*dx
                for jcount in range(npix_in):
                    self._coords[:, jcount, 2] = (jmin + jcount)*dx

                self._coords = normalize(self._coords, axis=2)

            elif shape_in == 'spherical':
                d_angle = np.deg2rad(max_tt_in / (npix_in-1))
                for phi_count in range(npix_in):
                    curr_phi = (imin + phi_count) * d_angle
                    for theta_count in range(npix_in):
                        curr_theta = (jmin + theta_count) * d_angle
                        self._coords[phi_count, theta_count, 0] = np.sin(curr_theta) * np.cos(curr_phi)
                        self._coords[phi_count, theta_count, 1] = np.sin(curr_theta) * np.sin(curr_phi)
                        self._coords[phi_count, theta_count, 2] = np.cos(curr_theta)


def new_screen(
        npix=None,
        screen_shape=None,
        max_twotheta=None,
):

    """
    Create a new Screen object
    """

    return Screen(npix, screen_shape, max_twotheta)
