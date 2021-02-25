# PyralleX2
An X-ray diffraction simulation suite (WIP)

## Installation
1. Git clone repo
```
git clone https://github.com/MasterVexillen/PyralleX2.git
cd PyralleX2
```

2. Create virtual environment in miniconda and pre-install packages
```
conda create -n pyra-env
conda activate pyra-env
conda install --file requirements.txt
conda install --channel conda-forge mrcfiles
```

3. Build PyralleX2
```
python setup.py develop
```

## Running PyralleX2
1. Activate miniconda virtual environment
```
conda activate pyra-env
```

2. Execute PyralleX2
```
pyrallex2.TASK [config]
```
where `${PYRA_PATH}` is the folder containing the codebase. Currently allowed `TASK`s are:
* `clear`: Cleans the current folder, erasing all images and spectral data.
* `new`: Creates new config (YAML) file as simulation inputs.
* `validate`: Validate an existing config file. *Config file must be provided.*
* `simulate`: Perform simulation using parameters in config file. *Config file must be provided.*
* `visualise`: Display a slice from given stack. *Config file must be provided.*
