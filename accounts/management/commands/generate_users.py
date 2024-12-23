import random
from django.core.management.base import BaseCommand
from django.core.files import File
from django.contrib.auth.hashers import make_password
from accounts.models import CustomUser
import os


class Command(BaseCommand):
    help = "Generate random users with roles (agents/workers) and optional profile pictures"

    def handle(self, *args, **kwargs):
        # Define sample data for user creation
        first_names = ["John", "Jane", "Alice", "Bob", "Mary", "Michael", "Sarah", "David"]
        last_names = ["Smith", "Doe", "Johnson", "Brown", "Taylor", "Anderson", "Lee", "Walker"]
        roles = ["agent", "worker"]  # Possible roles

        # Define base directory for profile pictures
        profile_pics_dir = os.path.join(os.getcwd(), "profile_pictures")
        if not os.path.exists(profile_pics_dir):
            self.stdout.write(self.style.WARNING(f"Profile pictures directory not found: {profile_pics_dir}"))
            profile_pics = []
        else:
            profile_pics = [
                os.path.join(profile_pics_dir, pic) 
                for pic in os.listdir(profile_pics_dir) if pic.endswith((".jpg", ".png"))
            ]

        # Create random users
        total_users = 20  # Specify how many users you want to create

        for i in range(total_users):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f"{first_name.lower()}{last_name.lower()}{i}"
            email = f"{username}@example.com"
            password = make_password("password123")  # Default password

            # Randomly choose whether the user is an agent or worker
            is_worker = random.choice([True, False])
            is_agent = not is_worker  # If not worker, they are agent

            # Choose a profile picture or use the default
            profile_picture = None
            if profile_pics and random.choice([True, False]):  # 50% chance to add a profile picture
                pic_path = random.choice(profile_pics)
                with open(pic_path, "rb") as pic_file:
                    profile_picture = File(pic_file, name=os.path.basename(pic_path))

            # Create the user
            user = CustomUser.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                is_worker=is_worker,  # Assign is_worker role
                is_agent=is_agent,  # Assign is_agent role
            )

            # Save the profile picture if available, otherwise use the default
            if profile_picture:
                user.profile_picture.save(profile_picture.name, profile_picture)
            else:
                user.profile_picture = 'profile_pictures/default.jpg'
            user.save()

            self.stdout.write(self.style.SUCCESS(f"Created user: {username} (Agent: {is_agent}, Worker: {is_worker})"))

        self.stdout.write(self.style.SUCCESS(f"Successfully created {total_users} random users!"))
