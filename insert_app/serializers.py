from dataclasses import field
from rest_framework import serializers
from .models import *
from ad_app.models import CustomAd as AdAppCustomAd     # This is comming from `ad_app` application's `models.py`

class AdMobAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdMobAd
        exclude = ('base_app','id')

class GoogleAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleAd
        exclude = ('admob_ad','id')

class UnityAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnityAd
        exclude = ('admob_ad','id')

class CustomAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomAd
        exclude = ('admob_ad','id')

class AppUpdateInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUpdateInformation
        exclude = ('base_app','id')

class AboutAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutApp
        exclude = ('base_app','id')

class RateAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateApp
        exclude = ('base_app','id')

class MoreAppsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoreApps
        exclude = ('base_app','id')

class ShareAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareApp
        exclude = ('base_app','id')

class OfficialWebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficialWebsite
        exclude = ('base_app','id')

class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        exclude = ('base_app','id')

class TermsOfUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsOfUse
        exclude = ('base_app','id')

class SplashScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = SplashScreen
        exclude = ('base_app','id')

class FeedbackSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackSupport
        exclude = ('base_app','id')

class AppSettingsSerializer(serializers.ModelSerializer):
    app_settings = serializers.JSONField()
    class Meta:
        model = AppSettings
        fields = ('app_settings',)

class BaseAppSerializer(serializers.ModelSerializer):
    admob_settings = serializers.SerializerMethodField()
    app_update_information = AppUpdateInformationSerializer(source='app_information')
    about_app = AboutAppSerializer(source = 'app_about')
    rate_app = RateAppSerializer(source = 'app_rate')
    more_apps = MoreAppsSerializer(source = 'app_more')
    share_app = ShareAppSerializer(source = 'app_share')
    official_website = OfficialWebsiteSerializer(source = 'app_official')
    privacy_policy = PrivacyPolicySerializer(source = 'app_privacy_policy')
    terms_of_use = TermsOfUseSerializer(source = 'app_terms')
    splash_screen = SplashScreenSerializer(source = 'app_splash_screen')
    feedback_support = FeedbackSupportSerializer(source = 'app_feedback')
    app_setting = AppSettingsSerializer(source = 'app_settings')

    class Meta:
        model = BaseApp
        fields = ('id','title','package_id','thumbnail','description',
                    'ads_loading_text','ads_loading_delay','is_banner_ads',
                    'is_interstitial_ads','created_date','admob_settings',
                    'app_update_information','about_app','rate_app','more_apps',
                    'share_app','official_website','privacy_policy',
                    'terms_of_use','splash_screen','feedback_support','app_setting')

    def get_admob_settings(self, obj):
        ad_mob = AdMobAdSerializer(obj.base_admob_ad).data
        google_ad = GoogleAdSerializer(obj.admob_google_ad).data
        unity_ads = UnityAdSerializer(obj.admob_unity_ad).data
        custom_ads = CustomAdSerializer(obj.admob_custom_ad).data

        data = {
                **ad_mob,
                'google_ads' : google_ad,
                'unity_ads' : unity_ads,
                'custom_ads' : custom_ads
            }
        
        return data

class GetCustomAdDataSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='cat_name',read_only=True)

    class Meta:
        model = AdAppCustomAd
        fields = ('ad_title','category','ad_image_url','redirect_url','priority','cr_date')