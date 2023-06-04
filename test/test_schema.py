from financial.schemas.RequestSchemas import *
from datetime import date

import unittest


class RequestSchemaDateTestcase(unittest.TestCase):

    def test_date_format_validation_success(self):
        result = date_format_validation("2018-05-01", "some_date" )
        assert result == date(2018, 5, 1)

    def test_date_format_validation_fail(self):
        self.assertRaises(RequestValidationError, date_format_validation, "2018", "some_date")

    def test_cross_validate_dates_success(self):
        cross_validate_dates("2018-05-01", "2018-05-20")


    def test_cross_validate_dates_bad_input_param1(self):
        self.assertRaises(RequestValidationError, cross_validate_dates, "2018-06-1", "2018-05-01")

    def test_cross_validate_dates_bad_input_param2(self):
        self.assertRaises(RequestValidationError, cross_validate_dates, "2018-06-01", "2018")

    def test_cross_validate_dates_fail(self):
        self.assertRaises(RequestValidationError, cross_validate_dates, "2018-06-01", "2018-05-01")
