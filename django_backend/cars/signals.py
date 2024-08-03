from PIL import Image
import io
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError
from .models import CarUpgrade, OfficialColors, Car

@receiver(post_save, sender=CarUpgrade)
def update_car_upgrades_total_on_save(sender, instance, **kwargs):
    instance.car.update_upgrades_total()

@receiver(post_delete, sender=CarUpgrade)
def update_car_upgrades_total_on_delete(sender, instance, **kwargs):
    instance.car.update_upgrades_total()

@receiver(pre_save, sender=Car)
def process_car_image_before_save(sender, instance, **kwargs):
    if instance.image:
        try:
            print("Processing Car image...")  # Debug
            # Open the image
            img = Image.open(instance.image)

            # Resize the image to half its original size
            resize_factor = 0.5  # Resize to half the size
            new_width = int(img.width * resize_factor)
            new_height = int(img.height * resize_factor)
            resized_image = img.resize((new_width, new_height), Image.LANCZOS)

            # Set the resized image as the current image to be cropped
            img = resized_image

            # Now crop the resized image
            width, height = img.size
            crop_top_height = int(1 * resize_factor)    # Adjust cropping values
            crop_bottom_height = int(1 * resize_factor)
            crop_left_width = int(1 * resize_factor)
            crop_right_width = int(1 * resize_factor)

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
            print("Image processing complete.")  # Debug

        except Exception as e:
            print(f"Error processing image: {e}")

@receiver(pre_save, sender=OfficialColors)
def process_oe_color_image_before_save(sender, instance, **kwargs):
    if instance.image:
        try:
            print("Processing OfficialColors image...")  # Debug
            # Open the image
            img = Image.open(instance.image)

            # Resize the image to half its original size
            resize_factor = 0.5  # Resize to half the size
            new_width = int(img.width * resize_factor)
            new_height = int(img.height * resize_factor)
            resized_image = img.resize((new_width, new_height), Image.LANCZOS)

            # Set the resized image as the current image to be cropped
            img = resized_image

            # Now crop the resized image
            width, height = img.size
            crop_top_height = int(150 * resize_factor)  # Adjust cropping values
            crop_bottom_height = int(50 * resize_factor)

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
            print("Image processing complete.")  # Debug

        except Exception as e:
            print(f"Error processing image: {e}")

@receiver(pre_save, sender=CarUpgrade)
def process_upgrade_image_before_save(sender, instance, **kwargs):
    if instance.image:
        try:
            print("Processing CarUpgrade image...")  # Debug
            # Open the image
            img = Image.open(instance.image)

            # Resize the image to half its original size
            resize_factor = 0.5  # Resize to half the size
            new_width = int(img.width * resize_factor)
            new_height = int(img.height * resize_factor)
            resized_image = img.resize((new_width, new_height), Image.LANCZOS)

            # Set the resized image as the current image to be cropped
            img = resized_image

            # Now crop the resized image
            width, height = img.size
            crop_top_height = int(580 * resize_factor)    # Adjust cropping values
            crop_bottom_height = int(355 * resize_factor)
            crop_left_width = int(255 * resize_factor)
            crop_right_width = int(255 * resize_factor)

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
            print("Image processing complete.")  # Debug

        except Exception as e:
            print(f"Error processing image: {e}")
