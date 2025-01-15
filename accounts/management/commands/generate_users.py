import random
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import make_password
from accounts.models import CustomUser
from services.models import Worker, Agent
import os

class Command(BaseCommand):
    help = "Generate random users with roles (agents/workers) and optional profile pictures"

    def handle(self, *args, **kwargs):
        # Define sample data for user creation
        first_names = ["John", "Jane", "Alice", "Bob", "Mary", "Michael", "Sarah", "David"]
        last_names = ["Smith", "Doe", "Johnson", "Brown", "Taylor", "Anderson", "Lee", "Walker"]
        roles = ["agent", "worker", "neither"]  # Possible roles

        # Define base directory for profile pictures
        profile_pics_dir = os.path.join(os.getcwd(),"media","profile_pictures")
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

            # Ensure unique username
            while CustomUser.objects.filter(username=username).exists():
                username = f"{first_name.lower()}{last_name.lower()}{random.randint(1000, 9999)}"
                self.stdout.write(self.style.WARNING(f"Username {username} already exists, generating a new one."))

            # Randomly assign roles: Ensure even distribution
            role_choice = random.choices(
                roles, 
                weights=[1, 1, 1],  # Equal probability for 'worker', 'agent', and 'neither'
                k=1
            )[0]

            is_worker = False
            is_agent = False

            if role_choice == "worker":
                is_worker = True
            elif role_choice == "agent":
                is_agent = True

            # Choose a profile picture or use the default
            profile_picture = None
            if profile_pics and random.choice([True, False]):  # 50% chance to add a profile picture
                pic_path = random.choice(profile_pics)
                with open(pic_path, "rb") as pic_file:
                    pic_data = pic_file.read()  # Read the file content
                    profile_picture = ContentFile(pic_data, name=os.path.basename(pic_path))

            try:
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

                # Now, create Worker or Agent profile if the user has the corresponding role
                if is_worker:
                    Worker.objects.create(
                        user=user,
                        NIN=f"NIN{random.randint(100000, 999999)}",
                        services_offered="Cleaning, Plumbing",
                        hourly_rate=random.uniform(10, 30),
                        availability=random.choice([True, False]),
                        rating=random.uniform(1, 5),
                        status=random.choice(['verified', 'pending', 'suspended']),
                    )
                if is_agent:
                    Agent.objects.create(
                        user=user,
                        NIN=f"NIN{random.randint(100000, 999999)}",
                        avg_price=random.uniform(50, 150),
                        availability=random.choice([True, False]),
                        rating=random.uniform(1, 5),
                        status=random.choice(['verified', 'pending', 'suspended']),
                    )

                self.stdout.write(self.style.SUCCESS(f"Created user: {username} (Agent: {is_agent}, Worker: {is_worker})"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating user {username}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully created {total_users} random users!"))
