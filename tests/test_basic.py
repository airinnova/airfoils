#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import numpy as np
import pytest

from airfoils import Airfoil
import airfoils.__version__ as v

X_UPPER = [0, 0.1, 0.5, 1]
Y_UPPER = [0, 0.3, 0.2, 0]
X_LOWER = [0, 0.1, 0.5, 1]
Y_LOWER = [0, -0.3, -0.2, 0]

UPPER = np.array([X_UPPER, Y_UPPER])
LOWER = np.array([X_LOWER, Y_LOWER])

@pytest.fixture
def airfoil():
    return Airfoil(UPPER, LOWER)


def test_version():
    """
    Version
    """

    assert isinstance(v.VERSION, tuple)
    assert isinstance(v.__version__, str)


def test_str_and_repr(airfoil):
    """
    Check that repr and str look okay
    """

    assert str(airfoil) == 'Airfoil(upper, lower)'
    assert repr(airfoil) == 'Airfoil(upper, lower)'


def test_all_points(airfoil):
    """
    Test 'all_points' method
    """

    all_points = airfoil.all_points
    assert np.array_equal(all_points[0], np.concatenate([X_UPPER, X_LOWER]))
    assert np.array_equal(all_points[1], np.concatenate([Y_UPPER, Y_LOWER]))


def test_interpolate_y(airfoil):
    """
    Test 'interpolate_y' method
    """

    y_up, y_low = airfoil.interpolate_y(xsi=X_UPPER[1])
    assert y_up == Y_UPPER[1]
    assert y_low == Y_LOWER[1]


def test_camber_line(airfoil):
    """
    Test 'camber_line' method
    """

    # Symmetric airfoil (y-coordinate of camber line is 0)
    for xsi in np.linspace(0, 1, num=50):
        assert airfoil.camber_line(xsi) == 0


def test_camber_line_angle(airfoil):
    """
    Test 'camber_line_angle' method
    """

    # Symmetric airfoil (camber line angle is 0)
    for xsi in np.linspace(0, 1, num=50):
        assert airfoil.camber_line_angle(xsi) == 0


def test_morph_new_from_two_foils(airfoil):
    """
    Test that 'morph' constructor method works
    """

    Airfoil.morph_new_from_two_foils(airfoil1=airfoil, airfoil2=airfoil, eta=0.5, n_points=100)

    # TODO: add sensible tests here

    wrong_eta_values = [
        -0.1,
        1.2,
    ]

    for wrong_eta in wrong_eta_values:
        with pytest.raises(ValueError):
            Airfoil.morph_new_from_two_foils(airfoil1=airfoil, airfoil2=airfoil, eta=wrong_eta, n_points=100)


def test_reordering():
    """
    Coordinates sorted from trailing edge to leading edge have to be reordered
    """

    x_upper = X_UPPER[::-1]
    y_upper = Y_UPPER[::-1]
    x_lower = X_LOWER[::-1]
    y_lower = Y_LOWER[::-1]

    Airfoil((x_upper, y_upper), (x_lower, y_lower))


def test_plotting():
    """
    Test plotting function
    """

    settings = {
        'points': True,
        'camber': True,
        'file_name': 'test.png',
    }

    file_name = Airfoil.NACA4('2412').plot(save=True, settings=settings)
    assert os.path.isfile(file_name)
