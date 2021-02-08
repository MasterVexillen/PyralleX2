"""
pyrallex2.screen.py
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
            dims=None,
            screen_shape=None,
            max_twotheta=None,
    ):

        """
        Initialise the detector screen

        ARGS:
            npix (int): number of pixels along horizontal/vertical axis
            dims (float): real dimensions of screen (in cm)
            max_twotheta (float): maximum two-theta angle on horizontal/vertical axis
            screen_shape (str): shape of detector screen (spherical / flat)
        """

        self.npix = npix
        self.dims = dims * 1.e8
        self.max_twotheta = max_twotheta
        self.screen_shape = screen_shape

        self.coords = (screen_shape, dims, npix, max_twotheta)

    @property
    def coords(self):
        """
        Absolute coordinates (normalised) of pixels on screen (=s)
        """
        return self._coords

    @coords.setter
    def coords(self, vals):
        self._coords = np.zeros((self.npix, self.npix, 3), dtype=np.float32)

        if self.screen_shape == 'flat':
            screen_dist = 0.5*self.dims / np.tan(np.radians(0.5*self.max_twotheta))
            dy = self.dims / self.npix
            dz = self.dims / self.npix
            ymin = -0.5*self.dims
            zmin = -0.5*self.dims
            for i in range(self.npix):
                for j in range(self.npix):
                    self._coords[i, j, :] = [screen_dist, ymin+i*dy, zmin+j*dz]

        elif self.screen_shape == 'cylindrical':
            screen_dist = self.dims / np.radians(self.max_twotheta)         # s = r*theta (in radians)
            theta_min = -0.5*np.radians(self.max_twotheta)
            dtheta = -2*theta_min / self.npix
            zmin = -0.5*self.dims
            dz = self.dims / self.npix
            for z_count in range(self.npix):
                ztemp   = zmin + z_count*dz
                for theta_count in range(self.npix):
                    azimuth = theta_min + theta_count*dtheta
                    xtemp   = screen_dist * np.cos(azimuth)
                    ytemp   = screen_dist * np.sin(azimuth)
                    self._coords[theta_count,z_count,:] = [xtemp, ytemp, ztemp]

        # Normalise coordinates of each pixel
        coords_norm = np.linalg.norm(self._coords, axis=2)
        for icount in range(self.npix):
            for jcount in range(self.npix):
                self._coords[icount, jcount] /= coords_norm[icount, jcount]

def create_screen(
        npix=None,
        dims=None,
        screen_shape=None,
        max_twotheta=None,
):

    """
    Create a new Screen object
    """

    return Screen(npix, dims, screen_shape, max_twotheta)
