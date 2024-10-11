from datetime import timedelta
from django.db import models


class City(models.Model):
    """
    A city where a project is located.
    """

    HIGH_COST = "high"
    LOW_COST = "low"
    COST_CHOICES = [
        (HIGH_COST, "High Cost"),
        (LOW_COST, "Low Cost"),
    ]

    name = models.CharField(max_length=100)  # City name
    state = models.CharField(max_length=2)  # State abbreviation
    cost_type = models.CharField(
        max_length=4, choices=COST_CHOICES, default=LOW_COST
    )  # Cost type (high or low)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "cities"
        unique_together = ['name', 'state']