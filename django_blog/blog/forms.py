from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from taggit.forms import TagWidget   # ✅ import TagWidget
from .models import Profile, Post, Comment


# ----------------------
# User & Profile Forms
# ----------------------
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]


# ----------------------
# Post Form (with TagWidget)
# ----------------------
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "tags"]
        widgets = {
            "tags": TagWidget(),   
        }


# ----------------------
# Comment Form
# ----------------------
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Write your comment here..."}
            ),
        }
