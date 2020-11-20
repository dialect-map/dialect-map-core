# -*- coding: utf-8 -*-

from parsers import DatetimeParser


def test_date_parser_check():
    """ Checks the correct matching of datetime strings """

    parser = DatetimeParser()

    s1 = "2020"
    s2 = "2020-11-20"
    s3 = "2020-11-20 14:00:00"

    assert parser.check(s1) is False
    assert parser.check(s2) is False
    assert parser.check(s3) is True


def test_date_parser_parse():
    """ Checks the correct parsing of datetime strings """

    parser = DatetimeParser()

    date_str = "1990-01-01 22:00:00"
    date_obj = parser.parse(date_str)

    assert date_obj.year == 1990
    assert date_obj.month == 1
    assert date_obj.hour == 22
    assert date_obj.minute == 0
    assert date_obj.second == 0
