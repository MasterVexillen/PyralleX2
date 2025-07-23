"""
pyrallex2.sample.py
Version: 0.1

AUTHOR: Neville Yee
Date: 4-Feb-2021
"""

import numpy as np
from sklearn.preprocessing import normalize

from icecream import ic

from . import cell_parse as Cell_parse
from . import io as IO
from .Data import atom_param as Atom_param


class Atom:
    """
    Class encapsulating Atom objects
    """

    def __init__(
            self,
            element=None,
            charge=None,
            width=None,
            pos=None,
            frac_pos=None,
    ):

        """
        Initialise an Atom object

        ARGS:
            element (str): Element name
            charge (int): Charge (atomic number) of atom
            width (float): Width (FWHM) of atom
            pos (nparray): Position of atom
            frac_pos (nparray): Fractional coordinates of atom
        """

        self.element = element
        self.charge = charge
        self.width = width
        self.pos = np.array(pos, dtype=np.float32)
        self.frac_pos = frac_pos

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
            cell_vec=None,
            supercell_dims=(1, 1, 1),
    ):

        """
        Initialise a Sample object

        ARGS:
            atom_list (list): list of Atom objects
            cell_vec (ndarray): cell vectors
        """
        self.atom_list = atom_list
        self.cell_vec = cell_vec
        self.supercell_dims = supercell_dims

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
        rot_axis = np.array(rot_axis, dtype=np.float32)
        rot_axis /= np.linalg.norm(rot_axis)
        angle = np.deg2rad(angle)

        rotated = vector * np.cos(angle) + \
            np.cross(rot_axis, vector) * np.sin(angle) + \
            rot_axis * np.dot(rot_axis, vector) * (1.-np.cos(angle))

        return rotated

    def rotate(self, rot_axis, angle):
        """
        Method to rotate whole cell
        """
        for vec in range(3):
            self.cell_vec[vec] = self._rodrigues(self.cell_vec[vec], rot_axis, angle)
        for count, atom in enumerate(self.atom_list):
            atom.pos = self._rodrigues(atom.pos, rot_axis, angle)


def create_sample(coords_file, cell_type, cell_vec, supercell_dims):
    """
    Create sample using given cell file

    ARGS:
        cell_filename (str): path to castep cell file

    RETURNS:
        Sample object
    """

    # Read cell file and create empty sample
    if coords_file.endswith(".xyz"):
        atom_list = IO.read_xyz(coords_file)
    if coords_file.endswith(".pdb"):
        atom_list = IO.read_pdb(coords_file)
    if coords_file.endswith(".cif"):
        atom_list = IO.read_cif(coords_file)

    atomtypes_array = np.array(atom_list, dtype=object)[:, 0].astype(str)
    position_array = np.concatenate(np.array(atom_list, dtype=object)[:, 1]).ravel().reshape((len(atomtypes_array), 3))
    position_array -= position_array[np.argmin(position_array, axis=1)]

    if cell_type == "Full":
        cell_vec = np.array(cell_vec).reshape((3,3))
    else:
        cell_vec = Cell_parse.Cell.niggly_to_cartesian(np.array(cell_vec).reshape((2,3)))

    my_sample = Sample(cell_vec=cell_vec,
                       supercell_dims=supercell_dims
    )

    # Calculate fractional position of atoms
    fractional_array = position_array @ np.linalg.inv(cell_vec.T)

    # Check if no atom is outside of defined unit cell
    assert (np.max(fractional_array) < 1), \
        "AssertionError: at least 1 atom is outside of the bounding box. Unit cell needs to be larger."

    # Load preset atom parameters
    atom_params = Atom_param.atom_params

    for index, atom in enumerate(atomtypes_array):
        curr_atom = Atom(element=atom,
                         charge=atom_params[atom_params['Name']==atom].Charge.values[0],
                         width=atom_params[atom_params['Name']==atom].Width.values[0],
                         pos=position_array[index],
                         frac_pos=fractional_array[index])
        my_sample.add_atom(curr_atom)
    my_sample.centre()

    return my_sample
