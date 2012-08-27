from finisht.success.models import Success
from django.forms import ModelForm
from django import forms

class SuccessForm(ModelForm):
    class Meta:
        model = Success
        fields = ('description',)
