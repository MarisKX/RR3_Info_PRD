from django.db import models
from django.db.models import Sum, Q
from core.custom_functions.unique_file_path import get_unique_file_path as gufp
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class Manufacturer(models.Model):

    name = models.CharField(max_length=80)
    display_name = models.CharField(max_length=254, null=False, blank=False)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the make name
        """
        self.name = self.display_name.replace(" ", "_").lower()
        super().save(*args, **kwargs)


class Upgrades(models.Model):

    class Meta:
        verbose_name_plural = 'Upgrades'

    upgrade_type_choices = [
        ('0', 'Engine'),
        ('1', 'Drivetrain'),
        ('2', 'Body'),
        ('3', 'Suspension'),
        ('4', 'Exhaust'),
        ('5', 'Brakes'),
        ('6', 'Tires & Wheels'),
    ]
    upgrade_type = models.CharField(
        max_length=1, choices=upgrade_type_choices, default='0')
    upgrade_heading = models.CharField(max_length=120)
    upgrade_description = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.get_upgrade_type_display()} - {self.upgrade_heading}"

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the upgrade heading
        """
        self.upgrade_heading = self.upgrade_heading.upper()
        super().save(*args, **kwargs)


class Car(models.Model):

    manufacturer = models.ForeignKey('Manufacturer', null=False, blank=False, on_delete=models.CASCADE)
    model = models.CharField(max_length=120)
    section_choices = [
        ('0', 'Motorsports'),
        ('1', 'Road Collection'),
    ]
    section = models.CharField(
        max_length=1,
        choices=section_choices,
        default='1')
    default_price = models.IntegerField(null=False, blank=False)
    discount_price = models.IntegerField(null=False, blank=False)
    currency_choices = [
        ('0', 'MS'),
        ('1', 'RS'),
        ('2', 'Gold'),
        ('3', 'Bonus'),
    ]
    currency = models.CharField(
        max_length=1,
        choices=currency_choices,
        default='1')
    delivery_time = models.DurationField()
    baseclass_choices = [
        ('0', 'P'),
        ('1', 'S'),
        ('2', 'R'),
    ]
    baseclass = models.CharField(
        max_length=1,
        choices=baseclass_choices,
        default='0')
    eng_drive_choices = [
        ('0', 'FF'),
        ('1', 'FR'),
        ('2', 'RR'),
        ('3', 'MR'),
        ('4', 'F4'),
        ('5', 'R4'),
        ('6', 'M4'),
    ]
    eng_drive = models.CharField(
        max_length=1,
        choices=eng_drive_choices,
        default='0')
    init_top_speed = models.DecimalField(max_digits=4, decimal_places=1, blank=False, null=False)
    max_top_speed = models.DecimalField(max_digits=4, decimal_places=1, blank=False, null=False)
    init_acceleration = models.DecimalField(max_digits=4, decimal_places=2, blank=False, null=False)
    max_acceleration = models.DecimalField(max_digits=4, decimal_places=2, blank=False, null=False)
    init_braking_distance = models.DecimalField(max_digits=3, decimal_places=1, blank=False, null=False)
    max_braking_distance = models.DecimalField(max_digits=3, decimal_places=1, blank=False, null=False)
    official_braking_distance = models.BooleanField(default=True)
    init_cornering = models.DecimalField(max_digits=3, decimal_places=2, blank=False, null=False)
    max_cornering = models.DecimalField(max_digits=3, decimal_places=2, blank=False, null=False)
    init_pr_score = models.DecimalField(max_digits=4, decimal_places=1, blank=False, null=False)
    max_pr_score = models.DecimalField(max_digits=4, decimal_places=1, blank=False, null=False)
    repair_time = models.DurationField()
    repair_price = models.IntegerField(null=False, blank=False)
    repair_currency = models.CharField(
        max_length=1,
        choices=currency_choices,
        default='1')
    upgrades_total_R = models.IntegerField(null=False, blank=False, default=0)
    upgrades_total_M = models.IntegerField(null=False, blank=False, default=0)
    upgrades_total_G = models.IntegerField(null=False, blank=False, default=0)
    upgrades_total_G_optional = models.IntegerField(null=False, blank=False, default=0)
    image = models.ImageField(upload_to=gufp, blank=True, null=True)
    full_info = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.manufacturer.display_name.upper()} {self.model}"

    def update_upgrades_total(self):
        """
        Update total upgrade costs each time a new upgrade is added.
        """
        self.upgrades_total_R = self.upgrade.aggregate(
            total_R=Sum('upgrade_option1_price', filter=Q(upgrade_option1_currency='1'))
        )['total_R'] or 0
        self.upgrades_total_M = self.upgrade.aggregate(
            total_M=Sum('upgrade_option1_price', filter=Q(upgrade_option1_currency='0'))
        )['total_M'] or 0
        self.upgrades_total_G = self.upgrade.aggregate(
            total_G=Sum('upgrade_option2_price', filter=Q(upgrade_option2_currency='2', upgrade_option1_price=0))
        )['total_G'] or 0
        self.upgrades_total_G_optional = self.upgrade.aggregate(
            total_G=Sum('upgrade_option2_price', filter=Q(upgrade_option2_currency='2'))
        )['total_G'] or 0
        self.save()


class OfficialColors(models.Model):
    """List of occicial colors of the car"""
    car = models.ForeignKey('Car', null=False, blank=False, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=gufp, blank=True, null=True)


class CarUpgrade(models.Model):

    class Meta:
        verbose_name_plural = 'Car Upgrades'

    car = models.ForeignKey('Car', null=False, blank=False, on_delete=models.CASCADE, related_name='upgrade')
    upgrade = models.ForeignKey('Upgrades', null=False, blank=False, on_delete=models.CASCADE)
    upgrade_sequence = models.IntegerField(null=False, blank=False)
    improvement_top_speed = models.DecimalField(max_digits=3, decimal_places=1, blank=False, null=False)
    improvement_acceleration = models.DecimalField(max_digits=4, decimal_places=3, blank=False, null=False)
    improvement_braking_distance = models.DecimalField(max_digits=3, decimal_places=1, blank=False, null=False)
    improvement_cornering = models.DecimalField(max_digits=4, decimal_places=3, blank=False, null=False)
    improvement_pr = models.DecimalField(max_digits=3, decimal_places=1, blank=False, null=False)
    upgrade_option1_price = models.IntegerField(null=False, blank=False)
    currency_choices = [
        ('0', 'MS'),
        ('1', 'RS'),
        ('2', 'Gold'),
        ('3', 'Bonus'),
    ]
    upgrade_option1_currency = models.CharField(
        max_length=1,
        choices=currency_choices,
        default='1')
    upgrade_option2_price = models.IntegerField(null=False, blank=False)
    upgrade_option2_currency = models.CharField(
        max_length=1,
        choices=currency_choices,
        default='2')
    upgrade_time = models.DurationField()
    image = models.ImageField(upload_to=gufp, blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the car upgrade
        """
        super().save(*args, **kwargs)
