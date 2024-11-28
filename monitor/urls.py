
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_procesos, name='lista_procesos'),
    path('terminar/<int:pid>/', views.terminar_proceso, name='terminar_proceso')
]