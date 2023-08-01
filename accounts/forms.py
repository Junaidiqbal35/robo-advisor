from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from django.urls import reverse_lazy

from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


# TODO: make a User model that its unique field is `email` and not `username`; i.e. we don't need username at all
def ac_il_email_validator(value):
    if not value.endswith('.ac.il'):
        raise ValidationError('Enter a valid email address with the domain ending ".ac.il".')


class UserRegisterForm(UserCreationForm):

    # TODO: Email must include `@ac` - thus be academic email!
    email = forms.EmailField(label="Email address", validators=[ac_il_email_validator])
    # TODO: add phone number field with validation
    # phone = PhoneNumberField()
    first_name = forms.CharField(label="First name", max_length=20)
    last_name = forms.CharField(label="Last name", max_length=20)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.form_id = 'signup-form'
        self.helper.attrs = {
            'hx-post': reverse_lazy('signup'),
            'hx-target': '#signup-form',
            # 'hx-swap': 'innerHTML'
        }
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = CustomUser
        # TODO: add phone number field with validation
        # fields = ['email', 'phone', 'first_name', 'last_name', 'password']
        fields = ['email', 'first_name', 'last_name', 'phone_number']

        widgets = {
            'password': forms.PasswordInput(),

            'email': forms.TextInput(attrs={
                'hx-get': reverse_lazy('check_email'),
                'hx-target': '#div_id_email',
                'hx-trigger': 'keyup changed delay:1s'
            })
        }


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label="First name", max_length=20)
    last_name = forms.CharField(label="Last name", max_length=20)

    # TODO: add phone number field with validation
    # phone = PhoneNumberField()

    class Meta:
        model = CustomUser
        # TODO: make password update possible to accounts (it is not currently), including validation
        # TODO: add phone number field with validation
        # fields = ['phone', 'first_name', 'last_name']
        fields = ['first_name', 'last_name']
