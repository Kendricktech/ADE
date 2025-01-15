from django.urls import path
from . import views

app_name = 'conversation'

urlpatterns = [
    path('', views.InboxView.as_view(), name='inbox'),
    path('<int:pk>/', views.ConversationDetailView.as_view(), name='detail'),
    path('new/<str:item_type>/<int:id>/', views.NewConversationView.as_view(), name='new'),  # Updated URL
]
