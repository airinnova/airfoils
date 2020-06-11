Changelog
=========

Changelog for PyTornado. Version numbers try to follow `Semantic
Versioning <https://semver.org/spec/v2.0.0.html>`__.

[0.2.2] -- 2020-06-11
---------------------

Added
~~~~~

* Dismiss duplicate entries coodinate vectors. This avoids the following error
  which my be thrown by ``scipy.interpolate.interp1d()``:

  ``ValueError: Expect x to be a 1-D sorted array_like.``

[0.2.1] -- 2020-01-05
---------------------

Fixed
~~~~~

* Fixed deprecation warning for `re` library

[0.2.0] -- 2019-09-16
---------------------

Changed
~~~~~~~

* Create interpolator objects for `y_upper` and `y_lower` in `Airfoil.__init__()`
    * Generally more efficient since `y_upper` and `y_lower` are queried a lot
* Renamed variable `xsi` in module 'airfoils' to `x`

Removed
~~~~~~~

* Removed `Airfoil.interpolate_y()` (replaced by methods `y_upper()` and `y_lower()`)

[0.1.1] -- 2019-09-15
---------------------

Changed
~~~~~~~

* Modified arguments of `Airfoil.plot()` function

Added
~~~~~

* Added `save` flag to `Airfoil.plot()` function

Fixed
~~~~~

* Typo in variable name

[0.1.0] -- 2019-09-04
---------------------

* Minor changes

[0.0.1] -- 2019-08-27
---------------------

* First public release
