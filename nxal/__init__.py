# -*- coding: utf-8 -*-

"""
nxal is an Nginx access log parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

nxal parses nginx access logs:

   >>> import nxal
   >>>  with open('/var/log/nginx/access.log', 'r') as log_file:
   >>>      for line in log_file:
   >>>          match = parse(line)
   >>>          if match is None:
   >>>              print "log pattern did not match log line."
   >>>              continue
   >>>          result.append(match)
   >>>  print result

:copyright: (c) 2017 by Tobias Dély.
:license: MIT, see LICENSE for more details.

"""

__title__ = 'nxal'
__version__ = '0.1.0'
__author__ = 'Tobias Dély'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 Tobias Dély'

from .parser import compile, parse
