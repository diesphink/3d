"""
(c) 2020 diesphink
This code is licensed under MIT license (see LICENSE for details)
"""


class Dimensions(object):
    def __getattr__(self, attr):
        setattr(self, attr, Dimensions())
        return getattr(self, attr)
