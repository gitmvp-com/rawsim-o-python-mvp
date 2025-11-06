#!/usr/bin/env python3
"""Setup script for RAWSim-O Python MVP."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="rawsim-o-python",
    version="0.1.0",
    author="RAWSim-O Python MVP Contributors",
    description="Python-based discrete event simulation for Robotic Mobile Fulfillment Systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitmvp-com/rawsim-o-python-mvp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "pygame>=2.1.0",
        "pyyaml>=6.0",
        "click>=8.0.0",
        "colorama>=0.4.4",
        "tqdm>=4.62.0",
        "sortedcontainers>=2.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.910",
        ],
        "performance": [
            "numba>=0.54.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "rawsim-cli=cli:main",
            "rawsim-visual=visualization:main",
            "rawsim-generate=generate_instance:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
