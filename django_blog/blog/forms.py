from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Post, Comment, Tag


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
# Post Form (with tags)
# ----------------------
class PostForm(forms.ModelForm):
    # extra field for comma-separated tags
    tags_field = forms.CharField(
        required=False,
        help_text="Enter comma-separated tags (e.g. django, python, tutorial)",
        widget=forms.TextInput(attrs={"placeholder": "tag1, tag2, tag3"}),
    )

    class Meta:
        model = Post
        fields = ["title", "content"]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        super().__init__(*args, **kwargs)
        if instance:
            # pre-populate with existing tags
            self.fields["tags_field"].initial = ", ".join(
                [tag.name for tag in instance.tags.all()]
            )

    def clean_tags_field(self):
        raw = self.cleaned_data.get("tags_field", "")
        tags = [t.strip() for t in raw.split(",") if t.strip()]
        return tags

    def save(self, commit=True):
        post = super().save(commit=commit)
        tags = self.cleaned_data.get("tags_field", [])
        if commit:
            # clear and re-attach tags
            post.tags.clear()
            for tag_name in tags:
                tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag_obj)
        else:
            self._pending_tags = tags
        return post


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
