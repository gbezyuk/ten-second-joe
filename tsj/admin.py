"""
Studio: ActionLearning.Ru
Authors: Andrew Sinitsyn, Grigoriy Beziuk
Project: Ten Second Joe
Module: Ten Second Joe
Part: Django Admin integration
"""
from django.contrib import admin
from django.contrib.contenttypes import generic
from .models import LimitedLink, YoutubeLink

class LimitedLinkAdmin(admin.ModelAdmin):
    readonly_fields = ['usages_count']

class LimitedLinkTabularInline(generic.GenericTabularInline):
    model = LimitedLink
    readonly_fields = ['usages_count']

class YoutubeLinkAdmin(admin.ModelAdmin):
    readonly_fields = ['video_cache']
    inlines = [LimitedLinkTabularInline]

admin.site.register(LimitedLink, LimitedLinkAdmin)
admin.site.register(YoutubeLink, YoutubeLinkAdmin)
