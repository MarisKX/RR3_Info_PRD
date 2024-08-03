from datetime import *

from django.shortcuts import get_object_or_404

from cars.models import Car, Manufacturer
from events.models import EventGroup, Event


def extras(request):

        all_manufacturers = Manufacturer.objects.all().order_by('name')
        all_event_groups_road_collection = EventGroup.objects.filter(section='1').order_by('sequence')
        all_road_cars_count = Car.objects.filter(section='1').count()
        all_motorsports_cars_count = Car.objects.filter(section='0').count()
        all_road_car_events_count = Event.objects.filter(section='1').count()
        all_motorsports_events_count = Event.objects.filter(section='0').count()
        return {
            'all_manufacturers': all_manufacturers,
            'all_event_groups_road_collection': all_event_groups_road_collection,
            'all_road_cars_count': all_road_cars_count,
            'all_motorsports_cars_count': all_motorsports_cars_count,
            'all_road_car_events_count': all_road_car_events_count,
            'all_motorsports_events_count': all_motorsports_events_count,
        }
