from django import forms
from django.core.exceptions import ValidationError

from .models import Post

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {
            'title',
            'picture',
            'status',
        }
    # picture = forms.ImageField()
    def clean_picture(self):
        image = self.cleaned_data.get('picture', False)
        print(self.cleaned_data)
        if image:
            if image._size > 1 * 1024 * 1024:
                raise ValidationError("Image file too large ( > 1mb )")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {
            'title',
            'status',
        }

class UserLoginForm(forms.Form):
    username = forms.CharField(label="")
    password = forms.CharField(label="", widget=forms.PasswordInput)