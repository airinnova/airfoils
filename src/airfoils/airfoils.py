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
Provides a class to create and modify an airfoil object

Developed for Airinnova AB, Stockholm, Sweden.
"""


import re

import numpy as np
from scipy.interpolate import interp1d
from scipy.misc import derivative
import matplotlib.pyplot as plt


class NACADefintionError(Exception):
    pass


class Airfoil:

    def __init__(self, upper, lower):
        """
        Main constructor method

        Args:
            :upper: (array) 2xn array with x and y coodinates of the upper side
            :lower: (array) 2xn array with x and y coodinates of the lower side

        Note:
            * During initialisation the data points are automatically ordered
              and normalised if necessary.
        """

        self.x_upper = upper[0]
        self.y_upper = upper[1]

        self.x_lower = lower[0]
        self.y_lower = lower[1]

        self.norm_factor = 1
        self._order_data_points()
        self._normalise_data_points()

    def __str__(self):
        return self.__class__.__name__ + "(upper, lower)"

    def __repr__(self):
        return self.__class__.__name__ + "(upper, lower)"

    @classmethod
    def NACA4(cls, naca_digits, n_points=100):
        """
        Create an airfoil object from a NACS 4-digit series definition.

        This is an alternative constructor method.

        Args:
            :naca_digits: (str) e.g. '4412'
            :points: (int) total number of points used to create the airfoil

        Returns:
            :airfoil: new airfoil instance
        """

        re_4digits = re.compile("^\d{4}$")

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
        Create a new airfoil object from a linear interpolation between two
        airfoil objects.

        This is an alternative constructor method.

        Args:
            :airfoil1: (obj) airfoil object at eta = 0
            :airfoil2: (obj) airfoil object at eta = 1
            :eta: (float) eta position where eta = [0, 1]
            :n_points: (int) number of points for new airfoil object

        Returns:
            :airfoil: new airfoil instance
        """

        if 0 > eta > 1:
            raise ValueError("eta must be in range [0,1], given eta is {:f}".format(float(eta)))

        xsi = np.linspace(0, 1, n_points)

        y_upper_af1, y_lower_af1 = airfoil1.interpolate_y(xsi)
        y_upper_af2, y_lower_af2 = airfoil2.interpolate_y(xsi)

        y_upper_new = y_upper_af1*(1 - eta) + y_upper_af2*eta
        y_lower_new = y_lower_af1*(1 - eta) + y_lower_af2*eta

        upper = np.array([xsi, y_upper_new])
        lower = np.array([xsi, y_lower_new])

        return cls(upper, lower)

    @property
    def all_points(self):
        """
        Returns a single 2xn array with x and y coordinates in separate columns.
        """

        all_points = np.array(
                [np.concatenate((self.x_upper, self.x_lower)),
                 np.concatenate((self.y_upper, self.y_lower))])

        return all_points

    def _order_data_points(self):
        """
        Order the data points so that coordinate start from 0
        """

        if self.x_upper[0] > self.x_upper[-1]:
            self.x_upper = np.flipud(self.x_upper)
            self.y_upper = np.flipud(self.y_upper)

        if self.x_lower[0] > self.x_lower[-1]:
            self.x_lower = np.flipud(self.x_lower)
            self.y_lower = np.flipud(self.y_lower)

    def _normalise_data_points(self):
        """
        Normalise data points so that x ranges from 0 to 1
        """

        self.norm_factor = abs(self.x_upper[-1] - self.x_upper[0])

        self.x_upper /= self.norm_factor
        self.y_upper /= self.norm_factor
        self.x_lower /= self.norm_factor
        self.y_lower /= self.norm_factor

    def interpolate_y(self, xsi):
        """
        Get the upper and lower y-coordinates of the airfoil for a given range
        of x (=xsi) values.

        The upper and lower coordinates are computed using a cubic spline
        interpolation.
        """

        y_upper = interp1d(self.x_upper, self.y_upper,
                           kind='cubic', bounds_error=False, fill_value="extrapolate")
        y_lower = interp1d(self.x_lower, self.y_lower,
                           kind='cubic', bounds_error=False, fill_value="extrapolate")
        return y_upper(xsi), y_lower(xsi)

###################
        # Note: scipy's CubicSpline() interpolation fails because the x-values
        # must be strictly increasing; this is not always given, especially at
        # the nose where the curvature can be relatively high

        # y_upper = CubicSpline(self.x_upper, self.y_upper)
        # y_lower = CubicSpline(self.x_lower, self.y_lower)
        # return y_upper(xsi), y_lower(xsi)
###################

###################
        # Note: accuracy problems
        # s=0: enforce curve to pass through all support points
        # per=False: do not consider curve as periodic

        # tck_y_upper, _ = splprep([self.x_upper, self.y_upper], task=0, s=0, per=False)
        # tck_y_lower, _ = splprep([self.x_lower, self.y_lower], task=0, s=0, per=False)

        # _, y_upper = splev(xsi, tck_y_upper)
        # _, y_lower = splev(xsi, tck_y_lower)

        # return y_upper, y_lower
###################

    def plot(self, *args, plot_for_seconds=None):
        """
        Plot the airfoil and camber line.
        """

        points = 'points'
        camber = 'camber'

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlim([0, 1])
        ax.set_xlabel('xsi')
        ax.set_ylabel('eta')
        ax.axis('equal')
        ax.grid()

        if points in args:
            ax.plot(self.all_points[0, :], self.all_points[1, :], '.', color='grey')

        ax.plot(self.x_upper, self.y_upper, '-', color='blue')
        ax.plot(self.x_lower, self.y_lower, '-', color='green')

        if camber in args:
            xsi = np.linspace(0, 1, 100)
            ax.plot(xsi, self.camber_line(xsi), '--', color='red')

        if plot_for_seconds is not None:
            plt.pause(plot_for_seconds)
            plt.show(block=False)
        else:
            plt.show()

    def camber_line(self, xsi):
        """
        Compute the camber line (method 1).

        Method 1: y_camber = (y_upper + y_lower)/2

        Args:
            :xsi: relative chordwise coordinate ranging from 0 to 1
        """

        y_upper, y_lower = self.interpolate_y(xsi)
        return (y_upper + y_lower)/2

    def camber_line_angle(self, xsi):
        """
        Compute the camber line angle

        Args:
            :xsi: relative chordwise coordinate ranging from 0 to 1
        """

    ########################
        xsi = np.asarray(xsi)
        scalar_input = False

        if xsi.ndim == 0:
            xsi = xsi[None]  # Make 1D array
            scalar_input = True
    ########################

        dydx = derivative(self.camber_line, xsi, dx=1e-12)
        theta = np.rad2deg(np.arctan(dydx))
        theta = np.array([0 if abs(x) > 50 else x for x in theta])

    ########################
        if scalar_input:
            return np.squeeze(theta)
        return theta
    ########################


class MorphAirfoil:

    def __init__(self, airfoil1, airfoil2, n_points=100):
        """
        Wrapper class which which can return a morphed airfoil object at a
        specified eta position.

        Attributes:
            :airfoil1: (obj) airfoil object at eta = 0
            :airfoil2: (obj) airfoil object at eta = 1
            :n_points: (int) number of points for new airfoil object
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

        return Airfoil.morph_new_from_two_foils(self.airfoil1,
                                                self.airfoil2,
                                                eta, self.n_points)


def gen_NACA4_airfoil(p, m, xx, n_points):
    """
    Generate the upper and lower points for a NACA 4 airfoil

    Args:
        :TODO:
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
