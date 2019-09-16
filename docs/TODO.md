# TODO

## Improvements
* Implement more accurate camber line computation ("Jesper method")

## Testing
* Thorough testing of NACA4 airfoil generator

## New features
* Implement generator for for NACA 6-digit series (etc.) and user input
* Add `Airfoil.chord_line(x)`
* Add `Airfoil.export(filename, n_point)` --> Serialise an aifoil object (write text file)
* Add `Airfoil.thickness(x)`
* Add `@property` for `Airfoil.max_thickness` (measured perpendicular to chord or camber line?)

## Documentation
* Add doc for airfoil import from files

## Airfoil class
* Shift data if `x_lower`/`x_upper` don't start at 0?
