from django.urls import path
from . import views

urlpatterns = [
    # Page Home
    path("", views.homeBase, name="home"),
    path('home/<str:param>', views.home, name='home'),

    # Page autre
    path("contact", views.contact, name="contact us"),
    path("about", views.about, name="about us"),
    

]