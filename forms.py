# Importing the required modules

# The forms module is used to create the forms for the application
from django import forms

# The User model is used here to create a form for the default django user model
# It is used to create the registration form and the edit profile form
from django.contrib.auth.models import User


# The RegistrationForm class is used to create the registration form for the user
class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput,
        }

# The ChangePasswordForm class is used to create the change password form for the user
class ChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
