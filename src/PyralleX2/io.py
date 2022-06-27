"""
PyralleX2.io

AUTHOR: Neville B.-y. Yee
Date: 05-May-2021
"""

from icecream import ic


def read_xyz(file_path):
    """
    Function to read in xyz file and output as list of atoms and positions

    ARGS:
    file_path (str): path to xyz file

    RETURNS:
    list
    """

    with open(file_path, "r") as f:
        xyz_file = f.readlines()[2:]


    atom_list = []
    for line in xyz_file:
        element, pos = line.split()[0], [float(x) for x in line.split()[1:]]
        atom_list.append([element, pos])

    return atom_list


def read_pdb(file_path):
    """
    Function to read in pdb file and output as list of atoms and positions

    ARGS:
    file_path (str): path to pdb file

    RETURNS:
    list
    """
    import Bio.PDB as pdb

    from Bio.PDB.PDBExceptions import PDBConstructionWarning
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', PDBConstructionWarning)

    parser = pdb.PDBParser()
    structure = parser.get_structure("MySample", file_path)

    # Extract data
    atom_list = []
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    element = atom.element
                    pos = atom.get_coord()

                    # Fix element symbol casing issues
                    if len(element) > 1:
                        element = element[0].upper() + element[1:].lower()
                    atom_list.append([element, pos])

    return atom_list


def read_cif(file_path):
    """
    Function to read in cif file and output as list of atoms and positions

    ARGS:
    file_path (str): path to cif file

    RETURNS:
    list
    """
    from pdbecif.mmcif_io import CifFileReader
    import numpy as np

    data = CifFileReader().read(file_path, only=['_atom_site'])
    poly_id = data.keys()

    atom_list = []
    for curr_id in poly_id:
        elements = data[curr_id]['_atom_site']['type_symbol']
        for index, element in enumerate(elements):
            # Fix element symbol casing issues
            if len(element) > 1:
                elements[index] = element[0].upper() + element[1:].lower()

        x_pos = data[curr_id]['_atom_site']['Cartn_x']
        y_pos = data[curr_id]['_atom_site']['Cartn_y']
        z_pos = data[curr_id]['_atom_site']['Cartn_z']

        atom_list.append([[elements[i], np.array([float(x_pos[i]), float(y_pos[i]), float(z_pos[i])])] for i in range(len(elements))])

    return list([item for sublist in atom_list for item in sublist])
