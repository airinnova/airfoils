#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from airfoils import Airfoil, MorphAirfoil


@pytest.fixture
def airfoil1():
    return Airfoil.NACA4('1234')


@pytest.fixture
def airfoil2():
    return Airfoil.NACA4('2412')


def test_basic(airfoil1, airfoil2):
    """
    TODO
    """

    morph = MorphAirfoil(airfoil1, airfoil2, n_points=200)
    morph.at_eta(eta=0.5)
