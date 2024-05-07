# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime

from src.dialect_map_core.encoding import CustomJSONEncoder


def test_python_encoding():
    """Checks the correct encoding of Python objects"""

    encoder = CustomJSONEncoder()

    o1 = datetime.today().date()
    o2 = "example"
    o3 = 100

    assert type(encoder.custom_encode(o1)) is str
    assert type(encoder.custom_encode(o2)) is str
    assert type(encoder.custom_encode(o3)) is str


def test_python_encoding_dates():
    """Checks the correct encoding of date objects"""

    encoder = CustomJSONEncoder()

    date_obj = date(1990, 1, 1)
    date_str = encoder.custom_encode(date_obj)

    assert date_str == "1990-01-01"
