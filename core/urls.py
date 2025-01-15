from django.contrib import admin
from django.urls import path, include
from .views import index, services, agents_list, agents_listing,DashBoardView
from django.conf import settings
from django.conf.urls.static import static
import accounts.urls as account_urls

urlpatterns = [
    path('services', include('services.urls'), name='services'),
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('dashboard/',DashBoardView.as_view(),name='dashboard'),
    path("__reload__/", include("django_browser_reload.urls")),
    path('accounts/', include(account_urls), name='accounts'),
    path('listings/', include('listings.urls')),  # Include listings URLs
    path('conversation', include('conversation.urls')),
    path('agents/<int:id>/listings/', agents_listing, name='agent_listings'),
]

# Adding static and media URLs
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
