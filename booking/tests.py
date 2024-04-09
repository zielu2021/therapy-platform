from django.test import TestCase
from datetime import datetime
from .views import validWeekday, dayToWeekday, isWeekdayValid
from .models import Appointment


class TestValidWeekday(TestCase):
    def test_validWeekday_no_sundays(self):
        test_days = 10
        result = validWeekday(test_days)
        for day in result:
            # Convert the date string back to datetime object
            date_obj = datetime.strptime(day, "%Y-%m-%d")
            # Check if the day is Sunday
            self.assertNotEqual(date_obj.strftime("%A"), "Sunday")


class TestDayToWeekday(TestCase):
    def test_dayToWeekday(self):
        date_string = "2024-03-14"
        result = dayToWeekday(date_string)
        expected_result = "Thursday"
        self.assertEqual(result, expected_result)


class TestIsWeekdayValid(TestCase):
    def setUp(self):
        Appointment.objects.create(day=datetime.strptime("2024-03-14", "%Y-%m-%d"))
        Appointment.objects.create(day=datetime.strptime("2024-03-15", "%Y-%m-%d"))
        Appointment.objects.create(day=datetime.strptime("2024-03-16", "%Y-%m-%d"))

    def test_isWeekdayValid(self):
        valid_weekdays = [
            datetime.strptime("2024-03-14", "%Y-%m-%d"),
            datetime.strptime("2024-03-15", "%Y-%m-%d"),
            datetime.strptime("2024-03-16", "%Y-%m-%d"),
        ]
        # Call the function with the list of valid weekdays
        result = isWeekdayValid(valid_weekdays)
        # Expected result should be all weekdays since there are no fully booked days
        expected_result = valid_weekdays
        self.assertEqual(result, expected_result)
