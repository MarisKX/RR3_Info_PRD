from django.shortcuts import render
# Custom model imports
from cars.models import Car
from events.models import (
    Event,
    EventGroup,
    EventType,
    EventSubGroup,
)


# Index (home) view
def index(request):
    """ A view to return the index page """
    # Road collcetion Car stats
    road_collection_fastest_car_by_top_speed = Car.objects.filter(section="1").order_by('-max_top_speed')[:10]
    road_collection_fastest_car_by_acceleration = Car.objects.filter(section="1").order_by('max_acceleration')[:10]
    road_collection_highest_max_pr = Car.objects.filter(section="1").order_by('-max_pr_score')[:10]
    road_collection_most_expensive_repair = Car.objects.filter(section="1").order_by('-repair_price')[:10]
    road_collection_most_expensive_purchase_R = Car.objects.filter(section="1", currency="1").order_by('-default_price')[:10]
    road_collection_most_expensive_purchase_G = Car.objects.filter(section="1", currency="2").order_by('-default_price')[:10]
    road_collection_most_expensive_upgrades_R = Car.objects.filter(section="1").order_by('-upgrades_total_R')[:10]
    road_collection_most_expensive_upgrades_G = Car.objects.filter(section="1").order_by('-upgrades_total_G')[:10]
    # Road collcetion Events stats
    road_collection_highest_rs_reward = Event.objects.filter(section="1").exclude(special_event=True).order_by('-reward')[:20]
    road_collection_highest_fame_reward = Event.objects.filter(section="1").exclude(special_event=True).order_by('-reward_fame')[:20]
    context = {
        # Road collcetion cars stats
        'road_collection_fastest_car_by_top_speed': road_collection_fastest_car_by_top_speed,
        'road_collection_fastest_car_by_acceleration': road_collection_fastest_car_by_acceleration,
        'road_collection_highest_max_pr': road_collection_highest_max_pr,
        'road_collection_most_expensive_repair': road_collection_most_expensive_repair,
        'road_collection_most_expensive_purchase_R': road_collection_most_expensive_purchase_R,
        'road_collection_most_expensive_purchase_G': road_collection_most_expensive_purchase_G,
        'road_collection_most_expensive_upgrades_R': road_collection_most_expensive_upgrades_R,
        'road_collection_most_expensive_upgrades_G': road_collection_most_expensive_upgrades_G,
        # Road collcetion events stats
        'road_collection_highest_rs_reward': road_collection_highest_rs_reward,
        'road_collection_highest_fame_reward': road_collection_highest_fame_reward,
    }

    return render(request, 'core/index.html', context)