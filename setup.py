from skbuild import setup

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
