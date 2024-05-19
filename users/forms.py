from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")


# class CustomerSignUpForm(UserCreationForm):
#    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}), help_text='Required. Enter a valid email address.')
# c'est la qu'on va creer le formulaire pour customer
# email
# password
# password confirmation
# username
# date of birth

class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'}))
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date of birth'}),
         input_formats=['%d/%m/%Y']
        )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('username', 'password1', 'password2','email', 'date_of_birth')



class CompanySignUpForm(UserCreationForm):
    # il faut faire la liste deroulante field
    
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    username = forms.CharField(max_length=30, help_text='Required. Enter a username.')
    password1 = forms.CharField(widget=forms.PasswordInput, help_text='Required. Enter a password.')
    password2 = forms.CharField(widget=forms.PasswordInput, help_text='Required. Confirm your password.')
    # field_of_work = forms.CharField(max_length=100, help_text='Enter your field of work.')
    field = forms.ChoiceField(
        choices=[(field[0], field[1]) for field in Company._meta.get_field('field').choices],
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Field of work'}))
    class Meta:
        model = User
        fields = ( 'username', 'password1', 'password2', 'email','field')

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autocomplete'] = 'off'
