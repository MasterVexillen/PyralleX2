"""
pyrallex.cell_parse.py
Version: 0.1

AUTHOR: Neville Yee
Date: 4-Feb-2021
"""

import re
import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize

from Pyrallex_revamped.sample import Atom, Sample


class Cell:
    """
    Class encapsulating Cell object
    """

    def __init__(
            self,
            cell_file=None,
    ):

        """
        Initialising a Cell object
        """
        self.cell_file = cell_file
        self.file_lines = cell_file

        self.position_type = cell_file
        self.lattice_type = cell_file

        self.atomtypes_array = cell_file
        self.lattice_array = cell_file
        self.position_array = cell_file
        self.fractional_array = cell_file

    @property
    def file_lines(self):
        """
        Read cell file to get lines for processing
        """
        return self._file_lines

    @file_lines.setter
    def file_lines(self, val):
        with open(self.cell_file, 'r') as f:
            lines = f.readlines()
            lines = [lines[i].strip('\n') for i in range(len(lines))]
        self._file_lines = lines

    @property
    def position_type(self):
        """
        Type of position vectors from source file
        """
        return self._position_type

    @position_type.setter
    def position_type(self, val):
        if '%BLOCK POSITIONS_ABS' in self._file_lines:
            self._position_type = 'abs'
        elif '%BLOCK POSITIONS_FRAC' in self._file_lines:
            self._position_type = 'frac'

    @property
    def lattice_type(self):
        """
        Type of lattice from source file
        """
        return self._lattice_type

    @lattice_type.setter
    def lattice_type(self, val):
        if '%BLOCK LATTICE_ABC' in self._file_lines:
            self._lattice_type = 'abc'
        elif '%BLOCK LATTICE_CART' in self._file_lines:
            self._lattice_type = 'cart'

    @property
    def atomtypes_array(self):
        """
        Array storing types of atoms in system
        """
        return self._atomtypes_array

    @atomtypes_array.setter
    def atomtypes_array(self, val):
        if self._position_type == 'abs':
            block_range = [self._file_lines.index('%BLOCK POSITIONS_ABS') + 1,
                           self._file_lines.index('%ENDBLOCK POSITIONS_ABS')]
        elif self._position_type == 'frac':
            block_range = [self._file_lines.index('%BLOCK POSITIONS_FRAC') + 1,
                           self._file_lines.index('%ENDBLOCK POSITIONS_FRAC')]

        atoms = np.array([re.split('\s+', self._file_lines[i].strip(' '))
                          for i in range(block_range[0], block_range[1])])
        self._atomtypes_array = atoms[:, 0]

    @property
    def lattice_array(self):
        """
        Array storing lattice information
        """
        return self._lattice_array

    @lattice_array.setter
    def lattice_array(self, val):
        if self._lattice_type == 'abc':
            lattice_range = [self._file_lines.index('%BLOCK LATTICE_ABC') + 1,
                             self._file_lines.index('%ENDBLOCK LATTICE_ABC')]
            lattice_niggly = np.array([re.split('\s+', self._file_lines[i].strip(' '))
                                       for i in range(lattice_range[0], lattice_range[1])], dtype=np.float64)
            self._lattice_array = self.niggly_to_cartesian(lattice_niggly)

        elif self._lattice_type == 'cart':
            lattice_range = [self._file_lines.index('%BLOCK LATTICE_CART') + 1,
                             self._file_lines.index('%ENDBLOCK LATTICE_CART')]
            self._lattice_array = np.array([re.split('\s+', self._file_lines[i].strip(' '))
                                            for i in range(lattice_range[0], lattice_range[1])], dtype=np.float64)

    @property
    def position_array(self):
        """
        Array storing position of atoms in system
        """
        return self._position_array

    @position_array.setter
    def position_array(self, val):
        if self._position_type == 'abs':
            block_range = [self._file_lines.index('%BLOCK POSITIONS_ABS') + 1,
                           self._file_lines.index('%ENDBLOCK POSITIONS_ABS')]
        elif self._position_type == 'frac':
            block_range = [self._file_lines.index('%BLOCK POSITIONS_FRAC') + 1,
                           self._file_lines.index('%ENDBLOCK POSITIONS_FRAC')]

        atoms = np.array([re.split('\s+', self._file_lines[i].strip(' '))
                          for i in range(block_range[0], block_range[1])])
        atom_positions = atoms[:, 1:].astype(np.float64)
        if self._position_type == 'abs':
            self._position_array = atom_positions
        elif self._position_type == 'frac':
            self._position_array = atom_positions @ self._lattice_array.T

    @property
    def fractional_array(self):
        """
        Array storing position of atoms in system
        """
        return self._fractional_array

    @fractional_array.setter
    def fractional_array(self, val):
        if self._position_type == 'abs':
            block_range = [self._file_lines.index('%BLOCK POSITIONS_ABS') + 1,
                           self._file_lines.index('%ENDBLOCK POSITIONS_ABS')]
        elif self._position_type == 'frac':
            block_range = [self._file_lines.index('%BLOCK POSITIONS_FRAC') + 1,
                           self._file_lines.index('%ENDBLOCK POSITIONS_FRAC')]

        atoms = np.array([re.split('\s+', self._file_lines[i].strip(' '))
                          for i in range(block_range[0], block_range[1])])
        atom_positions = atoms[:, 1:].astype(np.float64)
        if self._position_type == 'frac':
            self._fractional_array = atom_positions
        elif self._position_type == 'abs':
            self._fractional_array = atom_positions @ np.linalg.inv(self._lattice_array.T)

    @staticmethod
    def niggly_to_cartesian(niggly_in):
        """
        Convert lattice from reduced to cartesian
        """
        a, b, c = niggly_in[0]
        alpha, beta, gamma = np.radians(niggly_in[1])
        a1 = a
        b1 = b * np.cos(gamma)
        b2 = b * np.sin(gamma)
        c1 = c * np.cos(beta)
        c2 = c * (np.cos(alpha) - np.cos(beta)*np.cos(gamma)) / np.sin(gamma)
        c3 = np.sqrt(c**2 - c1**2 - c2**2)
        cart_out = np.array([[a1, 0., 0.],
                             [b1, b2, 0.],
                             [c1, c2, c3]], dtype=np.float64)
        return cart_out
