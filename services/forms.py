from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Worker, Booking, Review,Agent

class WorkerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['NIN', 'services_offered', 'hourly_rate', 'profile_picture']
        widgets = {
            'services_offered': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_NIN(self):
        nin = self.cleaned_data.get('NIN')
        if Worker.objects.filter(NIN=nin).exists():
            raise ValidationError('This National Insurance Number is already registered.')
        return nin

class AgentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['NIN',  'avg_price', 'profile_picture']
      

    def clean_NIN(self):
        nin = self.cleaned_data.get('NIN')
        if Worker.objects.filter(NIN=nin).exists():
            raise ValidationError('This National Insurance Number is already registered.')
        return nin

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service_description', 'scheduled_time', 'duration_hours', 'location', 'notes']
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'service_description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_scheduled_time(self):
        scheduled_time = self.cleaned_data.get('scheduled_time')
        if scheduled_time:
            # Check if time is in the future
            if scheduled_time < timezone.now():
                raise ValidationError('Booking time must be in the future.')
            
            # Check if time is during reasonable hours (e.g., 8 AM to 8 PM)
            if scheduled_time.hour < 8 or scheduled_time.hour > 20:
                raise ValidationError('Bookings must be between 8 AM and 8 PM.')

        return scheduled_time

    def clean(self):
        cleaned_data = super().clean()
        scheduled_time = cleaned_data.get('scheduled_time')
        duration_hours = cleaned_data.get('duration_hours')
        worker = self.instance.worker if self.instance else None

        if scheduled_time and duration_hours and worker:
            # Check for booking conflicts
            end_time = scheduled_time + timezone.timedelta(hours=float(duration_hours))
            conflicting_bookings = Booking.objects.filter(
                worker=worker,
                scheduled_time__lt=end_time,
                status__in=['pending', 'confirmed']
            ).exclude(pk=self.instance.pk if self.instance else None)

            if conflicting_bookings.exists():
                raise ValidationError('This time slot conflicts with existing bookings.')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5})
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating and (rating < 1 or rating > 5):
            raise ValidationError('Rating must be between 1 and 5.')
        return rating

    def clean(self):
        cleaned_data = super().clean()
        worker = self.instance.worker if self.instance else None
        customer = self.instance.customer if self.instance else None

        if worker and customer:
            # Check if customer has completed booking with worker
            completed_booking = Booking.objects.filter(
                worker=worker,
                customer=customer,
                status='completed'
            ).exists()

            if not completed_booking:
                raise ValidationError('You can only review workers after completing a booking with them.')

            # Check if already reviewed
            existing_review = Review.objects.filter(
                worker=worker,
                customer=customer
            ).exclude(pk=self.instance.pk if self.instance else None).exists()

            if existing_review:
                raise ValidationError('You have already reviewed this worker.')

class WorkerAvailabilityForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['availability']

class WorkerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['services_offered', 'hourly_rate', 'profile_picture']
        widgets = {
            'services_offered': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_hourly_rate(self):
        rate = self.cleaned_data.get('hourly_rate')
        if rate and rate < 0:
            raise ValidationError('Hourly rate cannot be negative.')
        return rate

class BookingFilterForm(forms.Form):
    STATUS_CHOICES = [('', 'All')] + list(Booking.STATUS_CHOICES)
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')

        if date_from and date_to and date_from > date_to:
            raise ValidationError('Start date must be before end date.')
        
    