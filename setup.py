from setuptools import find_packages, setup

setup(
    name="pyconcorde",
    version="0.2.0",
    install_requires=[
        "dataclasses; python_version < '3.7'",
        "importlib_resources; python_version < '3.9'",
        "numpy",
        "tsplib95",
    ],
    packages=find_packages(),
    include_package_data=True,
    license="BSD",
    author="Joris Vankerschaver",
    author_email="joris.vankerschaver@gmail.com",
    url="https://github.com/jvkersch/pyconcorde",
    description="Python wrapper for the Concorde TSP executable",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
    ],
)
