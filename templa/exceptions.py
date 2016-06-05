# -*- coding: utf-8 -*-


class BaseError(Exception):
    """
    Baseclass for all tempra errors.
    """
    pass


class TerminateLoop(BaseError):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class TempraError(BaseError):
    """
    """


class ParseError(BaseError):
    """
    """


class ConfigLoadError(BaseError):
    """
    """
