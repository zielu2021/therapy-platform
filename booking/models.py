from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

SERVICE_CHOICES = (
    ("50 mins Online Therapy- Individual", "50 mins Online Therapy Individual"),
    ("50 mins Online Therapy- Couples", "50 mins Online Therapy- Couples"),
)
TIME_CHOICES = (
    ("8 AM", "8 AM"),
    ("9 AM", "9 AM"),
    ("10 AM", "10 AM"),
    ("11 AM", "11 AM"),
    ("12 PM", "12 PM"),
    ("1 PM", "1 PM"),
    ("2 PM", "2 PM"),
    ("3 PM", "3 PM"),
    ("4 PM", "4 PM"),
    ("5 PM", "5 PM"),
    ("6 PM", "6 PM"),
    ("7 PM", "7 PM"),
    ("8 PM", "8 PM"),
)


class Appointment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    service = models.CharField(
        max_length=50,
        choices=SERVICE_CHOICES,
        default="50 mins Online Therapy- Individual",
    )
    day = models.DateField(default=timezone.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="8 AM")
    time_ordered = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.user} | day: {self.day} | time: {self.time}"
