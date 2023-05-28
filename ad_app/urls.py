from django.urls import  path
from .views import home,interstitial_ad,banner_app

urlpatterns = [
    path('',home,name = 'home'),
    path('interstitial_ad/',interstitial_ad,name = "interstitial_ad"),
    path('banner_ad/',banner_app,name = "banner_app"),
]