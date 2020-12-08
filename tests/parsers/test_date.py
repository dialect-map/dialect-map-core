# -*- coding: utf-8 -*-

from src.dialect_map.parsers import DateParser


def test_date_parser_check():
    """ Checks the correct matching of date strings """

    parser = DateParser()

    s1 = "2020"
    s2 = "2020-11-20"
    s3 = "2020-11-20 14:00:00"

    assert parser.check(s1) is False
    assert parser.check(s2) is True
    assert parser.check(s3) is False


def test_date_parser_parse():
    """ Checks the correct parsing of date strings """

    parser = DateParser()

    date_str = "1990-01-01"
    date_obj = parser.parse(date_str)

    assert date_obj.year == 1990
    assert date_obj.month == 1
    assert date_obj.day == 1
