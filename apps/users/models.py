# -*- coding:utf8 -*-
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username