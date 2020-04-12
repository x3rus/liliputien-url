#!/usr/bin/python3
#
######################################


class liliputienError(Exception):
    """Base class for other exceptions"""
    pass


class urlDontMatchCriteria(liliputienError):
    """Raised when url don't pass url validator"""
    pass


class urlIdNotFound(liliputienError):
    """Raised when url id is not found"""
    pass