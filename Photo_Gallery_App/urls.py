from django.urls import path
from . import views

urlpatterns = [
    # Home
    path("", views.home, name="home"),

    # Authentication
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Profile
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    # Photos
    path("upload/", views.upload_photo, name="upload_photo"),
    path("photo/<int:pk>/", views.photo_detail, name="photo_detail"),

    # Like / Dislike
    path("photo/<int:pk>/like/", views.react_photo, {"reaction": "LIKE"}, name="like_photo"),
    path("photo/<int:pk>/dislike/", views.react_photo, {"reaction": "DISLIKE"}, name="dislike_photo"),
]