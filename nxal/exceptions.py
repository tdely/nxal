# -*- coding: utf-8 -*-

"""
nxal.exceptions
~~~~~~~~~~~~~~~

Exceptions module for nxal.

"""

class UnknownFormatVariable(Exception):
    """An unknown format variable was encountered."""
    def __init__(self, message, errors):
        super(UnknownFormatVariable, self).__init__(message, errors)
