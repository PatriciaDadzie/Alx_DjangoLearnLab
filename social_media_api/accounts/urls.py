from django.urls import path
from .views import RegisterView, LoginView, ProfileView, FollowUserView, UnfollowUserView

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("follow_user/<int:user_id>/", FollowUserView.as_view(), name="follow_user"),
    path("unfollow_user/<int:user_id>/", UnfollowUserView.as_view(), name="unfollow_user"),
]
