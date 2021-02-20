from skbuild import setup

def main():
    setup(
        package_dir={"": "src"},
        packages={"PyralleX2"},
        install_requires=[],
    )

if __name__ == '__main__':
    main()
