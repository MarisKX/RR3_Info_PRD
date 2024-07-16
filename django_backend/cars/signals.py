from PIL import Image
import io
import sys
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import CarUpgrade, OfficialColors

@receiver(post_save, sender=CarUpgrade)
def update_car_upgrades_total_on_save(sender, instance, **kwargs):
    instance.car.update_upgrades_total()

@receiver(post_delete, sender=CarUpgrade)
def update_car_upgrades_total_on_delete(sender, instance, **kwargs):
    instance.car.update_upgrades_total()

@receiver(pre_save, sender=OfficialColors)
def crop_oe_color_image_before_save(sender, instance, **kwargs):
    if instance.image:
        try:
            # Open the image
            img = Image.open(instance.image)
            width, height = img.size
            crop_top_height = 150  # Height in pixels to crop from the top
            crop_bottom_height = 30  # Height in pixels to crop from the bottom

            # Calculate the cropping box
            box = (0, crop_top_height, width, height - crop_bottom_height)
            cropped_image = img.crop(box)

            # Save the cropped image to an in-memory file
            img_format = img.format if img.format else 'PNG'
            img_io = io.BytesIO()
            cropped_image.save(img_io, format=img_format)
            img_io.seek(0)

            # Create a new InMemoryUploadedFile
            new_image = InMemoryUploadedFile(
                img_io,
                field_name=instance.image.field.name,
                name=instance.image.name,
                content_type=instance.image.file.content_type,
                size=img_io.getbuffer().nbytes,
                charset=None
            )

            # Set the new image to the instance
            instance.image = new_image

        except Exception as e:
            print(f"Error processing image: {e}")

@receiver(pre_save, sender=CarUpgrade)
def crop_upgarde_image_before_save(sender, instance, **kwargs):
    if instance.image:
        try:
            # Open the image
            img = Image.open(instance.image)
            width, height = img.size
            crop_top_height = 150    # Height in pixels to crop from the top
            crop_bottom_height = 30  # Height in pixels to crop from the bottom
            crop_left_width = 30     # Width in pixels to crop from the left
            crop_right_width = 30    # Width in pixels to crop from the right

            # Calculate the cropping box
            box = (crop_left_width, crop_top_height, width - crop_right_width, height - crop_bottom_height)
            cropped_image = img.crop(box)

            # Save the cropped image to an in-memory file
            img_format = img.format if img.format else 'PNG'
            img_io = io.BytesIO()
            cropped_image.save(img_io, format=img_format)
            img_io.seek(0)

            # Create a new InMemoryUploadedFile
            new_image = InMemoryUploadedFile(
                img_io,
                field_name=instance.image.field.name,
                name=instance.image.name,
                content_type=instance.image.file.content_type,
                size=img_io.getbuffer().nbytes,
                charset=None
            )

            # Set the new image to the instance
            instance.image = new_image

        except Exception as e:
            print(f"Error processing image: {e}")
