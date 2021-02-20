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
python ${PYRA_PATH}/main.py TASK [config]
```
where `${PYRA_PATH}` is the folder containing the codebase. Currently allowed `TASK`s are:
* `new_config`: Creates new config (YAML) file as simulation inputs.
* `validate`: Validate an existing config file. Config file must be provided.
