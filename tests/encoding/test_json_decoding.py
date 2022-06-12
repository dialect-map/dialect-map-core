# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime

from src.dialect_map_core.encoding import CustomJSONDecoder


def test_json_decoding():
    """Checks the correct decoding of strings"""

    decoder = CustomJSONDecoder()

    s1 = "2020"
    s2 = "2020-11-20"
    s3 = "2020-11-20 14:00:00"

    assert type(decoder.custom_decode(s1)) == str
    assert type(decoder.custom_decode(s2)) == date
    assert type(decoder.custom_decode(s3)) == datetime


def test_json_decoding_dates():
    """Checks the correct decoding of date strings"""

    decoder = CustomJSONDecoder()

    date_str = "1990-01-01"
    date_obj = decoder.custom_decode(date_str)

    assert date_obj.year == 1990
    assert date_obj.month == 1
    assert date_obj.day == 1
