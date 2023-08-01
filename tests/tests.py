import pytest
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
def test_user_registration(client):
    # Test user registration
    data = {
        'first_name': 'test',
        'last_name': 'user',
        'phone_number': '+97221234567',
        'email': 'test@example.com',
        'password': 'testpassword',

    }
    response = client.post(reverse('signup'), data)
    print(response.status_code)
    assert response.status_code == 200

    # assert CustomUser.objects.filter(email='test@example.com').exists()


@pytest.mark.django_db
def test_user_login_logout(client, user_factory):
    # Create a test user
    user = user_factory()

    # Test user login
    data = {
        'login': user.email,
        'password': 'testpassword',
    }
    response = client.post(reverse('account_login'), data)

    assert response.status_code == 200

    # Test user logout
    response = client.post(reverse('account_logout'))
    print(response.status_code)
    assert response.status_code == 302


def test_login_invalid_credentials(client, user_factory):
    user = user_factory()

    response = client.post(reverse('account_login'), data={
        'email': user.email,
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

    assert response.status_code == 302  # Redirects to the success URL after the reset request

    # Retrieve the reset URL from the response
    reset_url = response.url

    # Now simulate clicking the reset link in the email
    response = client.get(reset_url)

    assert response.status_code == 200


@pytest.fixture
def user_factory(db):
    def create_user(**kwargs):
        user = CustomUser.objects.create(first_name='tester', last_name='1', phone_number='21234567',
                                         email='test@example.com',
                                         password='testpassword')
        print(user)
        return user

    return create_user
