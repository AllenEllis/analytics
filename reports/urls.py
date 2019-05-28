from django.urls import path
from . import views
from django.conf.urls import include


urlpatterns = [
    path('', views.index, name='index'),
    path('nav/', views.nav, name='nav'),
    path('<slug:category>/<slug:name>/', views.report, name='report'),
    path('<slug:category>/<slug:name>/<int:id>', views.report, name='report'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),

]