from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CurdOperations

class HomeForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']


class curdforms(forms.ModelForm):
    class Meta:
        model = CurdOperations
        fields = ['name','age','gender','email']

