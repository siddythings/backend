from django.urls import path
from core import views


urlpatterns = [
    path("check-number-plate/", views.CheckNumberPlateView.as_view(), name="core-check-number-plate"),
]
