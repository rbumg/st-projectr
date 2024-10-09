from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import City
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = "Seed the database with a demo admin"

    def handle(self, *args, **options):
        # Create a demo admin user
        self.create_user(
            username="admin",
            first_name="Admin",
            last_name="User",
            email="demo+admin@example.com",
            password="admin",
            type="admin",
        )

        # Create a demo regular user
        self.create_user(
            username="user",
            first_name="Regular",
            last_name="User",
            email="demo+user@example.com",
            password="user",
            type="user",
        )

        # Create a low cost city
        self.create_city(name="Arlington", state="VA", cost_type="high")

        # Create a high cost city
        self.create_city(name="Crozet", state="VA", cost_type="low")

    def create_user(self, username, first_name, last_name, email, password, type):
        try:
            if type == "admin":
                user = User.objects.create_superuser(
                    username=username, email=email, password=password
                )
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )

            user.first_name = first_name
            user.last_name = last_name
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"User {user.first_name} {user.last_name} created successfully!"
                )
            )

        except IntegrityError:
            self.stdout.write(self.style.WARNING("User already exists."))

    def create_city(self, name, state, cost_type):
        city = City.objects.create(name=name, state=state, cost_type=cost_type)
        self.stdout.write(self.style.SUCCESS(f"City {city.name} created successfully!"))
