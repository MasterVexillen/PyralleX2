from setuptools import setup, find_packages

setup(
    version="2.1a",
    name="PyralleX2",
    package_dir={"": "src"},
    packages=find_packages("PyralleX2"),
    zip_safe=False,
    install_requires=[
        "numpy",
        "scipy",
        "scikit-learn",
        "matplotlib",
        "pandas",
        "scikit-build",
        "pyyaml",
        "biopython",
        "pdbecif",
        "memory_profiler",
        "tqdm",
        "icecream",
        "mrcfile",
        "magicgui",
        "pyqt5",
    ],
    entry_points = {
        "console_scripts": [
            "pyrallex2.clear=PyralleX2.main:clear",
            "pyrallex2.new=PyralleX2.main:new_config",
            "pyrallex2.validate=PyralleX2.main:validate_config",
            "pyrallex2.simulate=PyralleX2.main:simulate",
            "pyrallex2.visualise=PyralleX2.main:viewslice",
        ]
    }
)
