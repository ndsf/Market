from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('user_to', 'body')
        widgets = {
            'user_to': forms.Select(attrs={'class': 'w3-select w3-border'}),
            'body': forms.Textarea(attrs={'class': 'w3-input w3-border'}),
        }