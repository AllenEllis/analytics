from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nav/', views.nav, name='nav'),
    path('<slug:category>/<slug:name>/', views.report, name='report'),
    path('<slug:category>/<slug:name>/<int:id>', views.report, name='report'),
]