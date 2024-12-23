from django.db import models
from accounts.models import CustomUser
from Location.models import LGA  # Ensure the LGA model is imported
from django.utils import timezone

# Path functions for image uploads
def listing_main_image_upload_path(instance, filename):
    # Custom path for the main image
    return f'static/uploads/listings/{instance.id}/main/{filename}'

def listing_sub_image_upload_path(instance, filename):
    # Custom path for the sub images
    return f'static/uploads/listings/{instance.listing.id}/sub/{filename}'

class Listing(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    num_bedrooms = models.IntegerField()
    num_bathrooms = models.IntegerField()
    square_footage = models.IntegerField()
    address = models.CharField(max_length=100)
    main_image = models.ImageField(upload_to=listing_main_image_upload_path)  # Use custom path function
    agent = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='listings',
        limit_choices_to={'is_agent': True}
    )
    location = models.ForeignKey('Location.LGA', null=True, on_delete=models.SET_NULL)  # Fixed null=True with comma

    # Adding created_at field to track the creation timestamp
    created_at = models.DateTimeField(auto_now_add=True)  # Only auto_now_add is needed
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SubImage(models.Model):
    listing = models.ForeignKey(Listing, related_name='sub_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=listing_sub_image_upload_path)  # Use custom path function
    location = models.ForeignKey(LGA, on_delete=models.CASCADE, null=False)

    created_at = models.DateTimeField(auto_now_add=True)  # Only auto_now_add is needed
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.listing.title} - Sub Image"
