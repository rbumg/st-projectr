from django.contrib.admin.sites import site
from django.test import TestCase
from app.models import City, Project
from app.admin import CityAdmin, ProjectAdmin


class AdminSiteTest(TestCase):
    def setUp(self):
        # Create sample data for testing
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

    def test_project_admin_get_low_cost_city(self):
        admin_class = ProjectAdmin(Project, site)
        self.assertEqual(admin_class.get_city(self.project1), "Crozet (Low Cost)")

    def test_project_admin_get_high_cost_city(self):
        admin_class = ProjectAdmin(Project, site)
        self.assertEqual(admin_class.get_city(self.project2), "Arlington (High Cost)")
