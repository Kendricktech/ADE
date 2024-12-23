import json
import requests
from django.core.management.base import BaseCommand
from Location.models import Country, State, LGA  # Import models from Location app

class Command(BaseCommand):
    help = "Load states and LGAs from a JSON URL"

    def handle(self, *args, **kwargs):
        # URL containing the JSON data
        url = "https://gist.githubusercontent.com/mykeels/1174cd68bcff6efc4f8cafb49a24a209/raw/388eea7fd85e2d615d92e473120355a0a37ab80b/states-and-cities.json"

        # Fetch the JSON data from the URL
        self.stdout.write("Fetching data from the URL...")
        response = requests.get(url)
        if response.status_code != 200:
            self.stderr.write("Failed to fetch data. Status code: {}".format(response.status_code))
            return

        data = response.json()

        # Create a Country (Nigeria) if it doesn't already exist
        country, created = Country.objects.get_or_create(
            name="Nigeria",
            defaults={
                "country_code": "NGA",
                "latitude": "9.0820",
                "longitude": "8.6753",
                "abbv": "NG",
            }
        )

        # Loop through states and LGAs
        for state_data in data:
            state_name = state_data["name"]
            cities = state_data["cities"]

            # Create or get the state
            state, created = State.objects.get_or_create(
                country=country,
                name=state_name
            )

            # Create LGAs for the state
            for lga_name in cities:
                LGA.objects.get_or_create(state=state, name=lga_name)

        self.stdout.write(self.style.SUCCESS("States and LGAs loaded successfully from the URL."))

