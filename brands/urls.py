from django.urls import path
from . import views

app_name = 'brands'

urlpatterns = [
    path('create/', views.create_brand, name='create'),
]
