from PIL import Image
import io
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Event, EventSubGroup, EventSubGroupRewards

def process_image(image_field, crop_top, crop_bottom, crop_left, crop_right):
    """
    Process the image by resizing and cropping.
    """
    try:
        # Open the image
        img = Image.open(image_field)

        # Resize the image to half its original size
        resize_factor = 0.5  # Resize to half the size
        new_width = int(img.width * resize_factor)
        new_height = int(img.height * resize_factor)
        resized_image = img.resize((new_width, new_height), Image.LANCZOS)

        # Set the resized image as the current image to be cropped
        img = resized_image

        # Now crop the resized image
        width, height = img.size
        crop_top_height = int(crop_top * resize_factor)    # Adjust cropping values
        crop_bottom_height = int(crop_bottom * resize_factor)
        crop_left_width = int(crop_left * resize_factor)
        crop_right_width = int(crop_right * resize_factor)

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
            field_name=image_field.field.name,
            name=image_field.name,
            content_type=image_field.file.content_type,
            size=img_io.getbuffer().nbytes,
            charset=None
        )

        return new_image
    except Exception as e:
        print(f"Error processing image: {e}")
        return image_field  # Return the original image if processing fails

@receiver(pre_save, sender=EventSubGroup)
def process_event_subgroup_image_before_save(sender, instance, **kwargs):
    if instance.image:
        print("Processing EventSubGroup image...")  # Debug
        instance.image = process_image(instance.image, crop_top=1, crop_bottom=1, crop_left=1, crop_right=1)
        print("EventSubGroup Image processing complete.")  # Debug

@receiver(pre_save, sender=EventSubGroupRewards)
def process_event_subgroup_rewards_image_before_save(sender, instance, **kwargs):
    if instance.image and instance.event_subgroup.repeatable_series:
        print("Processing EventSubGroupRewards image...")  # Debug
        instance.image = process_image(instance.image, crop_top=420, crop_bottom=445, crop_left=490, crop_right=490)
        print("EventSubGroupRewards Image processing complete.")  # Debug

@receiver(pre_save, sender=Event)
def process_event_rewards_image_before_save(sender, instance, **kwargs):
    if instance.reward_image:
        print("Processing Reward image...")  # Debug
        instance.reward_image = process_image(instance.reward_image, crop_top=150, crop_bottom=100, crop_left=50, crop_right=50)
        print("Reward Image processing complete.")  # Debug

    if instance.fame_image:
        print("Processing Fame image...")  # Debug
        instance.fame_image = process_image(instance.fame_image, crop_top=150, crop_bottom=100, crop_left=50, crop_right=50)
        print("Fame Image processing complete.")  # Debug
