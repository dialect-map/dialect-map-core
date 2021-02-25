# -*- coding: utf-8 -*-

import uuid


def generate_id() -> str:
    """
    Generates a random universal unique identifier (UUID)
    :return: UUID string
    """

    return str(uuid.uuid4()).replace("-", "")


def mutable_property(func):
    """
    Property decorator for ABC mutable attributes
    Its implementation is due to an existing MyPy limitation.
    Reference: https://github.com/python/mypy/issues/9160
    """

    def custom_set_attr(self, value):
        name = func.__name__
        super(self.__class__, self).__setattr__(name, value)

    return property(fget=func, fset=custom_set_attr)
