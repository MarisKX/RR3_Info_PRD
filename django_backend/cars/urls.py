"""
URL mapping for the publish app.
"""
from django.urls import path
from cars import views


urlpatterns = [
  path('road_collection', views.all_road_collection_cars, name='all_road_collection_cars'),
  path('road_collection/<id>/',
       views.road_collection_cars_by_manufacturer,
       name="road_collection_manufacturer"
      ),
  path('car/<id>', views.road_collection_car, name='road_collection_car'),
]
