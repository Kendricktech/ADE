from django.contrib import admin
from .models import Worker, Agent, Review, Booking

# Register Worker model
@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('user', 'NIN', 'status', 'hourly_rate', 'rating', 'active', 'created_at')
    search_fields = ('user__username', 'NIN', 'status', 'services_offered')
    list_filter = ('status', 'active')
    ordering = ('-created_at',)

# Register Agent model
@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('user', 'NIN', 'status', 'avg_price', 'rating', 'active', 'created_at')
    search_fields = ('user__username', 'NIN', 'status')
    list_filter = ('status', 'active')
    ordering = ('-created_at',)

# Register Review model
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'content_object', 'rating', 'created_at')
    search_fields = ('customer__username', 'content_object__user__username')
    list_filter = ('rating',)
    ordering = ('-created_at',)

# Register Booking model
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'worker', 'agent', 'status', 'scheduled_time', 'total_cost', 'created_at')
    search_fields = ('customer__username', 'worker__user__username', 'agent__user__username')
    list_filter = ('status', 'scheduled_time')
    ordering = ('-scheduled_time',)
