from decimal import Decimal

from autoslug import AutoSlugField
from django.db import models
from django.db.models import QuerySet, Sum
from django.urls import reverse
from django.utils.functional import cached_property
from pytils.translit import slugify

from utils.fields import WEBPField


def get_service_banner_upload_path(instance, filename):
    """ Get the loading path for the service banner. """
    filename, extension = filename.rsplit('.', 1)
    # Rename an upload image to `banner`.
    filename = 'banner'
    return f'cleaning/services/{instance.pk}/{filename}.{extension}'


class Service(models.Model):
    """ A service for cleaning. """
    title: str = models.CharField(unique=True, max_length=100)
    short_title: str = models.CharField(unique=True, max_length=50)
    slug: str = AutoSlugField(
        max_length=50,
        populate_from='title',
        always_update=True,
        allow_unicode=True
    )
    description: str = models.TextField(blank=True)
    banner: WEBPField = WEBPField(
        upload_to=get_service_banner_upload_path,
        blank=True
    )
    base_price: Decimal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        editable=False
    )

    def __str__(self) -> str:
        return self.title

    def calculate_base_price(self):
        if self.options.exists():
            self.base_price = self.options.filter(is_included=True).aggregate(total_price=Sum('price'))['total_price']

    @cached_property
    def absolute_url(self) -> str:
        """ Absolute URL for the service detail page. """
        return reverse('cleaning:service_detail', args=[self.slug])

    @cached_property
    def places(self) -> QuerySet:
        """ List of all places used by the service. """
        return self.serviceplace_set.select_related('place')

    @cached_property
    def options(self) -> QuerySet:
        """ List of all options used by the service. """
        return self.serviceoption_set.select_related('option')

    def included_options(self) -> QuerySet:
        """ List of all included options used by the service. """
        return self.options.filter(is_included=True)

    def extra_options(self) -> QuerySet:
        """ List of all extra options used by the service. """
        return self.options.exclude(is_included=True)

    def get_options_for_place(self, place) -> tuple:
        """ All options for a particular place used by the service. """
        included_options = self.options.filter(place=place, is_included=True)
        extra_options = self.options.filter(place=place, is_included=False)
        return included_options, extra_options


class Place(models.Model):
    """ The place where the option performed. """
    title: str = models.CharField(unique=True, max_length=50)

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return self.title


class Option(models.Model):
    """  Options. """

    class TypeEnum(models.TextChoices):
        """ Enumerating types for the option. """
        QUANTITATIVE: str = 'Quantitative'
        SWITCH: str = 'Switch'

    class UnitEnum(models.TextChoices):
        """ Enumerating units for the option. """
        PIECE: str = 'шт', 'штука,штуки,штук'
        HOUR: str = 'час', 'час,часа,часов'

    title: str = models.CharField(unique=True, max_length=50)
    description: str = models.TextField(blank=True)
    type: str = models.CharField(
        max_length=20,
        choices=TypeEnum.choices,
        default=TypeEnum.SWITCH.value
    )
    unit: str = models.CharField(
        max_length=20,
        choices=UnitEnum.choices,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return self.title

    def get_unit_forms(self) -> str:
        forms = {
            'шт': 'штука,штуки,штук',
            'час': 'час,часа,часов',
        }
        return forms.get(self.unit, '')


def get_service_place_thumbnail_upload_path(instance, filename):
    """ Get the loading path for the service place thumbnail. """
    # Rename an upload image to place title.
    slugged_filename = slugify(instance.place.title)
    new_filename = f'{slugged_filename}.webp'.lower()
    return f'cleaning/services/{instance.service.pk}/places/{new_filename}'


class ServicePlace(models.Model):
    """ Service and place relation. """
    service: Service = models.ForeignKey('Service', on_delete=models.CASCADE)
    place: Place = models.ForeignKey('Place', on_delete=models.CASCADE)
    thumbnail: WEBPField = WEBPField(
        upload_to=get_service_place_thumbnail_upload_path,
        blank=True
    )

    class Meta:
        unique_together: tuple = ('service', 'place')

    def __str__(self) -> str:
        return f'{self.service.title} - {self.place.title}'


class ServiceOption(models.Model):
    """ Option related to the service. """
    service: Service = models.ForeignKey('Service', on_delete=models.CASCADE)
    option: Option = models.ForeignKey('Option', on_delete=models.CASCADE)
    place: Place = models.ForeignKey('Place', on_delete=models.CASCADE)
    price: Decimal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    is_included: bool = models.BooleanField(default=True)

    class Meta:
        unique_together: tuple = ('service', 'option', 'place')

    def __str__(self) -> str:
        return f'{self.service.title} - {self.option.title}'
