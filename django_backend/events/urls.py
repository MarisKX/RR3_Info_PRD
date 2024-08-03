from django.urls import path
from . import views

urlpatterns = [
    path('road_collection_groups/', views.road_collection_groups, name="road_collection_groups"),
    path('road_collection_subgroups/<id>/', views.road_collection_subgroups, name="road_collection_subgroups"),
    path('road_collection_events/<id>/', views.road_collection_events, name="road_collection_events"),
    path('road_collection_event_details/<id>/', views.road_collection_event_details, name="road_collection_event_details"),
]