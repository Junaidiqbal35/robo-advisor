from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

RISK_MIN = 1
RISK_MAX = 3


# Custom User
class UserManager(BaseUserManager):
    """
    custom model accounts manager
    """

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("email is required")
        email = self.normalize_email(email)
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """creates new superuser with details """

        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    """
    custom accounts model
    """
    username = models.CharField(max_length=50, db_index=True, blank=True, null=True)
    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = PhoneNumberField()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email


class InvestorUser(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    risk_level = models.IntegerField(validators=[MinValueValidator(RISK_MIN), MaxValueValidator(RISK_MAX)])
    starting_investment_amount = models.IntegerField()
    stocks_symbols = models.CharField(max_length=500)  # Symbols are divided by `;`
    stocks_weights = models.CharField(max_length=1000)  # Symbols are divided by `;`
    sectors_names = models.CharField(max_length=500)  # Symbols are divided by `;`
    sectors_weights = models.CharField(max_length=1000)  # Symbols are divided by `;`
    annual_returns = models.FloatField()
    annual_max_loss = models.FloatField()
    annual_volatility = models.FloatField()
    annual_sharpe = models.FloatField()
    total_change = models.FloatField()
    monthly_change = models.FloatField()
    daily_change = models.FloatField()

    class Meta:
        db_table = 'InvestorUser'
