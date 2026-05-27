from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'email',
            'address',
            'postal_code',
            'city',
        ]
        labels = {
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'email': _('Эл. почта'),
            'address': _('Адрес'),
            'postal_code': _('Индекс'),
            'city': _('Город'),
        }
        
        def __init__(self, *args, **kwargs):
            self.fields['related_field'].widget = forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )