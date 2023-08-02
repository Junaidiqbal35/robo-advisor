import phonenumbers
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
    # TODO: add phone number field with validation
    # phone = PhoneNumberField()
    first_name = forms.CharField(label="First name", max_length=20)
    last_name = forms.CharField(label="Last name", max_length=20)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.form_id = 'signup-form'
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            ac_il_email_validator(email)
        except ValidationError as e:
            raise forms.ValidationError(str(e))
        return email

    # def clean_phone_number(self):
    #     phone_number = self.phone_number
    #
    #     try:
    #         parsed_phone = phonenumbers.parse(phone_number, None)
    #         if not phonenumbers.is_valid_number(parsed_phone):
    #             raise ValidationError('Enter a valid phone number (e.g. 02-123-4567) or a number with an '
    #                                   'international call prefix.')
    #     except phonenumbers.NumberParseException:
    #         raise ValidationError('Enter a valid phone number (e.g. 02-123-4567) or a number with an international '
    #                               'call prefix.')
    #
    #     return phone_number

    class Meta:
        model = CustomUser
        # TODO: add phone number field with validation
        # fields = ['email', 'phone', 'first_name', 'last_name', 'password']
        fields = ['email', 'first_name', 'last_name', 'phone_number']

        widgets = {
            'password': forms.PasswordInput(),

            'email': forms.TextInput(attrs={
                'hx-post': reverse_lazy('check_email'),
                'hx-target': '#div_id_email',
                'hx-trigger': 'keyup changed delay:1s'
            }),
            'phone_number': forms.TextInput(attrs={
                'hx-post': reverse_lazy('check_phone_number'),
                'hx-target': '#div_id_phone_number',
                'hx-trigger': 'keyup changed delay:1s'
            })
        }
# Enter a valid phone number (e.g. 02-123-4567) or a number with an international call prefix.

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
