# coding: utf-8

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Company(models.Model):
    name = models.CharField(max_length=500, verbose_name=_('company name'), unique=True)

    class Meta:
        db_table = 'Companies'
        verbose_name = _('company')
        verbose_name_plural = _('companies')

    def __str__(self):
        return str(self.name)


class Profile(AbstractUser):
    company = models.ForeignKey(Company, verbose_name=_('company'), null=True)
    about_me = models.TextField(verbose_name=_('about me'))
    timezone = models.CharField(max_length=50, default='Europe/Moscow', verbose_name=_('time zone'))
    avatar = models.ImageField(upload_to='avatars', verbose_name=_('avatar'), blank=True)

    objects = UserManager()

    class Meta:
        db_table = 'Profiles'
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    def __str__(self):
        return self.username
