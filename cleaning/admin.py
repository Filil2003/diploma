from django.contrib import admin
from django.db import models

from .models import Service, Option, ServiceOption, Place, ServicePlace
from .widgets import AdminImagePreviewWidget


class ServiceOptionInline(admin.TabularInline):
    model = ServiceOption
    classes = ('collapse',)
    extra = 0


class ServicePlaceInline(admin.TabularInline):
    model = ServicePlace
    classes = ('collapse',)
    formfield_overrides = {
        models.ImageField: {'widget': AdminImagePreviewWidget},
    }
    extra = 0


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    inlines = (ServiceOptionInline, ServicePlaceInline)
    list_display = ('title', 'slug', 'base_price')
    search_fields = ('title',)
    formfield_overrides = {
        models.ImageField: {'widget': AdminImagePreviewWidget},
    }

    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)
        if formset.model == ServiceOption:
            service = form.instance
            service.refresh_from_db()
            service.calculate_base_price()
            service.save()


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    search_fields = ('title',)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    search_fields = ('title',)
