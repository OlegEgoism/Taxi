import re
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

    def clean_phone_email(self):
        value = self.cleaned_data.get('phone_email', '').strip()
        if not value:
            return value
        is_phone = re.match(r'^\+375\d{9}$', value)
        is_email = '@' in value and not value.startswith('@') and not value.endswith('@')
        if not (is_phone or is_email):
            raise forms.ValidationError(
                "Введите корректные данные. Телефон в формате +375XXXXXXXXX или корректный email"
            )
        return value
