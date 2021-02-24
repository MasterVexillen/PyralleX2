"""
pyrallex2.simulation.py
Version: 0.3

AUTHOR: Neville Yee
Date: 4-Feb-2021
"""

import os
import time
import gc
import memory_profiler as mp
from tqdm import trange
import mrcfile
import numpy as np
from sklearn.preprocessing import normalize


class Simulation:
    """
    Class encapsulating a Simulation object
    """

    def __init__(
            self,
            sampleObj=None,
            screenObj=None,
            beamObj=None,
            mct=False,
            mct_rot_axis=None,
            mct_angle_step=None,
            mct_max_angle=None,
            bs_coverage=None,
    ):
        """
        Initialise a simulation.

        ARGS:
            sampleObj (obj): a Sample object
            screenObj (obj): a Screen object
            beamObj (obj): a Beam object
            mct (bool): switch for microtomography (series of scans)
            mct_rot_axis (list): rotation axis for mCT simulation
            mct_angle_step (float): step size of rotation angles for mCT simulation
            mct_max_angle (float): max rotation angles for mCT simulation
            bs_coverage (float): angular coverage of the lead backstop (to prevent central burnout)
        """

        self.sample = sampleObj
        self.screen = screenObj
        self.beam = beamObj
        self.mct = mct
        self.rot_axis = mct_rot_axis
        self.angle_step = mct_angle_step
        self.max_angle = mct_max_angle
        self.bs_coverage = bs_coverage

        if not mct:
            self.num_images = 1
        else:
            self.num_images = int((self.max_angle//self.angle_step) + 1)

        self.all_intensities = np.empty((self.screen.npix, self.screen.npix, self.num_images), dtype=np.float64)

    def _single_scan(self, index_in):
        """
        Method for performing a scan at a single angle

        RETURNS:
        Form factor & intensities array
        """

        # Form factor for single scan
        screen_s = (self.screen.coords-self.beam.beam_vec) / self.beam.wavelength
        screen_hkl = np.matmul(screen_s, self.sample.cell_vec.T)
        s_squared = np.linalg.norm(screen_s, axis=2)**2
        ssq2_const = -np.pi**2 * s_squared

        if self.sample.mode == 'crystal':
            thres = 500
            crystal_thetas = 2 * np.pi * screen_hkl
            crystal_kernals = 1 + 0.25 * np.sin((thres+1)*crystal_thetas) / np.sin(0.5*crystal_thetas+0.000001)
            crystal_term = np.prod(crystal_kernals, axis=-1)

        atom_fs0_array = np.array([atom.charge * np.exp(ssq2_const / atom.atom_k) \
                                   for atom in self.sample.atom_list]).T
        frac_pos_array = np.array([atom.frac_pos for atom in self.sample.atom_list]).T * 2j * np.pi

        def get_form_factor_atoms(hkl_in, frac_in):
            ff_iterator = trange(len(self.sample.atom_list),
                                 desc='Scanning image {:3d}/{:3d}... '.format(index_in+1, self.num_images),
                                 ncols=120,
            )
            for i in ff_iterator:
                form_factor_bare = atom_fs0_array[:, :, i] * np.exp(screen_hkl @ frac_pos_array[:, i])
                if self.sample.mode == 'crystal':
                    yield form_factor_bare * crystal_term
                else:
                    yield form_factor_bare

        form_factor_atoms = get_form_factor_atoms(screen_hkl, frac_pos_array)
        ss_form_factor = np.sum(form_factor_atoms, axis=2)
        del form_factor_atoms
        gc.collect()

        # Blot out centre
        screen_twotheta = np.degrees(np.arcsin(np.sqrt(s_squared)*self.beam.wavelength))
        ss_form_factor[screen_twotheta < self.bs_coverage] = 0
        ss_form_factor /= np.max(np.abs(ss_form_factor))

        ss_intensities = np.abs(ss_form_factor)**2

        return ss_intensities

    def full_scan(self):
        """
        Method for performing full tomographic scan
        """

        full_scan_iterator = range(self.num_images)
        for image_index in full_scan_iterator:
            ss_i = self._single_scan(image_index)
            self.all_intensities[:, :, image_index] = ss_i
            self.sample.rotate(self.rot_axis, self.angle_step)

    def get_intensity_prof(self, image_index):
        """
        Method for binning intensity profile

        ARGS:
        image_index (int): index of image in tomogram
        """

        image_flattened = self.all_intensities[:, :, image_index].flatten()
        image_flattened_log10 = np.log10(image_flattened)

        max_log_intensity = np.max(image_flattened_log10)

        return max_log_intensity


def create_simulation(
        sampleObj=None,
        screenObj=None,
        beamObj=None,
        mct=False,
        mct_rot_axis=None,
        mct_angle_step=None,
        mct_max_angle=None,
        bs_coverage=None,
):
    """
    Create a new Simulation object

    ARGS:
        sampleObj (obj): a Sample object
        screenObj (obj): a Screen object
        beamObj (obj): a Beam object
        mct (bool): switch for microtomography (series of scans)
        mct_rot_axis (list): rotation axis for mCT simulation
        mct_angle_step (float): step size of rotation angles for mCT simulation
        mct_max_angle (float): max rotation angles for mCT simulation
        bs_coverage (float): angular coverage of the lead backstop (to prevent central burnout)

    RETURNS:
        Simulation object
    """

    return Simulation(
        sampleObj,
        screenObj,
        beamObj,
        mct,
        mct_rot_axis,
        mct_angle_step,
        mct_max_angle,
        bs_coverage,
    )


def export_mrc(filename, simObj):
    """
    Write out stack intensities to MRC file

    Args:
    filename (str): name of the MRC file
    simObj (Simulation): the simulation object from simulations
    """

    # Check if file already exists
    assert (not os.path.isfile(filename)), \
        "Error in simulation.export_mrc: File already exists."

    # Swap axes to conform with mrc standard
    stack = np.moveaxis(simObj.all_intensities.astype(np.float32), 2, 0)

    with mrcfile.new(filename) as mrc:
        mrc.set_data(stack)
