# Generated by Django 2.2.22 on 2021-07-31 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSecurityToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extras', models.CharField(blank=True, max_length=255, null=True)),
                ('token', models.CharField(max_length=150)),
                ('token_type', models.SmallIntegerField(choices=[(1, 'Forgot Password'), (2, 'Account Activation Link')])),
                ('expire_date', models.DateTimeField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tokens', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
