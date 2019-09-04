#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
from pathlib import Path

import pytest

import airfoils.fileio as io

# ---------------------------------------------------------------------------
# Airfoil files downloaded from UIUC Airfoil Coordinates Database
#
# --> https://m-selig.ae.illinois.edu/ads/coord_database.html
#
# --> https://m-selig.ae.illinois.edu/ads/archives/coord_seligFmt.tar.gz (2019-09-04)
#
#     Unix tar archive of Version 2.0 (1550 airfoils):
#     [coord_seligFmt.tar.gz 618 kb]
#     Note that the files are in the Unix EOF format.
# ---------------------------------------------------------------------------

HERE = os.path.abspath(os.path.dirname(__file__))
AIRFOIL_DIR = os.path.join(HERE, 'airfoil_files')
AIRFOIL_FILES = glob.glob(os.path.join(AIRFOIL_DIR, '*'))

# File that have a wrong format (won't be supported)
AIRFOIL_FILES_BLACKLIST = [
    '2032c.dat',
    'fx74130wp2.dat',
    'fx74130wp2mod.dat',
    'goe187.dat',
    'goe188.dat',
    'goe235.dat',
    'joukowsk.dat',
    'naca23015.dat',
    'naca23018.dat',
    'naca23021.dat',
    'naca23024.dat',
    'naca2412.dat',
    'naca2415.dat',
    'naca2418.dat',
    'naca2421.dat',
    'naca2424.dat',
    'naca4412.dat',
    'naca4418.dat',
    'naca4421.dat',
    'naca4424.dat',
]


def test_uiuc_imports():
    """
    Test that UIUC files can be imported without error
    """

    for airfoil_file in AIRFOIL_FILES:
        airfoil_file_name = os.path.basename(airfoil_file)
        print(airfoil_file_name)

        if airfoil_file_name in AIRFOIL_FILES_BLACKLIST:
            continue

        upper, lower = io.import_airfoil_data(airfoil_file)


def test_empty_file():
    """
    Import of empty file must raise an error
    """

    empty_file = Path('empty.dat')
    empty_file.touch()

    with pytest.raises(io.FileInputFormatError):
        io.import_airfoil_data(empty_file)

    os.remove(empty_file)
