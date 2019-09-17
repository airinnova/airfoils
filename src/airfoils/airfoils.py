#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2019 Airinnova AB and the Airfoils authors
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
Provides tools to create and modify airfoil objects

Developed for Airinnova AB, Stockholm, Sweden.
"""

from datetime import datetime
import os
import re

import numpy as np
from scipy.interpolate import interp1d
from scipy.misc import derivative
import matplotlib.pyplot as plt

POINTS_AIRFOIL = 200


class NACADefintionError(Exception):
    """Raised when the NACA identifier number is not valid"""

    pass


class Airfoil:

    def __init__(self, upper, lower):
        """
        Main constructor method

        Args:
            :upper: 2 x N array with x- and y-coordinates of the upper side
            :lower: 2 x N array with x- and y-coordinates of the lower side

        Note:
            * During initialisation data points are automatically ordered
              and normalised if necessary.
        """

        # Always use Numpy arrays
        upper = np.array(upper, dtype=float)
        lower = np.array(lower, dtype=float)

        # Unpack coordinates
        self._x_upper, self._y_upper = upper
        self._x_lower, self._y_lower = lower

        # Process coordinates
        self.norm_factor = 1
        self._order_data_points()
        self._normalise_data_points()

        # Make interpolation functions for 'y_upper' and 'y_lower'
        self._y_upper_interp = interp1d(
            self._x_upper,
            self._y_upper,
            kind='cubic',
            bounds_error=False,
            fill_value="extrapolate"
        )

        self._y_lower_interp = interp1d(
            self._x_lower,
            self._y_lower,
            kind='cubic',
            bounds_error=False,
            fill_value="extrapolate"
        )

    def __str__(self):
        return self.__class__.__name__ + "(upper, lower)"

    def __repr__(self):
        return self.__class__.__name__ + "(upper, lower)"

    def y_upper(self, x):
        return self._y_upper_interp(x)

    def y_lower(self, x):
        return self._y_lower_interp(x)

    @classmethod
    def NACA4(cls, naca_digits, n_points=POINTS_AIRFOIL):
        """
        Create an airfoil object from a NACA 4-digit series definition

        Note:
            * This is an alternative constructor method

        Args:
            :naca_digits: String like '4412'
            :points: Total number of points used to create the airfoil

        Returns:
            :airfoil: New airfoil instance
        """

        re_4digits = re.compile(r"^\d{4}$")

        if re_4digits.match(naca_digits):
            p = float(naca_digits[0])/10
            m = float(naca_digits[1])/100
            xx = float(naca_digits[2:4])/100
        else:
            raise NACADefintionError("Identifier not recognised as valid NACA 4 definition")

        upper, lower = gen_NACA4_airfoil(p, m, xx, n_points)
        return cls(upper, lower)

    @classmethod
    def morph_new_from_two_foils(cls, airfoil1, airfoil2, eta, n_points):
        """
        Create an airfoil object from a linear interpolation between two
        airfoil objects

        Note:
            * This is an alternative constructor method

        Args:
            :airfoil1: Airfoil object at eta = 0
            :airfoil2: Airfoil object at eta = 1
            :eta: Relative position where eta = [0, 1]
            :n_points: Number of points for new airfoil object

        Returns:
            :airfoil: New airfoil instance
        """

        if not 0 <= eta <= 1:
            raise ValueError(f"'eta' must be in range [0,1], given eta is {float(eta):.3f}")

        x = np.linspace(0, 1, n_points)

        y_upper_af1 = airfoil1.y_upper(x)
        y_lower_af1 = airfoil1.y_lower(x)
        y_upper_af2 = airfoil2.y_upper(x)
        y_lower_af2 = airfoil2.y_lower(x)

        y_upper_new = y_upper_af1*(1 - eta) + y_upper_af2*eta
        y_lower_new = y_lower_af1*(1 - eta) + y_lower_af2*eta

        upper = np.array([x, y_upper_new])
        lower = np.array([x, y_lower_new])

        return cls(upper, lower)

    @property
    def all_points(self):
        """
        Returns a single 2 x N array with x and y-coordinates in separate columns
        """

        all_points = np.array([
            np.concatenate((self._x_upper, self._x_lower)),
            np.concatenate((self._y_upper, self._y_lower))
        ])
        return all_points

    def _order_data_points(self):
        """
        Order the data points so that x-coordinate starts at 0
        """

        if self._x_upper[0] > self._x_upper[-1]:
            self._x_upper = np.flipud(self._x_upper)
            self._y_upper = np.flipud(self._y_upper)

        if self._x_lower[0] > self._x_lower[-1]:
            self._x_lower = np.flipud(self._x_lower)
            self._y_lower = np.flipud(self._y_lower)

    def _normalise_data_points(self):
        """
        Normalise data points so that x ranges from 0 to 1
        """

        self.norm_factor = abs(self._x_upper[-1] - self._x_upper[0])

        self._x_upper /= self.norm_factor
        self._y_upper /= self.norm_factor
        self._x_lower /= self.norm_factor
        self._y_lower /= self.norm_factor

    def plot(self, *, show=True, save=False, settings={}):
        """
        Plot the airfoil and camber line

        Note:
            * 'show' and/or 'save' must be True

        Args:
            :show: (bool) Create an interactive plot
            :save: (bool) Save plot to file
            :settings: (bool) Plot settings

        Plot settings:
            * Plot settings must be a dictionary
            * Allowed keys:

            'points': (bool) ==> Plot coordinate points
            'camber': (bool) ==> Plot camber
            'chord': (bool) ==> Plot chord
            'path': (str) ==> Output path (directory path, must exists)
            'file_name': (str) ==> Full file name

        Returns:
            None or 'file_name' (full path) if 'save' is True
        """

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlim([0, 1])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.axis('equal')
        ax.grid()

        ax.plot(self._x_upper, self._y_upper, '-', color='blue')
        ax.plot(self._x_lower, self._y_lower, '-', color='green')

        if settings.get('points', False):
            ax.plot(self.all_points[0, :], self.all_points[1, :], '.', color='grey')

        if settings.get('camber', False):
            x = np.linspace(0, 1, int(POINTS_AIRFOIL/2))
            ax.plot(x, self.camber_line(x), '--', color='red')

        if settings.get('chord', False):
            pass

        plt.subplots_adjust(left=0.10, bottom=0.10, right=0.98, top=0.98, wspace=None, hspace=None)

        if show:
            plt.show()

        if save:
            path = settings.get('path', '.')
            file_name = settings.get('file_name', False)

            if not file_name:
                now = datetime.strftime(datetime.now(), format='%F_%H%M%S')
                file_type = 'png'
                file_name = f'airfoils_{now}.{file_type}'

            fig.savefig(os.path.join(path, file_name))
            return file_name

    def camber_line(self, x):
        """
        Compute the camber line

        Method 1: y_camber = (y_upper + y_lower)/2

        Args:
            :x: Relative chordwise coordinate ranging from 0 to 1

        Returns:
            :camber_line: y-coordinates at given x positions
        """

        return (self.y_upper(x) + self.y_lower(x))/2

    def camber_line_angle(self, x):
        """
        Compute the camber line angle

        Args:
            :x: Relative chordwise coordinate ranging from 0 to 1

        Returns:
            :theta: Camber line angle at given x positions
        """

    ########################
        x = np.asarray(x)
        scalar_input = False

        if x.ndim == 0:
            x = x[None]  # Make 1D array
            scalar_input = True
    ########################

        dydx = derivative(self.camber_line, x, dx=1e-12)
        theta = np.rad2deg(np.arctan(dydx))
        theta = np.array([0 if abs(x) > 50 else x for x in theta])

    ########################
        if scalar_input:
            return np.squeeze(theta)
        return theta
    ########################


class MorphAirfoil:

    def __init__(self, airfoil1, airfoil2, n_points=POINTS_AIRFOIL):
        """
        Wrapper class that returns a morphed airfoil at specified eta position

        Attributes:
            :airfoil1: Airfoil object at eta = 0
            :airfoil2: Airfoil object at eta = 1
            :n_points: Number of points for new airfoil object
        """

        self.airfoil1 = airfoil1
        self.airfoil2 = airfoil2
        self.n_points = n_points

    def at_eta(self, eta):
        """
        Returns a new airfoil object at a given eta position

        Args:
            :eta: (float) eta position where eta = [0, 1]

        Returns:
            :morphed_airfoil: (obj) interpolated airfoil object at the given eta position
        """

        return Airfoil.morph_new_from_two_foils(
            self.airfoil1,
            self.airfoil2,
            eta=eta,
            n_points=self.n_points
        )


def gen_NACA4_airfoil(p, m, xx, n_points):
    """
    Generate upper and lower points for a NACA 4 airfoil

    Args:
        :p:
        :m:
        :xx:
        :n_points:

    Returns:
        :upper: 2 x N array with x- and y-coordinates of the upper side
        :lower: 2 x N array with x- and y-coordinates of the lower side
    """

    def yt(xx, xsi):
        # Thickness distribution

        a0 = 1.4845
        a1 = 0.6300
        a2 = 1.7580
        a3 = 1.4215
        a4 = 0.5075

        return xx*(a0*np.sqrt(xsi) - a1*xsi - a2*xsi**2 + a3*xsi**3 - a4*xsi**4)

    def yc(p, m, xsi):
        # Camber line

        def yc_xsi_lt_p(xsi):
            return (m/p**2)*(2*p*xsi - xsi**2)

        def dyc_xsi_lt_p(xsi):
            return (2*m/p**2)*(p - xsi)

        def yc_xsi_ge_p(xsi):
            return (m/(1 - p)**2)*(1 - 2*p + 2*p*xsi - xsi**2)

        def dyc_xsi_ge_p(xsi):
            return (2*m/(1 - p)**2)*(p - xsi)

        yc = np.array([yc_xsi_lt_p(x) if x < p else yc_xsi_ge_p(x) for x in xsi])
        dyc = np.array([dyc_xsi_lt_p(x) if x < p else dyc_xsi_ge_p(x) for x in xsi])

        return yc, dyc

    xsi = np.linspace(0, 1, n_points)

    yt = yt(xx, xsi)
    yc, dyc = yc(p, m, xsi)
    theta = np.arctan(dyc)

    x_upper = xsi - yt*np.sin(theta)
    y_upper = yc + yt*np.cos(theta)
    x_lower = xsi + yt*np.sin(theta)
    y_lower = yc - yt*np.cos(theta)

    upper = np.array([x_upper, y_upper])
    lower = np.array([x_lower, y_lower])

    return upper, lower
