import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse, resolve
from django.http import Http404
from accounts import views
from accounts.forms import ac_il_email_validator

from accounts.models import CustomUser


def test_home_url():
    # Test home URL
    url = reverse('homepage')
    assert resolve(url).view_name == 'homepage'


def test_about_url():
    # Test home URL
    url = reverse('about')
    assert resolve(url).view_name == 'about'


def test_capital_market_algorithm_preferences_form():
    # Test home URL
    url = reverse('capital_market_algorithm_preferences_form')
    assert resolve(url).view_name == 'capital_market_algorithm_preferences_form'


def test_capital_market_investment_preferences_form():
    # Test home URL
    url = reverse('capital_market_investment_preferences_form')
    assert resolve(url).view_name == 'capital_market_investment_preferences_form'


def test_registration_url():
    # Test URL for YourView
    url = reverse('signup')
    view = resolve(url).func.view_class
    assert view == views.SignUpView


def test_login_url():
    # Test URL for YourView
    url = reverse('account_login')
    view = resolve(url).func.view_class
    assert view == views.HtmxLoginView


def test_logout_url():
    # Test URL for YourView
    url = reverse('account_logout')
    assert resolve(url).view_name == 'account_logout'


@pytest.mark.django_db
def test_user_registration(client, user_factory):
    # Test user registration
    data = {
        'first_name': 'test',
        'last_name': 'user',
        'phone_number': '+97221234567',
        'email': 'test@example.ac.il',
        'password1': 'django1234',
        'password2': 'django1234',

    }
    user = user_factory(**data)
    assert user is not None
    assert user.first_name == 'test'
    assert user.last_name == 'user'
    response = client.post(reverse('signup'), data)
    assert response.request['REQUEST_METHOD'] == 'POST'

    assert response.status_code == 200

    assert CustomUser.objects.filter(email='test@example.ac.il').exists()


@pytest.mark.django_db
def test_user_login_logout(client, user_factory):
    # Create a test user
    user = user_factory()
    print(user.email)

    # Test user login
    data = {
        'login': user.email,
        'password': 'django1234',
    }
    response = client.post(reverse('account_login'), data)
    assert response.status_code == 200
    assert response.request['REQUEST_METHOD'] == 'POST'

    # Test user logout
    response = client.post(reverse('account_logout'))

    assert response.status_code == 302


def test_login_invalid_credentials(client, user_factory):
    user = user_factory()

    response = client.post(reverse('account_login'), data={
        'login': user.email,
        'password': 'wrongpassword',
    })

    assert response.status_code == 200
    assert '_auth_user_id' not in client.session


def test_ac_il_email_validator_valid():
    # Valid email addresses
    valid_emails = [
        'john.doe@university.ac.il',
        'jane.smith@college.ac.il',
        'foo.bar@school.ac.il',
    ]

    for email in valid_emails:
        # The validator should not raise any exception for valid emails
        ac_il_email_validator(email)


def test_ac_il_email_validator_invalid():
    # Invalid email addresses
    invalid_emails = [
        'invalid.email@example.com',
        'user@domain.com',
        'user@acil',
        'user@university.ac.com',
    ]

    for email in invalid_emails:
        # The validator should raise a ValidationError for invalid emails
        with pytest.raises(ValidationError):
            ac_il_email_validator(email)


def test_password_reset(client, user_factory):
    user = user_factory()
    response = client.post(reverse('account_reset_password'), data={
        'email': user.email,
    })
    assert response.status_code == 302

    # Retrieve the reset URL from the response
    reset_url = response.url
    response = client.get(reset_url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_registration_invalid_phone_number(client):
    # Test user registration with invalid phone number format
    data = {
        'first_name': 'test',
        'last_name': 'user',
        'phone_number': '12345',  # Invalid phone number format
        'email': 'test@example.com',
        'password': 'testpassword',
    }
    response = client.post(reverse('signup'), data)
    assert response.status_code == 200
    assert 'Enter a valid phone number' in response.content.decode()


@pytest.mark.django_db
def test_user_registration_invalid_email(client):
    # Test user registration with invalid email format
    data = {
        'first_name': 'test',
        'last_name': 'user',
        'phone_number': '+97221234567',
        'email': 'invalid_email@gmail.com',
        'password': 'testpassword',
    }
    response = client.post(reverse('signup'), data)
    assert response.status_code == 200
    assert 'Enter a valid email address' in response.content.decode()


@pytest.fixture
def user_factory(db):
    def create_user(**kwargs):
        user = CustomUser.objects.create(
            first_name=kwargs.get('first_name', 'test'),
            last_name=kwargs.get('last_name', 'user'),
            phone_number=kwargs.get('phone_number', '+97221234567'),
            email=kwargs.get('email', 'test@example.ac.il'),
            password=kwargs.get('password', 'django1234')
        )

        return user

    return create_user
