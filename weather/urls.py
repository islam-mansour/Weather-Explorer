from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<city>', views.detail, name='detail'),
    path('remove/<city>', views.remove, name='remove')
]
