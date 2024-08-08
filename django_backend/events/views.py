from django.shortcuts import render, get_object_or_404
from .models import (
    EventGroup,
    EventSubGroup,
    EventType,
    Event,
    EventSubGroupRewards,
    )
from cars.models import Car


def road_collection_groups(request):
    """Render the road collection groups page (Amateur, Pro/Am etc)"""
    road_collection_groups = EventGroup.objects.filter(section='1').order_by('sequence')
    road_collection_subgroups = EventSubGroup.objects.filter(event_group__section='1')
    context = {
        'road_collection_groups': road_collection_groups,
        'road_collection_subgroups': road_collection_subgroups,
    }
    return render(request, 'events/road_collection_groups.html', context)

def road_collection_subgroups(request, id):
    """Render the road collection subgroups page (Pure Stock Challenge etc.)"""
    road_collection_subgroups = EventSubGroup.objects.filter(event_group=id).order_by('page', '-main_event')
    road_collection_events = Event.objects.filter(section='1').order_by('event_group', 'event_sub_group', 'page', 'page_sequence')
    road_collection_group = get_object_or_404(EventGroup, id=id)

    subgroup_rewards = EventSubGroupRewards.objects.filter(event_subgroup__in=road_collection_subgroups).order_by('reward_name')

    # Collect all featured cars from subgroups
    featured_cars = Car.objects.filter(featured_in_events__in=road_collection_subgroups).distinct()

    context = {
        'subgroup_rewards': list(subgroup_rewards),
        'featured_cars': list(featured_cars),
        'road_collection_events': road_collection_events,
        'road_collection_subgroups': road_collection_subgroups,
        'road_collection_group': road_collection_group
    }
    return render(request, 'events/road_collection_subgroups.html', context)

def road_collection_events(request, id):
    """Render the road collection events page (Nissan Silvia Time Trial etc.)"""
    road_collection_events = Event.objects.filter(section='1', event_sub_group=id).order_by('page', 'page_sequence')
    road_collection_subgroup = get_object_or_404(EventSubGroup, id=id)
    context = {
        'road_collection_events': road_collection_events,
        'road_collection_subgroup': road_collection_subgroup,
    }
    return render(request, 'events/road_collection_events.html', context)

def road_collection_event_details(request, id):
    """Render the road collection event details page"""
    road_collection_event = get_object_or_404(Event, id=id)
    event_subgroup = road_collection_event.event_sub_group
    featured_cars = event_subgroup.featured_cars.all()
    context = {
        'road_collection_event': road_collection_event,
        'featured_cars': featured_cars,
    }
    return render(request, 'events/road_collection_event_details.html', context)
