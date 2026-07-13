from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
from .models import (
    CustomUser,
    Profile,
    Photo,
    Tag,
    PhotoReaction,
)

from .forms import (
    RegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    PhotoForm,
)


def home(request):
    photos = Photo.objects.all().order_by("-created_at")
    tags = Tag.objects.all()

    tag_name = request.GET.get("tag")

    if tag_name:
        photos = photos.filter(tags__name=tag_name)

    context = {
        "photos": photos,
        "tags": tags,
    }

    return render(request, "Photo_Gallery_App/home.html", context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "Photo_Gallery_App/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "Photo_Gallery_App/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def profile(request):
    return render(
        request,
        "Photo_Gallery_App/profile.html",
        {"profile": request.user.profile},
    )


@login_required
def edit_profile(request):

    if request.method == "POST":

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, "Profile updated successfully.")
            return redirect("profile")

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(
        request,
        "Photo_Gallery_App/edit_profile.html",
        context,
    )


@login_required
def upload_photo(request):

    if request.method == "POST":

        form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploaded_by = request.user
            photo.save()

            form.save_m2m()

            messages.success(request, "Photo uploaded successfully.")
            return redirect("home")

    else:
        form = PhotoForm()

    return render(
        request,
        "Photo_Gallery_App/upload_photo.html",
        {"form": form},
    )


def photo_detail(request, pk):

    photo = get_object_or_404(Photo, pk=pk)

    context = {
        "photo": photo,
    }

    return render(
        request,
        "Photo_Gallery_App/photo_detail.html",
        context,
    )


@login_required
def react_photo(request, pk, reaction):

    photo = get_object_or_404(Photo, pk=pk)

    PhotoReaction.objects.update_or_create(
        user=request.user,
        photo=photo,
        defaults={"reaction": reaction},
    )

    return redirect("photo_detail", pk=pk)