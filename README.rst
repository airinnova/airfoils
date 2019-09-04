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

*Airfoils* is a small Python library for object-oriented airfoil modelling. Airfoil objects can be imported from files. Airfoil definitions hosted on the `UIUC Airfoil Coordinates Database <https://m-selig.ae.illinois.edu/ads/coord_database.html>`_ are supported. Alternatively, airfoil objects can be instantiated from a NACA-4-series definition.

.. figure:: https://raw.githubusercontent.com/airinnova/airfoils/master/docs/source/_static/images/airfoil_nomenclature.svg?sanitize=true
    :width: 700 px
    :align: center
    :target: https://github.com/airinnova/airfoils
    :alt: Example

    Airfoil nomenclature. Image in the public domain, via `Wikimedia Commons <https://commons.wikimedia.org/wiki/File:Wing_profile_nomenclature.svg>`_.

Examples
--------

**NACA 4-series airfoils**

.. code:: python

    >>> from airfoils import Airfoil
    >>> naca4412 = Airfoil.NACA4('4412')
    >>> naca4412.plot()

.. image:: https://raw.githubusercontent.com/airinnova/airfoils/master/docs/source/_static/images/example.png
    :width: 600 px
    :target: https://github.com/airinnova/airfoils
    :alt: Example

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
