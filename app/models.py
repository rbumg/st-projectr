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


class Project(models.Model):
    """
    A project that a user can work on.

    Note: Set is the number of the project. For example, the first project is set 1.
    """

    set = models.IntegerField(default=1)
    idx = models.IntegerField(default=1)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Set the project index based on the set
        if not self.idx:
            self.idx = Project.objects.filter(set=self.set).count() + 1
        super().save(*args, **kwargs)

    def get_project_id(self):
        return f"{self.set}-{self.idx}"
