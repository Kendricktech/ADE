from django.urls import path
from .views import (
    AgentCreateView,
    AgentDetailView,
    AgentListView,
    AgentUpdateView,
    AgentDashBoardView,
    WorkerCreateView,
    WorkerDetailView,
    WorkerListView,
    WorkerUpdateView,
    WorkerDashBoardView,
    BookingCreateView,
    BookingDetailView,
    BookingListView,
    BookingUpdateView,
    BookingCancelView,
    ReviewCreateView,
    ReviewListView,
    ReviewUpdateView,
    ReviewDeleteView,
    Index,
    UnconfirmedView,
    AccountUpgradeView
)
app_name='services'
urlpatterns = [
    # Agent URLs
        path('', Index.as_view(), name='index'),
    path('unconfirmed/', UnconfirmedView.as_view(), name='unconfirmed'),
    path('work_with_us',AccountUpgradeView.as_view(),name='work_with_us'),

    path('agent/create/', AgentCreateView.as_view(), name='create_agent'),
    path('agent/<int:pk>/', AgentDetailView.as_view(), name='agent-detail'),
    path('agents/', AgentListView.as_view(), name='agents'),
    path('agent/update/<int:pk>/', AgentUpdateView.as_view(), name='agent-update'),
    path('agent/dashboard/', AgentDashBoardView.as_view(), name='agent-dashboard'),

    # Worker URLs
    path('worker/create/', WorkerCreateView.as_view(), name='create_worker'),
    path('worker/<int:pk>/', WorkerDetailView.as_view(), name='worker-detail'),
    path('workers/', WorkerListView.as_view(), name='workers'),
    path('worker/update/<int:pk>/', WorkerUpdateView.as_view(), name='worker-update'),
    path('worker/dashboard/', WorkerDashBoardView.as_view(), name='worker-dashboard'),

    # Booking URLs
path('booking/create/<int:worker_id>/', BookingCreateView.as_view(), name='booking-create'),
    path('booking/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('booking/update/<int:pk>/', BookingUpdateView.as_view(), name='booking-update'),
    path('booking/cancel/<int:pk>/', BookingCancelView.as_view(), name='booking-cancel'),

    # Review URLs
    path('review/create/<str:model_type>/<int:object_id>/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<str:model_type>/<int:object_id>/', ReviewListView.as_view(), name='review-list'),
    path('review/update/<str:model_type>/<int:object_id>/<int:pk>/', ReviewUpdateView.as_view(), name='review-update'),
    path('review/delete/<str:model_type>/<int:object_id>/<int:pk>/', ReviewDeleteView.as_view(), name='review-delete'),
]
