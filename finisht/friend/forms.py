from finisht.friend.models import Friend
from django.forms import ModelForm
from django import forms

class FriendForm(ModelForm):
    class Meta:
        model = Friend
        fields = ('friend_user',)

