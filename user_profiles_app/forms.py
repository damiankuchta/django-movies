from django import forms


class Login(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)