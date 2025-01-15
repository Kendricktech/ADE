from django.db import models
from accounts.models import CustomUser
from Location.models import LGA
from services.models import Agent
from django.utils import timezone
from django.conf import settings

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
        Agent,
        on_delete=models.CASCADE,
        related_name='listings',
        limit_choices_to={'is_agent': True}
    )
    location = models.ForeignKey('Location.LGA', null=True, on_delete=models.SET_NULL)
    available = models.BooleanField(default=True)  # Fixed typo to 'available'
    taker = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_taken = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def take(self, taker):
        """Marks a listing as taken and assigns the taker."""
        self.taker = taker
        self.available = False
        self.date_taken = timezone.now()  # Set the date_taken when the listing is taken
        self.save()

    def make_available(self):
        """Marks the listing as available again."""
        self.available = True
        self.taker = None
        self.date_taken = None
        self.save()

    class Meta:
        verbose_name = "Listing"
        verbose_name_plural = "Listings"
        ordering = ['-created_at']  # Order listings by creation date, most recent first


class SubImage(models.Model):
    listing = models.ForeignKey(Listing, related_name='sub_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=listing_sub_image_upload_path)  # Use custom path function
    location = models.ForeignKey(LGA, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.listing.title} - Sub Image"

    class Meta:
        verbose_name = "Sub Image"
        verbose_name_plural = "Sub Images"
        ordering = ['-created_at']  # Order sub-images by creation date, most recent first
