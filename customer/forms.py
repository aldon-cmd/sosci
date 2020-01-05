import random
import string

from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.conf import settings
from django.utils.http import is_safe_url
from django.contrib.auth import password_validation
from customer import models
from custom_user import models as user_models
from customer.utils import normalise_email
from catalogue import models as catalogue_models


def generate_username():
    # Python 3 uses ascii_letters. If not available, fallback to letters
    try:
        letters = string.ascii_letters
    except AttributeError:
        letters = string.letters
    uname = ''.join([random.choice(letters + string.digits + '_')
                     for i in range(30)])
    try:
        user_models.User.objects.get(username=uname)
        return generate_username()
    except user_models.User.DoesNotExist:
        return uname


class EmailUserCreationForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput)
    redirect_url = forms.CharField(
        widget=forms.HiddenInput, required=False)

    class Meta:
        model = user_models.User
        fields = ('email','first_name','last_name',)

    def __init__(self, host=None, *args, **kwargs):
        self.host = host
        super(EmailUserCreationForm, self).__init__(*args, **kwargs)

    def clean_first_name(self):
        return self.cleaned_data['first_name'].title()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].title()

    def clean_email(self):
        """
        Checks for existing users with the supplied email address.
        """
        email = normalise_email(self.cleaned_data['email'])
        if user_models.User._default_manager.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "A user with that email address already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        if password1 != password2:
            raise forms.ValidationError(
                "The two password fields didn't match.")
        password_validation.validate_password(password2, self.instance,[
                password_validation.MinimumLengthValidator(min_length=6),
                password_validation.CommonPasswordValidator(),
            ])
        return password2

    def clean_redirect_url(self):
        url = self.cleaned_data['redirect_url'].strip()
        if url and is_safe_url(url, self.host):
            return url
        return settings.LOGIN_REDIRECT_URL

    def save(self, commit=True):
        user = super(EmailUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False # not active until they open activation link

        if 'username' in [f.name for f in user_models.User._meta.fields]:
            user.username = generate_username()
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
       
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['username'].widget.attrs.update({'placeholder':'Email'})
        self.fields['password'].widget.attrs.update({'placeholder':'Password'})

class IndividualStudentInviteForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)    
    

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user",None)
        super(IndividualStudentInviteForm, self).__init__(*args, **kwargs)
        course_queryset = catalogue_models.Product.objects.filter(user=user)
        self.fields['course'] = forms.ModelChoiceField(queryset=course_queryset)

    def clean_first_name(self):
        return self.cleaned_data['first_name'].title()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].title()                     