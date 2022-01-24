from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from vehicles.views import VehicleListView, VehicleDetailView

urlpatterns = [
    path("vehicles/", VehicleListView.as_view(), name="vehicle-list"),
    path("vehicles/<int:id>/", VehicleDetailView.as_view(), name="vehicle-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
