.. image:: https://img.shields.io/pypi/v/airfoils.svg?style=flat
   :target: https://pypi.org/project/airfoils/
   :alt: Latest PyPI version

.. image:: https://img.shields.io/badge/license-Apache%202-blue.svg
    :target: https://github.com/airinnova/framat/blob/master/LICENSE.txt
    :alt: License

.. image:: https://readthedocs.org/projects/airfoils/badge/?version=latest
    :target: https://airfoils.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/airinnova/airfoils.svg?branch=master
    :target: https://travis-ci.org/airinnova/airfoils
    :alt: Build Status

.. image:: https://codecov.io/gh/airinnova/airfoils/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/airinnova/airfoils
    :alt: Coverage

|

.. image:: https://raw.githubusercontent.com/airinnova/airfoils/master/docs/source/_static/images/logo.png
    :alt: Airfoils
    :width: 100 px
    :scale: 100 %

*Airfoils* is a small *Python* library for object-oriented airfoil modelling. The library provides tools to easily instantiate airfoil objects and to query geometric information. An airfoil object is defined by upper and a lower surface coordinates.

.. figure:: https://raw.githubusercontent.com/airinnova/airfoils/master/docs/source/_static/images/airfoil_nomenclature.svg?sanitize=true
    :width: 700 px
    :align: center
    :target: https://github.com/airinnova/airfoils
    :alt: Example

    Airfoil nomenclature. Image in the public domain, via `Wikimedia Commons <https://commons.wikimedia.org/wiki/File:Wing_profile_nomenclature.svg>`_.

Features
--------

* Airfoil generation with a *NACA-4* series definition

* Import from files

    * Full support for airfoils from the `UIUC Airfoil Coordinates Database <https://m-selig.ae.illinois.edu/ads/coord_database.html>`_

* Interpolation or computation of airfoil geometry parameters

    * Upper and lower surface coordinates
    * Camber line coordinates
    * Chord line coordinates (TODO)
    * Thickness distribution (TODO)
    * Maximum thickness (TODO)

* Linear interpolation between two different airfoils (*MorphAirfoil*)

* Plotting of airfoils

Example
-------

.. code:: python

    >>> from airfoils import Airfoil
    >>> foil = Airfoil.NACA4('4812')
    >>> foil.plot()

.. image:: https://raw.githubusercontent.com/airinnova/airfoils/master/docs/source/_static/images/example.png
    :width: 600 px
    :target: https://github.com/airinnova/airfoils
    :alt: Example

.. code:: python

    >>> foil.y_upper(x=0.5)
    array(0.13085448)
    >>> foil.y_lower(x=[0.2, 0.6, 0.85])
    array([0.00217557, 0.02562315, 0.01451318])
    >>> foil.camber_line(x=0.5)
    0.07789290253609385


Installation
------------

.. code::

    pip install airfoils

Documentation
-------------

* https://airfoils.readthedocs.io/

License
-------

**License:** Apache-2.0
