from rest_framework.generics import RetrieveAPIView,ListAPIView
from .models import BaseApp
from .serializers import BaseAppSerializer,GetCustomAdDataSerializer
from ad_app.models import CustomAd

class GetAppData(RetrieveAPIView):
    queryset = BaseApp.objects.all()
    serializer_class = BaseAppSerializer
    lookup_field = 'package_id'

class GetCustomAdData(ListAPIView):
    queryset = CustomAd.objects.all()
    serializer_class = GetCustomAdDataSerializer