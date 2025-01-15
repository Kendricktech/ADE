from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Worker(models.Model):
    STATUS_CHOICES = [
        ('verified', 'Verified'),
        ('pending', 'Pending Verification'),
        ('suspended', 'Suspended'),
    ]

    active = models.BooleanField(default=False)
    NIN = models.CharField(
        max_length=20, 
        unique=True, 
        null=False, 
        blank=False,
        help_text="National Insurance Number"
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="worker_profile"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    services_offered = models.TextField(
        help_text="List of services offered by the worker (e.g., cleaning, plumbing)."
    )
    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Hourly rate charged by the worker."
    )
    availability = models.BooleanField(
        default=True,
        help_text="Whether the worker is currently available for jobs."
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Average rating based on customer reviews."
    )
    profile_picture = models.ImageField(
        upload_to="worker_profiles/",
        null=True,
        blank=True,
        help_text="Profile picture of the worker."
    )
    bio = models.TextField(
        blank=True,
        help_text="Worker's professional biography and experience."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['status', 'active']),
            models.Index(fields=['rating']),
        ]
        ordering = ['-rating', '-created_at']

    def __str__(self):
        return f"{self.user.username} ({self.NIN})"

    def update_rating(self):
        """Update worker's average rating based on reviews"""
        avg_rating = self.reviews.aggregate(models.Avg('rating'))['rating__avg']
        self.rating = round(avg_rating, 2) if avg_rating else None
        self.save()

class Agent(models.Model):
    STATUS_CHOICES = [
        ('verified', 'Verified'),
        ('pending', 'Pending Verification'),
        ('suspended', 'Suspended'),
    ]

    active = models.BooleanField(default=False)
    NIN = models.CharField(
        max_length=20, 
        unique=True, 
        null=False, 
        blank=False,
        help_text="National Insurance Number"
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="agent_profile"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    avg_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Average price charged by the agent."
    )
    availability = models.BooleanField(
        default=True,
        help_text="Whether the agent is currently available for jobs."
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Average rating based on customer reviews."
    )
    profile_picture = models.ImageField(
        upload_to="agent_profiles/",
        null=True,
        blank=True,
        help_text="Profile picture of the agent."
    )
    bio = models.TextField(
        blank=True,
        help_text="Agent's professional biography and experience."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['status', 'active']),
            models.Index(fields=['rating']),
        ]
        ordering = ['-rating', '-created_at']

    def __str__(self):
        return f"{self.user.username} ({self.NIN})"

    def update_rating(self):
        """Update agent's average rating based on reviews"""
        avg_rating = self.reviews.aggregate(models.Avg('rating'))['rating__avg']
        self.rating = round(avg_rating, 2) if avg_rating else None
        self.save()

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

class Review(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    
    # Generic fields to associate with either a Worker or an Agent
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer} for {self.content_object}"
    
    class Meta:
        unique_together = ('customer', 'content_type', 'object_id')  # Ensure a customer can only review once for a worker/agent

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    worker = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text="Worker assigned to this booking."
    )
    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name='bookings',
        null=True,
        blank=True,
        help_text="Agent handling this booking."
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_bookings',
        help_text="Customer who made the booking."
    )
    service_description = models.TextField(
        help_text="Description of the service requested."
    )
    scheduled_time = models.DateTimeField(
        help_text="Scheduled date and time for the service."
    )
    duration_hours = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0.5)],
        help_text="Expected duration of the service in hours."
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Total cost of the service."
    )
    location = models.TextField(
        help_text="Service location address."
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes or special instructions."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['worker', 'scheduled_time']),
            models.Index(fields=['customer', 'scheduled_time']),
            models.Index(fields=['status']),
        ]
        ordering = ['-scheduled_time']

    def __str__(self):
        return f"Booking for {self.customer.username} with {self.worker.user.username} on {self.scheduled_time}"

    def save(self, *args, **kwargs):
        if not self.total_cost and self.duration_hours:
            self.total_cost = self.worker.hourly_rate * self.duration_hours
        super().save(*args, **kwargs)

    def can_cancel(self):
        """Check if booking can be cancelled (24 hours before scheduled time)"""
        return self.status in ['pending', 'confirmed'] and \
               self.scheduled_time > timezone.now() + timezone.timedelta(hours=24)
