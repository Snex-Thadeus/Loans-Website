from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name="about"),
    path('services', views.services, name="services"),
    path('apply', views.apply, name="apply"),
    path('loan', views.loan, name="loan"),
]
