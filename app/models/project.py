from datetime import timedelta
from django.db import models

from .city import City


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
    calculated_rate = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Set the project index based on the set
        if not self.idx:
            self.idx = Project.objects.filter(set=self.set).count() + 1
        super().save(*args, **kwargs)

    def get_project_id(self):
        return f"{self.set}-{self.idx}"

    def get_rate(self, day_type):
        """
        Determines the rate based on the city cost type and day type (travel or full).
        """
        return self.get_day_rate(day_type, self.city.cost_type)

    @staticmethod
    def get_day_rate(day_type, city_type):
        """
        Determines the rate based on the city cost type and day type (travel or full).
        """
        rates = {"high": {"travel": 55, "full": 85}, "low": {"travel": 45, "full": 75}}

        return rates[city_type][day_type]

    @staticmethod
    def collect_project_dates(projects):
        date_to_city = {}

        # Iterate over all projects and collect unique dates
        for project in projects:
            current_date = project.start_date
            while current_date <= project.end_date:
                if current_date not in date_to_city:
                    date_to_city[current_date] = {"low": 0, "high": 0}
                city_type = "high" if project.city.cost_type == "high" else "low"
                date_to_city[current_date][city_type] += 1
                current_date += timedelta(days=1)

        return date_to_city

    @staticmethod
    def classify_days(projects, date_to_city):
        """
        Classify days across multiple projects in a set.
        - Handle overlaps and gaps correctly, upgrading travel days to full days where appropriate.
        - Ensure that any day is only counted once, even if it belongs to multiple projects.
        """
        day_types = {}
        sorted_projects = sorted(projects, key=lambda p: p.start_date)

        for i, project in enumerate(sorted_projects):
            first_day = project.start_date
            last_day = project.end_date
            current_date = first_day

            while current_date <= last_day:
                city_type = "high" if project.city.cost_type == "high" else "low"

                # If the day hasn't been assigned yet, classify it
                if current_date not in day_types:
                    # First and last day are travel days unless upgraded to full due to overlap or push
                    if current_date == first_day or current_date == last_day:
                        day_types[current_date] = {
                            "type": "travel",
                            "city_type": city_type,
                        }
                    else:
                        day_types[current_date] = {
                            "type": "full",
                            "city_type": city_type,
                        }
                else:
                    # If the day is already marked as travel, upgrade it to full for overlaps or adjacent projects
                    if (
                        day_types[current_date]["type"] == "travel"
                        and current_date != last_day
                    ):
                        day_types[current_date]["type"] = "full"

                    # Use the higher city cost type (high) if there's a conflict
                    if (
                        day_types[current_date]["city_type"] == "low"
                        and city_type == "high"
                    ):
                        day_types[current_date]["city_type"] = "high"

                current_date += timedelta(days=1)

            # Handle the case where two projects push up against each other
            if i < len(sorted_projects) - 1:
                next_project = sorted_projects[i + 1]
                next_first_day = next_project.start_date

                # If projects touch, mark the last day as full
                if last_day + timedelta(days=1) == next_first_day:
                    day_types[first_day] = {
                        "type": "full",
                        "city_type": city_type,
                    }  # Project pushes against the next one
                    day_types[next_first_day] = {
                        "type": "full",
                        "city_type": next_project.city.cost_type,
                    }
                else:
                    # Ensure the last day of the project is classified correctly as travel if not touching the next project
                    if (
                        last_day not in day_types
                        or day_types[last_day]["type"] != "full"
                    ):
                        day_types[last_day] = {"type": "travel", "city_type": city_type}

        return day_types

    @staticmethod
    def calculate_total_reimbursement(day_types):
        """
        Calculate the total reimbursement based on the classified days.
        """
        rates = {"travel": {"low": 45, "high": 55}, "full": {"low": 75, "high": 85}}

        total_reimbursement = 0

        # Calculate the total reimbursement
        for day, info in day_types.items():
            day_type = info["type"]
            city_type = info["city_type"]
            rate = rates[day_type][city_type]
            print(f"Day: {day}, Type: {day_type}, City: {city_type}, Rate: {rate}")
            total_reimbursement += rate

        print(f"Total Reimbursement: {total_reimbursement}")
        return total_reimbursement

    @classmethod
    def calculate_reimbursement_for_project_set(cls, project_set):
        """
        Calculate the reimbursement for all projects in a given project set.
        Each project will also have its own individual reimbursement calculated and saved.
        """
        # Fetch all projects in the set
        projects = cls.objects.filter(set=project_set).select_related("city")

        # Step 1: Collect all unique dates and associated city types
        date_to_city = cls.collect_project_dates(projects)

        # Step 2: Classify each day across all projects (based on the entire set)
        day_types = cls.classify_days(projects, date_to_city)

        # Step 3: Calculate the total reimbursement for all projects in the set
        total_reimbursement = cls.calculate_total_reimbursement(day_types)

        # Step 4: Track already reimbursed days to avoid double counting
        reimbursed_days = set()

        # Step 5: Calculate and save the rate for each project individually
        for project in projects:
            project_reimbursement = 0

            # For each project, sum up the reimbursement for the days that belong to this project
            for day, info in day_types.items():
                if (
                    project.start_date <= day <= project.end_date
                    and day not in reimbursed_days
                ):
                    # Add the rate for each day that belongs to this project and hasn't been reimbursed yet
                    rate = cls.get_day_rate(info["type"], info["city_type"])
                    project_reimbursement += rate

                    # Mark the day as reimbursed to prevent double counting
                    reimbursed_days.add(day)

            # Save the calculated reimbursement for the project
            project.calculated_rate = project_reimbursement
            project.save()

        return total_reimbursement
