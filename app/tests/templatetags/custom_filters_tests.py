from django.test import TestCase
from app.models import Project, City
from app.templatetags.custom_filters import (
    get_rate,
    get_calculated_rate,
    get_project_set_total,
)


class CustomFiltersTest(TestCase):
    def setUp(self):
        self.city_low = City.objects.create(name="Crozet", cost_type="low")
        self.city_high = City.objects.create(name="Arlington", cost_type="high")
        self.project1 = Project.objects.create(
            name="Project 1",
            start_date="2024-10-01",
            end_date="2024-10-03",
            city=self.city_low,
        )
        self.project2 = Project.objects.create(
            name="Project 2",
            start_date="2024-10-01",
            end_date="2024-10-03",
            city=self.city_high,
        )

    def test_get_rate(self):
        # Test with a low cost city
        self.assertEqual(get_rate(self.project1, "travel"), "$45.00")
        self.assertEqual(get_rate(self.project1, "full"), "$75.00")

        # Test with a high cost city
        self.assertEqual(get_rate(self.project2, "travel"), "$55.00")
        self.assertEqual(get_rate(self.project2, "full"), "$85.00")

    def test_get_calculated_rate(self):
        self.project1.calculated_rate = 100.00
        self.project1.save()
        self.assertEqual(get_calculated_rate(self.project1), "$100.00")

        self.project2.calculated_rate = 200.00
        self.project2.save()
        self.assertEqual(get_calculated_rate(self.project2), "$200.00")

    def test_get_total_cost(self):
        # get_project_set_total
        self.project1.calculated_rate = 100.00
        self.project1.save()

        self.project2.calculated_rate = 200.00
        self.project2.save()

        self.assertEqual(
            get_project_set_total(self.project1, self.project1.set), "$300.00"
        )
