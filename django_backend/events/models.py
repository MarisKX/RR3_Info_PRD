# Generic Python imports
import re
# Django imports
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Custom model imports
from cars.models import Car
# Custom functions import
from core.custom_functions.unique_file_path import get_unique_file_path as gufp


class Track(models.Model):
    name = models.CharField(max_length=80)
    display_name = models.CharField(max_length=254, null=False, blank=False)
    location = models.CharField(max_length=254, null=False, blank=False)
    lenght = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the make name
        """
        self.name = re.sub(r'[ /-]', '_', self.display_name).lower()
        super().save(*args, **kwargs)


class TrackConfiguaration(models.Model):
    track = models.ForeignKey('Track', null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    display_name = models.CharField(max_length=254, null=False, blank=False)

    def __str__(self):
        return f"{self.track.display_name} - {self.display_name}"

    def get_display_name(self):
        return self.display_name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the make name
        """
        self.name = re.sub(r'[ /-]', '_', self.display_name).lower()
        super().save(*args, **kwargs)


class EventGroup(models.Model):
    car_group_choices = [
        ('0', 'Motorsports'),
        ('1', 'Road Collection'),
    ]
    section = models.CharField(
        choices=car_group_choices, default='1', max_length=2)
    sequence = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=80)
    display_name = models.CharField(max_length=254, null=False, blank=False)
    available_from_lvl = models.IntegerField(null=False, blank=False)
    image = models.ImageField(upload_to=gufp, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the make name
        """
        self.name = re.sub(r'[ /-]', '_', self.display_name).lower()
        super().save(*args, **kwargs)


class EventSubGroup(models.Model):
    event_group = models.ForeignKey('EventGroup', null=False, blank=False, on_delete=models.CASCADE)
    page = models.IntegerField(null=False, blank=False)
    main_event = models.BooleanField(default=False)
    name = models.CharField(max_length=80)
    repeatable_series = models.BooleanField(default=True)
    display_name = models.CharField(max_length=254, null=False, blank=False)
    featured_cars = models.ManyToManyField(Car, related_name='featured_in_events')
    stages = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)
    image = models.ImageField(upload_to=gufp, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the make name
        """
        self.name = re.sub(r'[ /-]', '_', self.display_name).lower()
        super().save(*args, **kwargs)


class EventSubGroupRewards(models.Model):
    event_subgroup = models.ForeignKey('EventSubGroup', null=False, blank=False, on_delete=models.CASCADE)
    reward_choices = [
        ('0', '25%'),
        ('1', '50%'),
        ('2', '75%'),
        ('3', '100%'),
        ('4', 'Stage 1'),
        ('5', 'Stage 2'),
        ('6', 'Stage 3'),
        ('7', 'Stage 4'),
        ('8', 'Stage 5'),
        ('9', 'Stage 6'),
        ('10', 'Stage 7'),
        ('11', 'Stage 8'),
        ('12', 'Stage 9'),
        ('13', 'Stage 10'),
    ]
    reward_name = models.CharField(
        choices=reward_choices, default='0', max_length=2)
    reward_amount_RS = models.IntegerField(default=0)
    reward_amount_MS = models.IntegerField(default=0)
    reward_amount_Gold = models.IntegerField(default=0)
    image = models.ImageField(upload_to=gufp, blank=True, null=True)


class EventType(models.Model):
    name = models.CharField(max_length=80)
    display_name = models.CharField(max_length=254, null=False, blank=False)
    description = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the make name
        """
        self.name = re.sub(r'[ /-]()', '_', self.display_name).lower()
        super().save(*args, **kwargs)


class Event(models.Model):
    car_group_choices = [
        ('0', 'Motorsports'),
        ('1', 'Road Collection'),
    ]
    section = models.CharField(
        choices=car_group_choices, default='1', max_length=2)
    name = models.CharField(max_length=80)
    display_name = models.CharField(max_length=254, null=False, blank=False)
    special_event = models.BooleanField(default=False)
    description = models.CharField(max_length=500, null=True, blank=True)
    event_group = models.ForeignKey('EventGroup', null=False, blank=False, on_delete=models.CASCADE)
    event_sub_group = models.ForeignKey('EventSubGroup', null=False, blank=False, on_delete=models.CASCADE)
    page = models.IntegerField(null=False, blank=False)
    page_sequence = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(1), MaxValueValidator(5)])
    event_type = models.ForeignKey('EventType', null=False, blank=False, on_delete=models.CASCADE)
    track_and_config = models.ForeignKey('TrackConfiguaration', null=True, blank=True, on_delete=models.CASCADE)
    notes = models.CharField(max_length=100, null=True, blank=True)
    laps = models.IntegerField(null=False, blank=False, default=0)
    min_pr_requirements = models.DecimalField(max_digits=4, decimal_places=1, blank=False, null=False)
    time_required = models.DurationField()
    reward = models.IntegerField(null=False, blank=False)
    currency_choices = [
        ('0', 'MS'),
        ('1', 'RS'),
        ('2', 'Gold'),
        ('3', 'Bonus'),
    ]
    reward_currency = models.CharField(
        choices=currency_choices, default='1', max_length=2)
    clean_race_bonus = models.IntegerField(null=False, blank=False)
    clean_race_bonus_currency = models.CharField(
        choices=currency_choices, default='1', max_length=2)
    reward_image = models.ImageField(upload_to=gufp, blank=True, null=True)
    reward_fame = models.IntegerField(null=False, blank=False)
    fame_image = models.ImageField(upload_to=gufp, blank=True, null=True)
    reward_in_one_minute_spent = models.DecimalField(max_digits=7, decimal_places=1, null=True, blank=True)
    fame_in_one_minute_spent = models.DecimalField(max_digits=8, decimal_places=1, null=True, blank=True)
    image = models.ImageField(upload_to=gufp, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the make name
        and calculate reward and fame per minute.
        """
        # Create a "computer-friendly" name
        base_name = re.sub(r'[() /-]', '_', self.display_name).lower()
        # Combine with page_sequence to ensure uniqueness
        self.name = f"{base_name}_{self.page_sequence}"

        # Calculate total seconds from time_required
        if self.time_required and self.time_required.total_seconds() > 0:
            total_seconds = self.time_required.total_seconds()
            total_minutes = total_seconds / 60

            # Calculate reward and fame per minute
            self.reward_in_one_minute_spent = self.reward / total_minutes
            self.fame_in_one_minute_spent = self.reward_fame / total_minutes
        else:
            # Handle cases where time_required is None or 0
            self.reward_in_one_minute_spent = 0
            self.fame_in_one_minute_spent = 0

        super().save(*args, **kwargs)
