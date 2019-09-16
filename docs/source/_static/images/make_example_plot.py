#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from airfoils import Airfoil

HERE = os.path.abspath(os.path.dirname(__file__))


def make_example():
    print('Create example plot... ', end='')
    settings = {
        'file_name': 'example.png',
        'path': HERE,
    }

    Airfoil.NACA4('4812', n_points=300).plot(show=False, save=True, settings=settings)
    print('Done!')


if __name__ == '__main__':
    make_example()
