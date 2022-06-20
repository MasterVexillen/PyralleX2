from setuptools import setup, find_packages

<<<<<<< HEAD
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
        "memory_profiler",
        "tqdm",
        "icecream",
        "mrcfile",
        "magicgui",
        "pyqt5",
    ],
    entry_points = {
        "console_scripts": [
            "pyrallex2.clear=PyralleX2.src.PyralleX2.main:clear",
            "pyrallex2.new=PyralleX2.src.PyralleX2.main:new_config",
            "pyrallex2.validate=PyralleX2.src.PyralleX2.main:validate_config",
            "pyrallex2.simulate=PyralleX2.src.PyralleX2.main:simulate",
            "pyrallex2.visualise=PyralleX2.src.PyralleX2.main:viewslice",
        ]
    }
)
=======
def main():
    setup(
        package_dir={"": "src"},
        packages={"PyralleX2"},
        install_requires=[],
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

if __name__ == '__main__':
    main()
>>>>>>> fa56a72a3ec89b014dd7a1b4769f9bb57574b9f5
