import os
import random
from django.core.management.base import BaseCommand
from django.core.files import File
from listings.models import Listing, SubImage
from accounts.models import CustomUser
from Location.models import LGA
from services.models import Agent

class Command(BaseCommand):
    help = "Generate listings and sub-images from the Houses Dataset"

    def handle(self, *args, **kwargs):
        base_dir = os.path.join(os.getcwd(), "Houses-dataset", "Houses Dataset")
        if not os.path.exists(base_dir):
            self.stdout.write(self.style.ERROR("Dataset directory not found."))
            return

        # Get all folders in the base directory
        house_folders = [
            folder for folder in os.listdir(base_dir)
            if os.path.isdir(os.path.join(base_dir, folder)) and folder.isdigit()
        ]
        if not house_folders:
            self.stdout.write(self.style.ERROR("No house folders found in the dataset directory."))
            return

        agents = Agent.objects.all()
        locations = LGA.objects.all()

        if not agents.exists():
            self.stdout.write(self.style.ERROR("No agents found in the database."))
            return

        if not locations.exists():
            self.stdout.write(self.style.ERROR("No locations (LGAs) found in the database."))
            return

        for folder in house_folders:
            folder_path = os.path.join(base_dir, folder)
            main_image_name = f"{folder}_frontal.jpg"
            main_image_path = os.path.join(folder_path, main_image_name)

            if not os.path.exists(main_image_path):
                self.stdout.write(self.style.WARNING(f"Main image not found for house {folder}. Skipping."))
                continue

            # Select a random agent and location
            agent = random.choice(agents)
            location = random.choice(locations)

            # Open the main image file and save it using Django's file system
            with open(main_image_path, "rb") as img_file:
                listing = Listing.objects.create(
                    title=f"House {folder}",
                    price=random.randint(50000, 500000),
                    num_bedrooms=random.randint(1, 5),
                    num_bathrooms=random.randint(1, 3),
                    square_footage=random.randint(100, 500),
                    address=f"Address {folder}",
                    main_image=File(img_file, name=main_image_name),  # Save image to MEDIA_ROOT
                    agent=agent,
                    location=location,
                )

            self.stdout.write(self.style.SUCCESS(f"Created listing: {listing.title}"))

            # Add sub-images
            for file in os.listdir(folder_path):
                if file != main_image_name and file.endswith(".jpg"):
                    sub_image_path = os.path.join(folder_path, file)
                    with open(sub_image_path, "rb") as sub_img_file:
                        SubImage.objects.create(
                            listing=listing,
                            image=File(sub_img_file, name=file),  # Save sub-image to MEDIA_ROOT
                            location=location,
                        )
                    self.stdout.write(self.style.SUCCESS(f"Added sub-image for {listing.title}: {file}"))

        self.stdout.write(self.style.SUCCESS("Listings and sub-images generated successfully."))
