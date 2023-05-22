
from django import forms
from .models import perfile

class PerfileUpdateForm(forms.ModelForm):
    class Meta:
        model = perfile
        fields = ['name', 'biography', 'image', 'ProfileBanner']