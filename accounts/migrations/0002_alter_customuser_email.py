# Generated by Django 4.2.3 on 2023-07-31 18:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, validators=[django.core.validators.RegexValidator('^[\\w\\.-]+@[\\w\\.-]+\\.[a-zA-Z]{2,}\\.ac\\.[a-zA-Z]{2,}$', 'Enter a valid email address with the format: <email_name>@<email_domain>.ac.<ending>.')]),
        ),
    ]
