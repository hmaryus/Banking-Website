from django import forms
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import UserProfile, Deposit, Withdraw
from django.utils.translation import gettext, gettext_lazy as _
from .validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator


User = get_user_model()


CHOISE_LOCATIONS = (('CLUJ', 'Cluj'), ('MARAMURES', 'Maramures'),
                    ('ALBA', 'Alba'), ('ILFOV', 'Ilfov'),
                    ('IASI', 'Iasi'), ('TIMIS', 'Timis'),
                    ('BIHOR', 'Bihor'))


class RegistrationForm(UserCreationForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'username_used':_("Username is already in use."),}

    username_validator = UnicodeUsernameValidator()
    username     = forms.CharField(max_length=20,
        help_text=_('Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },)
    email        = forms.EmailField(required=True)
    password1    = forms.CharField(max_length=100, widget=forms.PasswordInput, label= ("Password"))
    password2    = forms.CharField(max_length=100, widget=forms.PasswordInput, label= ("Password Confirmation"))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
                ]

    #
    def clean_email(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch'
            )
        return password2

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class EditProfileForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'pattern': r'^[A-Za-z]+$'}), max_length=20, required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'pattern': r'^[A-Za-z]+$'}), max_length=20, required=True)
    email = forms.EmailField(required=True)
    card_nr = forms.CharField(widget=forms.TextInput(attrs={'pattern': r'^[0-9]+$'}),
                              min_length=16, max_length=16, required=True)
    location = forms.ChoiceField(choices=CHOISE_LOCATIONS, required=True)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'pattern': r'^[0-9]+$'}),
                                   min_length=10, max_length=10, required=True)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'email',
            'card_nr',
            'location',
            'phone_number',
            'profile_pic'
        ]


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ["amount"]


class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Withdraw
        fields = ["amount"]