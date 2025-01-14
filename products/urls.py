from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.product_list, name='list'),
    path('create/', views.create_product, name='create'),
    path('detail/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.product_detail, name='detail'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('review/<int:pk>/', views.create_review, name='create_review'),  # Corrected URL
]
