#
# Copyright 2008,2009 Free Software Foundation, Inc.
#
# SPDX-License-Identifier: MIT
#

# The presence of this file turns this directory into a Python package

'''
This is the GNU Radio PROWESS module. Place your Python package
description here (python/__init__.py).
'''
import os

# import pybind11 generated symbols into the prowess namespace
try:
    # this might fail if the module is python-only
    from .prowess_python import *
except ModuleNotFoundError:
    pass

# import any pure python here
from .signal_generator import signal_generator

#
