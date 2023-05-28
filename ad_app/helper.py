from .models import CustomAd
from django.db.models import Sum
from random import randint

def get_ad_data(category:str):
    try:
        banner_ad_list = CustomAd.objects.filter(category__cat_name=category)
        total = banner_ad_list.aggregate(sum_of_pr = Sum('priority'))['sum_of_pr']
        random_no = randint(0,total)
        iter_pr = 0
        for ad in banner_ad_list:
            if random_no >= iter_pr and random_no <= (ad.priority + iter_pr):
                context = {'ad_data' : ad}
                return context
            iter_pr += ad.priority
        return False
    except Exception as e:
        print(e)
        return False