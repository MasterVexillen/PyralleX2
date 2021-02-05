"""
pyrallex.sample.py
Version: 0.1

AUTHOR: Neville Yee
Date: 4-Feb-2021
"""

import numpy as np
from sklearn.preprocessing import normalize

class Atom:
    """
    Class encapsulating Atom objects
    """

    def __init__(
            self,
            element=None,
            charge=None,
            width=None,
            pos=None
    ):

        """
        Initialise an Atom object

        ARGS:
            element (str): Element name
            charge (int): Charge (atomic number) of atom
            width (float): Width (FWHM) of atom
            pos (nparray): Position of atom
        """

        self.element = element
        self.charge = charge
        self.width = width
        self.pos = np.array(pos, dtype=np.float32)

        self.atom_k = width

        @property
        def atom_k(self):
            """
            Gaussian factor depending on atomic width
            """
            return self._atom_k

        @atom_k.setter
        def _atom_k(self, var):
            self._atom_k = np.log(2.) / var**2

class Sample:
    """
    Class to define a sample
    """

    def __init__(
            self,
            atom_list=list(),
    ):

        """
        Initialise a Sample object
        """
        self.atom_list = atom_list

    def add_atom(self, atomObj):
        """
        Method to add an atom to the sample
        """
        self.atom_list.append(atomObj)

    def translation(self, trans_vec):
        """
        Method to translate the cell

        Args:
        trans_vec (nparray): the translation vector
        """
        for count, atom in enumerate(self.atom_list):
            atom.pos += np.array(trans_vec, dtype=np.float32)

    def centre(self):
        """
        Method to centre cell
        """
        # Calculate the current geometrical centroid
        centroid = np.zeros(3)
        for count, atom in enumerate(self.atom_list):
            centroid += atom.pos
        centroid /= len(self.atom_list)

        # Translate whole cell by original offset of centroid
        self.translation(-centroid)

    @staticmethod
    def _rodrigues(vector, rot_axis, angle):
        """
        Rodrigues' rotation formula to rotate an arbitrary vector

        ARGS:
        vector (nparray): original vector to be rotated
        rot_axis (nparray): rotational axis
        angle (float): angle at which vector is rotated

        RETURNS:
        vector (nparray): post-rotation vector
        """
        # Transform data for easier processing
        vector = np.array(vector, dtype=np.float32)
        rot_axis = normalize(np.array(rot_axis, dtype=np.float32)) # must be a unit vector
        angle = np.deg2rad(angle)

        rotated = vector * np.cos(angle) + \
            np.cross(rot_axis, vector) * np.sin(angle) + \
            rot_axis * np.dot(rot_axis, vector) * (1.-np.cos(angle))

        return rotated

    def rotate(self, rot_axis, angle):
        """
        Method to rotate whole cell
        """
        for count, atom in enumerate(self.atom_list):
            atom.pos = self._rodrigues(atom.pos, rot_axis, angle)
