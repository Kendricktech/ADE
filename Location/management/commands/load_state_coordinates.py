import json
import requests
import re
from django.core.management.base import BaseCommand
from Location.models import State


def normalize_name(name):
    """
    Normalize a state name by converting it to lowercase, 
    removing spaces, hyphens, and other non-alphanumeric characters.
    """
    return re.sub(r"[\s\-]+", "", name.strip().lower())


class Command(BaseCommand):
    help = "Update state latitude and longitude from a JSON URL"

    def handle(self, *args, **kwargs):
        # JSON URL
        url = "https://raw.githubusercontent.com/iamspruce/intro-d3/refs/heads/main/data/nigeria-states.json"

        self.stdout.write("Fetching data from the URL...")
        response = requests.get(url)
        if response.status_code != 200:
            self.stderr.write(f"Failed to fetch data. Status code: {response.status_code}")
            return

        data = response.json().get("data", [])
        if not data:
            self.stderr.write("No data found in the JSON file.")
            return

        # Create a normalized mapping of state names in the database
        db_states = {normalize_name(state.name): state for state in State.objects.all()}

        updated_count = 0
        for state_data in data:
            json_name = normalize_name(state_data.get("Name", ""))
            info = state_data.get("info", {})
            latitude = info.get("Latitude")
            longitude = info.get("Longitude")

            # Match the normalized name with database entries
            state = db_states.get(json_name)
            if state:
                state.latitude = latitude
                state.longitude = longitude
                state.save()
                updated_count += 1
                self.stdout.write(f"Updated {state.name}: Lat={latitude}, Lon={longitude}")
            else:
                self.stderr.write(f"State {state_data.get('Name')} does not exist in the database.")

        self.stdout.write(self.style.SUCCESS(f"Successfully updated {updated_count} states."))
