from . import views
from django.urls import path

urlpatterns = [
    path('', views.get_list),
    path('search/<str:search_text>/', views.get_search_list),
]
