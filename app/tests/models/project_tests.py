from django.test import TestCase
from datetime import date
from app.models import Project, City


class ProjectModelTests(TestCase):
    def setUp(self):
        # Create low and high cost cities
        self.city_low = City.objects.create(name="Crozet", state="VA", cost_type="low")
        self.city_high = City.objects.create(
            name="Arlington", state="VA", cost_type="high"
        )

        # Set 1: One project in low-cost city
        self.project_set1 = [
            Project.objects.create(
                name="Project 1",
                start_date=date(2015, 9, 1),
                end_date=date(2015, 9, 3),
                city=self.city_low,
                set=1,
            )
        ]

        # Set 2: Multiple projects in low-cost and high-cost cities with overlaps
        self.project_set2 = [
            Project.objects.create(
                name="Project 1",
                start_date=date(2015, 9, 1),
                end_date=date(2015, 9, 1),
                city=self.city_low,
                set=2,
            ),
            Project.objects.create(
                name="Project 2",
                start_date=date(2015, 9, 2),
                end_date=date(2015, 9, 6),
                city=self.city_high,
                set=2,
            ),
            Project.objects.create(
                name="Project 3",
                start_date=date(2015, 9, 6),
                end_date=date(2015, 9, 8),
                city=self.city_low,
                set=2,
            ),
        ]

        # Set 3: Multiple projects with gaps between them
        self.project_set3 = [
            Project.objects.create(
                name="Project 1",
                start_date=date(2015, 9, 1),
                end_date=date(2015, 9, 3),
                city=self.city_low,
                set=3,
            ),
            Project.objects.create(
                name="Project 2",
                start_date=date(2015, 9, 5),
                end_date=date(2015, 9, 7),
                city=self.city_high,
                set=3,
            ),
            Project.objects.create(
                name="Project 3",
                start_date=date(2015, 9, 8),
                end_date=date(2015, 9, 8),
                city=self.city_high,
                set=3,
            ),
        ]

        # Set 4: Multiple projects on the same dates
        self.project_set4 = [
            Project.objects.create(
                name="Project 1",
                start_date=date(2015, 9, 1),
                end_date=date(2015, 9, 1),
                city=self.city_low,
                set=4,
            ),
            Project.objects.create(
                name="Project 2",
                start_date=date(2015, 9, 1),
                end_date=date(2015, 9, 1),
                city=self.city_low,
                set=4,
            ),
            Project.objects.create(
                name="Project 3",
                start_date=date(2015, 9, 2),
                end_date=date(2015, 9, 2),
                city=self.city_high,
                set=4,
            ),
            Project.objects.create(
                name="Project 4",
                start_date=date(2015, 9, 2),
                end_date=date(2015, 9, 3),
                city=self.city_high,
                set=4,
            ),
        ]

    def test_reimbursement_set1(self):
        total_reimbursement = Project.calculate_reimbursement_for_project_set(1)
        expected_reimbursement = 45 + 75 + 45  # 165
        self.assertEqual(total_reimbursement, expected_reimbursement)

    def test_reimbursement_set2(self):
        total_reimbursement = Project.calculate_reimbursement_for_project_set(2)
        expected_reimbursement = (75) + (85 + 85 + 85 + 85 + 85) + (75 + 45)  # 620
        self.assertEqual(total_reimbursement, expected_reimbursement)

    def test_reimbursement_set3(self):
        total_reimbursement = Project.calculate_reimbursement_for_project_set(3)
        expected_reimbursement = 45 + 75 + 45 + 55 + 85 + 85 + 85  # 475
        self.assertEqual(total_reimbursement, expected_reimbursement)

    def test_reimbursement_set4(self):
        total_reimbursement = Project.calculate_reimbursement_for_project_set(4)
        expected_reimbursement = 75 + 85 + 55  # 215
        self.assertEqual(total_reimbursement, expected_reimbursement)
