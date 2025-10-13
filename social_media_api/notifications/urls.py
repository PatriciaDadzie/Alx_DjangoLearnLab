from django.urls import path
from .views import NotificationListView
from .views import FeedView


urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('feed/', FeedView.as_view(), name='user-feed'),

]
