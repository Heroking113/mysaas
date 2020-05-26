# -*- coding: utf-8 -*-
from django.contrib import admin

from home_application.models import ScriptSearch


# Register your models here.
@admin.register(ScriptSearch)
class ScriptSearchAdmin(admin.ModelAdmin):
    list_display = ('name', 'content')

