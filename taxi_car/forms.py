from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    """Обратная связь"""
    class Meta:
        model = Feedback
        fields = ['name', 'phone_email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя', 'id': 'name', 'style': 'border-radius: 0px'}),
            'phone_email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон или email', 'id': 'phone_email', 'style': 'border-radius: 0px'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Сообщение', 'id': 'message', 'style': 'height: 250px; border-radius: 0px'}),
        }
