#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pytest

from airfoils import Airfoil


def test_non_monotonic_data():
    x_upper = [0, +0.1, +0.1, +0.5, 1]
    y_upper = [0, +0.3, +0.3, +0.2, 0]
    x_lower = [0, +0.1, +0.5, 1]
    y_lower = [0, -0.3, -0.2, 0]

    upper = np.array([x_upper, y_upper])
    lower = np.array([x_lower, y_lower])

    Airfoil(upper, lower)

    # No error should be thrown here...
    # TODO: asserts...
