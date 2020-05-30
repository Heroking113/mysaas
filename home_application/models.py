# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class ScriptSearch(models.Model):
    name = models.CharField(max_length=100, default='')
    content = models.CharField(max_length=300, default='')
