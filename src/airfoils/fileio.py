#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2017-2019 Airinnova AB and the Airfoils authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------

# Authors:
# * Aaron Dettmann

"""
Import airfoil data from a text file

Developed for Airinnova AB, Stockholm, Sweden.
"""

import re
import numpy as np

# Format identifiers
FORMAT_1 = 'format_1'
FORMAT_2 = 'format_2'

# If x-value deviates from 0 or 1 in this range, it is set to 0 or 1
DATA_TOLERANCE = 1e-3


class FileInputFormatError(Exception):
    """Raised if file input data is not formatted correctly"""

    pass


def import_airfoil_data(file_name):
    """
    Import airfoil data from a text file

    Args:
        :file_name: File name (string)

    Returns:
        :upper: Upper airfoil coordinates
        :lower: Lower airfoil coordinates
    """

    import_functions = {
        FORMAT_1: _import_format_1,
        FORMAT_2: _import_format_2,
    }

    # ----- Determine the file format -----
    file_format = None
    with open(file_name, 'r') as infile:
        for line_nr, line in enumerate(infile):

            if line_nr == 0:
                continue
            if line_nr == 2:
                break

            line = line.strip()

            try:
                data = np.fromstring(line, sep=' ')

                if data[0] > 2:
                    file_format = FORMAT_2
                else:
                    file_format = FORMAT_1
            except:
                # Fallback on format 1
                file_format = FORMAT_1

    # ----- Try to import the file -----
    if file_format is not None:
        upper, lower = import_functions[file_format](file_name)
    else:
        raise FileInputFormatError("Input file not recognised as valid airfoil file")

    return upper, lower


def _import_format_1(file_name):
    """
    Import airfoil data from a text file (format 1)

    FILE FORMAT:
        * First row is name of airfoil or comment
        * Columns for x- and y-coordinates
        * Data typically starts at x = 1

    Note:
        * Empty lines are ignored
        * Lines not starting with a number are ignored

    Args:
        :file_name: File name (string)

    Returns:
        :upper: Upper airfoil coordinates
        :lower: Lower airfoil coordinates
    """

    line_with_text = re.compile(r"^[a-z]", flags=re.IGNORECASE)
    line_with_not_number = re.compile(r"[^\+\-\d\.]")  # +,-,.,0,1,2,...,8,9

    x = []
    y = []
    with open(file_name, 'r') as infile:
        for line_nr, line in enumerate(infile):
            line = line.strip()

            if not line or line_with_text.match(line) or line_with_not_number.match(line):
                continue

            xy = np.fromstring(line, sep=' ')
            x.append(xy[0])
            y.append(xy[1])

    x = np.asarray(x)
    y = np.asarray(y)

    # Shift data points if necessary
    shift_factor = min(x)
    if shift_factor != 0:
        x -= shift_factor

    # Normalise data points if necessary
    norm_factor = max(x)
    x /= norm_factor
    y /= norm_factor

    # Account for numerical inaccuracies if necessary
    if abs(1 - x[0]) < DATA_TOLERANCE:
        x[0] = 1
    elif abs(1 - x[0]) < 1 + DATA_TOLERANCE:
        x[0] = 0

    x_upper = []
    y_upper = []
    x_lower = []
    y_lower = []

    if x[0] == 0:
        for i, xy in enumerate(zip(x, y)):
            x_upper.append(xy[0])
            y_upper.append(xy[1])

            if xy[0] == 1:
                break
        else:
            # If we did not break, something went wrong
            raise FileInputFormatError("Trailing edge point not found")

    elif x[0] == 1:
        for i, xy in enumerate(zip(x, y)):
            x_upper.append(xy[0])
            y_upper.append(xy[1])

            if xy[0] < DATA_TOLERANCE:
                break
        else:
            # If we did not break, something went wrong
            raise FileInputFormatError("Leading edge point not found")
    else:
        raise FileInputFormatError("Unable to process input file '{:s}'".format(file_name))

    x_lower = x[i:]
    y_lower = y[i:]

    upper = np.array([x_upper, y_upper])
    lower = np.array([x_lower, y_lower])

    # Swap upper and lower side if necessary
    if np.mean(y_lower) > np.mean(y_upper):
        upper, lower = lower, upper

    return upper, lower


def _import_format_2(file_name):
    """
    Import airfoil data from a text file (format 2)

    FILE FORMAT:
        * First row is name of airfoil or comment
        * Second row contains two columns with integers for the number of upper and lower x, y coordinates, respectively
        * Then there are two blocks of x- and y-coordinates,
          the first one for the upper points, the second one for the lower points

    Note:
        * Empty lines are ignored

    Args:
        :file_name: File name (string)

    Returns:
        :upper: Upper airfoil coordinates
        :lower: Lower airfoil coordinates
    """

    x_upper = []
    y_upper = []

    x_lower = []
    y_lower = []

    with open(file_name, 'r') as infile:
        for line_nr, line in enumerate(infile):
            line = line.strip()

            if not line:
                continue

            if line_nr == 0:
                continue

            # Fetch the number of upper and lower points
            if line_nr == 1:
                n_points = np.fromstring(line, sep=' ')
                n_upper = (line_nr+1, n_points[0]+2)
                n_lower = n_points[1]
                continue

            xy = np.fromstring(line, sep=' ')

            if n_upper[0] <= line_nr <= n_upper[1]:
                x_upper.append(xy[0])
                y_upper.append(xy[1])
            else:
                x_lower.append(xy[0])
                y_lower.append(xy[1])

        n_lower_actual = len(x_lower)
        if n_lower_actual != n_lower:
            raise RuntimeError(f"Expected {n_lower} points, got {n_lower_actual}")

    upper = np.asarray((x_upper, y_upper))
    lower = np.asarray((x_lower, y_lower))
    return upper, lower
