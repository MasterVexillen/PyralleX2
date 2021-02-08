"""
atom_param.py
Version: 0.1

AUTHOR: Neville Yee
Date: 08-Feb-2021
"""

import pathlib
import pandas as pd

CURR_PATH = str(pathlib.Path(__file__).parent.absolute()) + '/'
atom_params = pd.read_csv(CURR_PATH+'Atoms.csv')
