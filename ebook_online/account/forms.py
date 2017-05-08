from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from filer.fields.image import FilerImageField

from . import models

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'required': 'required'})
        )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'required':'required'}), 
        )

class UserForm(forms.ModelForm):
    alpanumeric = RegexValidator(regex="^[a-zA-Z0-9]*$", message="Please use alpanumeric characters only")
    name = RegexValidator(regex="^(?! )[A-Za-z0-9 ]*(?<! )$", message="Please enter a valid name")
    username = forms.CharField(
        max_length="50", min_length="6",
        widget=forms.TextInput(attrs={'required': 'required'}),
        validators=[alpanumeric,] 
        )
    first_name = forms.CharField(max_length="60", validators=[name,])
    last_name = forms.CharField(max_length="60", validators=[name,])
    password = forms.CharField(
        min_length="6",
        widget=forms.PasswordInput(attrs={'required':'required'})
        )
    password_validate = forms.CharField(
        min_length="6",
        widget=forms.PasswordInput(attrs={'required':'required'}),
        label="Confirm Password"
        )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def clean(self):
        cleaned_data = self.cleaned_data

        for key in cleaned_data:
            if cleaned_data[key] != cleaned_data[key].strip():
                raise forms.ValidationError("There are trailing whitespaces in some fields.")
        return cleaned_data
    
    def clean_username(self):
        cleaned_data = self.cleaned_data
        user = User.objects.filter(username=cleaned_data['username'])
        if user:
            raise forms.ValidationError("Username is already taken.")
        return cleaned_data['username']

    def clean_email(self):
        cleaned_data = self.cleaned_data
        user = User.objects.filter(email=cleaned_data['email'])
        if user:
            raise forms.ValidationError("Email is already taken.")
        return cleaned_data['email']

    def clean_password_validate(self):
        cleaned_data = self.cleaned_data

        if cleaned_data['password'] != cleaned_data['password_validate']:
            raise forms.ValidationError("Password does not match")
        return cleaned_data['password_validate']


class UserProfileEditForm(forms.ModelForm):
    name = RegexValidator(regex="^(?! )[A-Za-z0-9 ]*(?<! )$", message="Please enter a valid name")
    first_name = forms.CharField(max_length="60", validators=[name,])
    last_name = forms.CharField(max_length="60", validators=[name,])
    display_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
    

class PasswordEditForm(forms.Form):
    validator = RegexValidator(regex="^(?! )[$&+,:;=?@#|'<>.^*()%!-A-Za-z0-9 ]*(?<! )$", message="Please enter a valid name")
    old_password = forms.CharField(
        min_length="6",
        widget=forms.PasswordInput(attrs={'required':'required'}),
        validators=[validator,],
        label="Old Password",
        )
    new_password = forms.CharField(
        min_length="6",
        widget=forms.PasswordInput(attrs={'required':'required'}),
        validators=[validator,],
        label="New Password",
        )
    password_validate = forms.CharField(
        min_length="6",
        widget=forms.PasswordInput(attrs={'required':'required'}),
        label="Confirm Password",
        validators=[validator,],
        )

    def clean_password_validate(self):
        cleaned_data = self.cleaned_data
        print(cleaned_data)
        if cleaned_data['new_password'] != cleaned_data['password_validate']:
            raise forms.ValidationError("Password does not match")
        return cleaned_data['password_validate']