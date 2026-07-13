from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    profile_picture = models.ImageField(upload_to="profile_pictures/")
    tags = models.ManyToManyField(Tag, blank=True)
    uploaded_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="photos"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.reactions.filter(reaction="LIKE").count()

    def total_dislikes(self):
        return self.reactions.filter(reaction="DISLIKE").count()

    def __str__(self):
        return self.title


class PhotoReaction(models.Model):
    REACTION_CHOICES = [
        ("LIKE", "Like"),
        ("DISLIKE", "Dislike"),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )
    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
        related_name="reactions"
    )
    reaction = models.CharField(
        max_length=10,
        choices=REACTION_CHOICES
    )

    class Meta:
        unique_together = ("user", "photo")

    def __str__(self):
        return f"{self.user.username} - {self.reaction} - {self.photo.title}"