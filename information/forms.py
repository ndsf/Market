from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'class': 'w3-input w3-border'}),
        }
