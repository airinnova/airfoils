#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from airfoils import Airfoil


def test_constructor_NACA4():
    """
    Test NACA 4-series constructor
    """

    wrong_naca_IDs = [
        'very_wrong',
        '12345',
        'NACA1234',
    ]

    for wrong_naca_ID in wrong_naca_IDs:
        with pytest.raises(ValueError):
            Airfoil.NACA4(wrong_naca_ID)


# TODO: assert that points have been created correctly
