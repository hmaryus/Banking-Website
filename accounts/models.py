from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from django.core.validators import MinValueValidator


CHOISE_LOCATIONS = (('CLUJ','Cluj'),('MARAMURES','Maramures'),
                    ('ALBA', 'Alba'), ('ILFOV', 'Ilfov'),
                    ('IASI', 'Iasi'), ('TIMIS', 'Timis'),
                    ('BIHOR', 'Bihor'))


class UserProfile(AbstractUser):
    card_nr = models.CharField(max_length=16, default='')
    location = models.CharField(choices=CHOISE_LOCATIONS, max_length=20, default='')
    phone_number = models.CharField(_('phone number'), max_length=10, default='')
    bank_account = models.CharField(_('bank account'), max_length=20, default='')
    account_balance = models.IntegerField(_('account balance'), default=0)
    profile_pic = models.ImageField(upload_to='profile_image', null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def profile_pic_url(self):
        if self.profile_pic:
            return self.profile_pic.url
        return '/media/profile_image/no_img.jpg'


class Deposit(models.Model):
    user = models.ForeignKey(UserProfile, on_delete='CASCADE')
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('1.00'))
        ]
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Withdraw(models.Model):
    user = models.ForeignKey(UserProfile, on_delete='CASCADE')
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('1.00'))
        ]
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
