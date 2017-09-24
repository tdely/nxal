# -*- coding: utf-8 -*-

"""
nxal.parser
~~~~~~~~~~~

Parsing module for nxal.

"""

import re
import sys
from .exceptions import UnknownFormatVariable

_pattern_variables = {
    'remote_addr': '(?P<remote_addr>\d+.\d+.\d+.\d+)',
    'remote_user': '(?P<remote_user>(\S)+)',
    'time_local': '(?P<time_local>\d{2}\/[A-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} [+\-]\d{4})',
    'time_iso8601': '(?P<time_iso8601>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+\-]\d{2}:\d{2})',
    'request': '(?P<request>(?P<request_method>\w+)\s(?P<request_uri>\S+)\s(?P<request_protocol>(?P<request_protocol_name>\w+)/(?P<request_protocol_version>\S+)))',
    'status': '(?P<status>\d+)',
    'body_bytes_sent': '(?P<body_bytes_sent>\d+)',
    'bytes_sent': '(?P<bytes_sent>\d+)',
    'http_referer': '(?P<http_referer>.+)',
    'http_user_agent': '(?P<http_user_agent>.+)',
    'request_length': '(?P<request_length>\d+)',
    'request_time': '(?P<request_time>\d+\.\d{3})',
    'msec': '(?P<msec>\d+\.\d{3})',
    'pipe': '(?P<pipe>[p\.])',
    'connection': '(?P<connection>\d+)',
    'upstream_connect_time': '(?P<upstream_connect_time>\d+\.\d{3}|-)',
    'upstream_header_time': '(?P<upstream_header_time>\d+\.\d{3}|-)',
    'upstream_response_time': '(?P<upstream_response_time>\d+\.\d{3}|-)'
}


def compile(format_string):
    """Compile a regular expression pattern from a format string.
    Returns :class:`re.RegexObject <pattern>` object.

    :param format_string: Format of the Nginx access log.
    :rtype: :class:`re.RegexObject` object or None.
    """
    if isinstance(format_string, re._pattern_type):
        return format_string

    pattern = re.escape(format_string)
    pattern = pattern.replace('\_', '_')

    for variable in re.findall('(\$(\w+))', format_string):
        if variable[1] not in _pattern_variables:
            raise UnknownFormatVariable(
                'Unknown variable in format string.',
                variable
            )

    for variable, value in _pattern_variables.iteritems():
        pattern = pattern.replace('\$' + variable, value)

    return re.compile(pattern)


def parse(string, pattern=None):
    """Parse Nginx access log line. Returns dict or None.

    :param string: Nginx access log line.
    :param pattern: Regular expression pattern or format string.
    :type: :class:`re.RegexObject` or string.
    :rtype: dict or None.
    """
    if pattern is None:
        pattern = ('$remote_addr - $remote_user [$time_local] "$request" '
                   '$status $body_bytes_sent "$http_referer" "$http_user_agent"')

    p = compile(pattern)
    result = re.search(p, string)
    if result is not None:
        result = result.groupdict()
    return result


if __name__ == '__main__':
    access_log = sys.argv[1]
    if len(sys.argv) == 3:
        format_string = sys.argv[2]
    else:
        format_string = None

    result = list()

    with open(access_log, 'r') as f:
        for line in f:
            match = parse(line, format_string)
            if match is None:
                print "log pattern did not match log line."
                continue
            result.append(match)

    print result
