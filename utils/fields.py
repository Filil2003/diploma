import io

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.utils.text import slugify


class WEBPFieldFile(ImageFieldFile):
    """
    A file field for saving images in WEBP format.
    Automatically convert the image to WEBP format and save it.

    Usage:
        1. Define a model field using WEBPField instead of ImageField.
        2. Any image uploaded through this field will save as a WEBP image.
    """

    # Override the save method for processing images in WEBP format.
    def save(self, name, content, save=True):
        # Move the file pointer to the beginning.
        content.file.seek(0)

        # Open image with a PIL library.
        image = Image.open(content.file)

        # Create a temporary object to save the image in WEBP format.
        image_bytes = io.BytesIO()

        # Save the image in WEBP format to the temporary object
        image.save(fp=image_bytes, format='WEBP')

        # Create ContentFile from byte representation of image.
        image_content_file = ContentFile(content=image_bytes.getvalue())

        # Change the file extension to '.webp'.
        name, _ = name.rsplit('.', 1)
        name = f'{slugify(name).lower()}.webp'

        # Call the parent save method to save the image.
        super().save(name, image_content_file, save)


class WEBPField(models.ImageField):
    attr_class = WEBPFieldFile
