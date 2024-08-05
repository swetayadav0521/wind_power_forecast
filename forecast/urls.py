# forecast/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("train/", views.train_model_view, name="train_model"),
    path("predict/", views.predict_from_file_view, name="predict_from_file_view"),
]
