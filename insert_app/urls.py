from django.urls import path
from .views import GetAppData,GetCustomAdData

urlpatterns = [
    path('v1/get_ad_data/<str:package_id>/',GetAppData.as_view(),name = "get_ad_data"),
    path('v1/custom_ad_data/',GetCustomAdData.as_view(),name = "custom_ad_data")
]