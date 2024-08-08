import boto3
from django.core.management.base import BaseCommand
from django.conf import settings
from events.models import EventGroup, EventSubGroup, EventSubGroupRewards, Event
from cars.models import Car, OfficialColors, CarUpgrade


class Command(BaseCommand):
    help = 'List of images in use with additional information'

    def handle(self, *args, **kwargs):
        current_images_group = []
        current_images_subgroup = []
        current_images_subgroup_rewards = []
        current_images_events = []
        current_images_cars = []
        current_images_official_colors = []
        current_images_car_upgrade = []

        for group in EventGroup.objects.all():
            if group.image:
                # Remove the 'uploads/' prefix from the filename
                cleaned_filename = group.image.name.replace('uploads/', '')
                current_images_group.append({
                    'filename': cleaned_filename,
                    'event_group': group.display_name,
                })

        for subgroup in EventSubGroup.objects.all():
            if subgroup.image:
                # Remove the 'uploads/' prefix from the filename
                cleaned_filename = subgroup.image.name.replace('uploads/', '')
                current_images_subgroup.append({
                    'filename': cleaned_filename,
                    'event_sub_group': subgroup.display_name,
                })

        for reward in EventSubGroupRewards.objects.all():
            if reward.image:
                # Remove the 'uploads/' prefix from the filename
                cleaned_filename = reward.image.name.replace('uploads/', '')
                current_images_subgroup_rewards.append({
                    'filename': cleaned_filename,
                    'event_sub_group_reward': reward.get_reward_name_display(),
                    'event_sub_group': reward.event_subgroup.display_name,
                })

        for event in Event.objects.all():
            if event.reward_image or event.fame_image:
                # Remove the 'uploads/' prefix from the filename
                cleaned_filename_reward = event.reward_image.name.replace('uploads/', '')
                cleaned_filename_fame = event.fame_image.name.replace('uploads/', '')
                current_images_events.append({
                    'filename': cleaned_filename_reward,
                    'event_sub_group': event.event_sub_group.display_name,
                    'event': event.display_name,
                    'event_sequence': f"{event.page} - {event.page_sequence}"
                })
                current_images_events.append({
                    'filename': cleaned_filename_fame,
                    'event_sub_group': event.event_sub_group.display_name,
                    'event': event.display_name,
                    'event_sequence': f"{event.page} - {event.page_sequence}"
                })

        for car in Car.objects.all():
            if car.image:
                # Remove the 'uploads/' prefix from the filename
                cleaned_filename_car = car.image.name.replace('uploads/', '')
                current_images_cars.append({
                    'filename': cleaned_filename_car,
                    'car': f"{car.manufacturer.display_name} - {car.model}"
                })

        for official_color in OfficialColors.objects.all():
            if official_color.image:
                # Remove the 'uploads/' prefix from the filename
                cleaned_filename = official_color.image.name.replace('uploads/', '')
                current_images_official_colors.append({
                    'filename': cleaned_filename,
                    'car': f"{official_color.car.manufacturer.display_name} - {official_color.car.model}"
                })

        for upgrade in CarUpgrade.objects.all():
            if upgrade.image:
                # Remove the 'uploads/' prefix from the filename
                cleaned_filename = upgrade.image.name.replace('uploads/', '')
                current_images_car_upgrade.append({
                    'filename': cleaned_filename,
                    'car': f"{upgrade.car.manufacturer.display_name} - {upgrade.car.model}",
                    'upgrade': upgrade.upgrade,
                })

        # Sort the list of images by filename
        current_images_group.sort(key=lambda x: x['filename'])
        current_images_subgroup.sort(key=lambda x: x['filename'])
        current_images_subgroup_rewards.sort(key=lambda x: x['filename'])
        current_images_events.sort(key=lambda x: x['filename'])
        current_images_cars.sort(key=lambda x: x['filename'])
        current_images_official_colors.sort(key=lambda x: x['filename'])
        current_images_car_upgrade.sort(key=lambda x: x['filename'])

        # Print each image detail
        print("#####################################################")
        print("Event section")
        print("Group: ")
        for image_info in current_images_group:
            print(f"{image_info['filename']}, EventGroup: {image_info['event_group']}")

        # Print each image detail
        print("SubGroup: ")
        for image_info in current_images_subgroup:
            print(f"{image_info['filename']}, EventSubGroup: {image_info['event_sub_group']}")

        # Print each image detail
        print("Rewards: ")
        for image_info in current_images_subgroup_rewards:
            print(f"{image_info['filename']}, EventSubGroupReward: {image_info['event_sub_group_reward']}, EventSubGroup: {image_info['event_sub_group']}")

        # Print each image detail
        print("Events: ")
        for image_info in current_images_events:
            print(f"{image_info['filename']}, EventSubGroup: {image_info['event_sub_group']}, Event: {image_info['event']}, Event Sequence: {image_info['event_sequence']}")

        print("#####################################################")
        print("Car section")
        # Print each image detail
        print("Cars: ")
        for image_info in current_images_cars:
            print(f"{image_info['filename']}, Car: {image_info['car']}")

        print("Official Colors: ")
        for image_info in current_images_official_colors:
            print(f"{image_info['filename']}, Car: {image_info['car']}")

        print("Upgrades: ")
        for image_info in current_images_car_upgrade:
            print(f"{image_info['filename']}, Car: {image_info['car']}, Upgrade: {image_info['upgrade']}")
