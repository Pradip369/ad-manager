from django.shortcuts import render
from PIL import Image
from .helper import get_ad_data
from io import BytesIO
import requests

def home(request):
    return render(request,'ad/home.html')

def banner_app(request):
    context = ''
    try:
        context = get_ad_data(category = 'Banner')
        # Find the image dimensions
        if context:
            if context['ad_data'].ad_image_url:
                response = requests.get('https://github.com/kp-bitcoding/ad-manager/blob/main/AdImages/a4f48a.png?raw=true')
                img = Image.open(BytesIO(response.content))
            # else:
            #     img = Image.open(context['ad_data'].ad_image)
            width = img.width
            height = img.height
            context['height'] = height
            context['width'] = width
    except Exception as e:
        print("errrrrrrrrrrr",e)
        pass
    return render(request,'ad/banner.html',{'data' : context})

def interstitial_ad(request):
    context = get_ad_data(category = 'Interstitial')
    return render(request,'ad/interstitial.html',{'data' : context})