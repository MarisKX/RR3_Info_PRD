from django.contrib import admin
from .models import (
    Manufacturer,
    Car,
    OfficialColors,
    Upgrades,
    CarUpgrade,
    )


class CarUpgradeAdmin(admin.TabularInline):
    model = CarUpgrade
    list_display = (
        'upgrade',
        'upgrade_sequence',
        'upgrade_option1_price',
        'upgrade_option1_currency',
        'upgrade_option2_price',
        'upgrade_option2_currency',
        'upgrade_time',
    )
    ordering = ('upgrade__upgrade_type', 'upgrade_sequence', )


class UpgradesAdmin(admin.ModelAdmin):
    list_display = (
        'upgrade_type_display',
        'upgrade_heading',
        'upgrade_description',
    )
    ordering = ('upgrade_type', 'upgrade_heading', )

    def upgrade_type_display(self, obj):
        return obj.get_upgrade_type_display()
    upgrade_type_display.short_description = 'Upgrade Type'


class OfficialColorsAdmin(admin.TabularInline):
    model = OfficialColors


class ManufacturerAdmin(admin.ModelAdmin):
    readonly_fields = ('name', )
    list_display = (
        'display_name',
        'name',
    )


class CarAdmin(admin.ModelAdmin):
    inlines = (CarUpgradeAdmin, OfficialColorsAdmin, )
    list_display = (
        'manufacturer',
        'model',
        'section',
        'default_price',
        'currency',
        'delivery_time',
        'upgrades_total_R',
        'upgrades_total_M',
        'upgrades_total_G',
        'upgrades_total_G_optional',
        'full_info',
    )
    ordering = ('manufacturer__display_name', 'model',)

    def get_manufacturer_name(self, obj):
        return obj.manufacturer.display_name
    get_manufacturer_name.admin_order_field = 'manufacturer__display_name'
    get_manufacturer_name.short_description = 'Manufacturer'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['manufacturer'].queryset = Manufacturer.objects.order_by('display_name')
        return form


admin.site.register(Upgrades, UpgradesAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Car, CarAdmin)
