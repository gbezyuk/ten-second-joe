"""
Studio: ActionLearning.Ru
Authors: Andrew Sinitsyn, Grigoriy Beziuk
Project: Ten Second Joe
Module: Ten Second Joe
Part: Django Admin integration
"""
from django.contrib import admin
from .models import LimitedLink

class LimitedLinkAdmin(admin.ModelAdmin):
    readonly_fields = ['usages_count']

admin.site.register(LimitedLink, LimitedLinkAdmin)