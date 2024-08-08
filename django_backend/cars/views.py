from django.shortcuts import render, get_object_or_404
from .models import (
    Manufacturer,
    Car,
    OfficialColors,
    CarUpgrade,
    )
from events.models import EventSubGroup, Event


def all_road_collection_cars(request):
    """Render the cars page"""
    all_road_collection_cars = Car.objects.filter(section='1').order_by('manufacturer__display_name', 'model')
    context = {
        'all_road_collection_cars': all_road_collection_cars
    }
    return render(request, 'cars/all_road_collection_cars.html', context)


def road_collection_cars_by_manufacturer(request, id):
    """Render the cars page by manufacturer"""
    road_collection_cars_by_manufacturer = Car.objects.filter(section='1', manufacturer=id).order_by('model')
    manufacturer = get_object_or_404(Manufacturer, id=id)
    context = {
        'road_collection_cars_by_manufacturer': road_collection_cars_by_manufacturer,
        'manufacturer': manufacturer
    }
    return render(request, 'cars/road_collection_cars_by_manufacturer.html', context)


def road_collection_car(request, id):
    """Render the car details"""
    road_collection_car = get_object_or_404(Car, id=id)
    official_colors = OfficialColors.objects.filter(car=road_collection_car).order_by('id')
    event_subgroups = EventSubGroup.objects.filter(featured_cars=road_collection_car).order_by('page', '-main_event')
    upgrades = CarUpgrade.objects.filter(car=road_collection_car).order_by('upgrade__upgrade_type', 'upgrade_sequence', )
    context = {
        'road_collection_car': road_collection_car,
        'official_colors': official_colors,
        'event_subgroups': event_subgroups,
        'upgrades': upgrades,
    }
    return render(request, 'cars/road_collection_car.html', context)
