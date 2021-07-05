# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup


# Package meta-data
NAME = "dialect-map-core"
INFO = "Python package containing the core models of the Dialect Map"
URL = "https://github.com/dialect-map/dialect-map-core"
REQUIRES_PYTHON = ">=3.7, <4"
AUTHORS = "NYU DS3 Team"
VERSION = open("VERSION", "r").read().strip()


# Installation requirements
INSTALLATION_REQS = [
    "click==8.0.1",
    "psycopg2-binary==2.9.1",
    "sqlalchemy==1.4.20",
]

# Development requirements
DEVELOPMENT_REQS = [
    "black>=21.4b0",
    "coverage>=5.0.4",
    "mypy==0.910",
    "pre-commit>=2.13.0",
    "pytest>=6.2.2",
    "pytest-cov>=2.10.0",
]


setup(
    name=NAME,
    version=VERSION,
    description=INFO,
    author=AUTHORS,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"": ["data/*.json", "files/*.json"]},
    include_package_data=True,
    install_requires=INSTALLATION_REQS,
    extras_require={
        "dev": DEVELOPMENT_REQS,
    },
    entry_points={
        "console_scripts": [
            "dm-admin = dialect_map.cli:main",
        ],
    },
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    cmdclass={},
)
