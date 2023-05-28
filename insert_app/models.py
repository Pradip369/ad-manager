import json
from pyexpat import model
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

class BaseApp(models.Model):
    title = models.CharField(max_length=200,help_text="Application title",unique=True)
    package_id = models.CharField(max_length=250,unique=True)
    thumbnail = models.URLField(null = True,blank=True,verbose_name="Thubnail url")
    description = models.TextField()
    ads_loading_text = models.CharField(max_length=250)
    ads_loading_delay = models.IntegerField(help_text="Loading delay in milli-seconds")
    is_banner_ads = models.BooleanField(default=False)
    is_interstitial_ads = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "%s (%s)" %(self.title,self.package_id)

    def app_thumb_tag(self):
        if self.thumbnail:
            return mark_safe('<img src="%s" height="100px" width="100px"/>' % (self.thumbnail))
    app_thumb_tag.short_description = 'App thumbnail'

class AdMobAd(models.Model):
    base_app = models.OneToOneField(to = BaseApp,on_delete=models.CASCADE,related_name="base_admob_ad")
    ads_loading_text = models.CharField(max_length=60)
    ads_loading_delay = models.IntegerField(help_text="Loading delay in milli-seconds")
    is_banner_ads = models.BooleanField(default=False)
    is_interstitial_ads = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "%s" %(self.id)

class GoogleAd(models.Model):
    admob_ad = models.OneToOneField(to = BaseApp,on_delete=models.CASCADE,related_name="admob_google_ad")
    ads_app_id_ios = models.CharField(max_length=250)
    ads_app_id_android = models.CharField(max_length=250)
    banner_ad_unit_id_ios = models.CharField(max_length=250)
    banner_ad_unit_id_android = models.CharField(max_length=250)
    interstitial_ad_unit_id_ios = models.CharField(max_length=250)
    interstitial_ad_unit_id_android = models.CharField(max_length=250)
    app_open_ad_unit_id_android = models.CharField(max_length=150)
    app_open_ad_unit_id_ios = models.CharField(max_length=150)
    native_ads_unit_id_android = models.CharField(max_length=150)
    is_banner_ads = models.BooleanField(default=False)
    is_open_ads = models.BooleanField(default=False)
    is_interstitial_ads = models.BooleanField(default=False)
    is_native_ads = models.BooleanField(default=False)
    visibility_percentage = models.IntegerField(help_text="Visibility Percentage in %")

    def __str__(self) -> str:
        return "%s" %(self.id)

class UnityAd(models.Model):
    admob_ad = models.OneToOneField(to = BaseApp,on_delete=models.CASCADE,related_name="admob_unity_ad")
    ads_app_id_ios = models.CharField(max_length=200)
    ads_app_id_android = models.CharField(max_length=200)
    is_banner_ads = models.BooleanField(default=False)
    is_interstitial_ads = models.BooleanField(default=False)
    visibility_percentage = models.IntegerField(help_text="Visibility Percentage in %")

    def __str__(self) -> str:
        return "%s" %(self.id)

class CustomAd(models.Model):
    admob_ad = models.OneToOneField(to = BaseApp,on_delete=models.CASCADE,related_name="admob_custom_ad")
    is_banner_ads = models.BooleanField(default=False)
    is_interstitial_ads = models.BooleanField(default=False)
    visibility_percentage = models.IntegerField(help_text="Visibility Percentage in %")
    banner_ads_url = models.URLField()
    interstitial_ads_url = models.URLField()
    all_custom_ad_url = models.URLField(null=True)

    def __str__(self) -> str:
        return "%s" %(self.id)

class AppUpdateInformation(models.Model):
    base_app = models.OneToOneField(to = BaseApp,on_delete=models.CASCADE,related_name="app_information")
    is_popup_dialog = models.BooleanField(default=False)
    download_url = models.URLField()
    website_url = models.URLField()
    updated_version_code = models.IntegerField()
    filename = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    default_message = models.CharField(max_length=50)
    log_message = models.TextField()

    def __str__(self) -> str:
        return "%s" %(self.id)

class AboutApp(models.Model):
    base_app = models.OneToOneField(to = BaseApp,on_delete=models.CASCADE,related_name="app_about")
    is_about_app = models.BooleanField(default=False)
    about_title = models.CharField(max_length=70)
    about_message = models.TextField()

    def __str__(self) -> str:
        return "%s" %(self.id)

class RateApp(models.Model):
    base_app = models.OneToOneField(to = BaseApp,on_delete=models.CASCADE,related_name="app_rate")
    is_rate_app = models.BooleanField(default=False)
    package_id = models.CharField(max_length=50)
    rate_app_url = models.URLField()
    rate_message = models.TextField()

    def __str__(self) -> str:
        return "%s" %(self.id)


class MoreApps(models.Model):
    base_app = models.OneToOneField(to = BaseApp,on_delete=models.CASCADE,related_name="app_more")
    is_more_app = models.BooleanField(default=False)
    developer_id = models.CharField(max_length=80)
    more_app_url = models.URLField()

    def __str__(self) -> str:
        return "%s" %(self.id)

class ShareApp(models.Model):

    base_app = models.OneToOneField(to = BaseApp,on_delete=models.CASCADE,related_name="app_share")
    is_share_app = models.BooleanField(default=False)
    share_message_app = models.CharField(max_length=250)
    share_message_link = models.URLField()

    def __str__(self) -> str:
        return "%s" %(self.id)

class OfficialWebsite(models.Model):
    base_app = models.OneToOneField(to = BaseApp,on_delete=models.CASCADE,related_name="app_official")
    is_official_website = models.BooleanField(default=False)
    official_website = models.URLField()

    def __str__(self) -> str:
        return "%s" %(self.id)

class PrivacyPolicy(models.Model):
    base_app = models.OneToOneField(to = BaseApp,on_delete=models.CASCADE,related_name="app_privacy_policy")
    is_privacy_policy = models.BooleanField(default=False)
    privacy_policy = models.TextField()

    def __str__(self) -> str:
        return "%s" %(self.id)

class TermsOfUse(models.Model):
    base_app = models.OneToOneField(to = BaseApp,on_delete=models.CASCADE,related_name="app_terms")
    is_terms_of_use = models.BooleanField(default=False)
    terms_of_use = models.TextField()

    def __str__(self) -> str:
        return "%s" %(self.id)

class SplashScreen(models.Model):
    base_app = models.OneToOneField(to = BaseApp,on_delete=models.CASCADE,related_name="app_splash_screen")
    is_splash_details = models.BooleanField(default=False)
    registration_detail = models.TextField()
    version_detail = models.TextField()

    def __str__(self) -> str:
        return "%s" %(self.id)

class FeedbackSupport(models.Model):
    base_app = models.OneToOneField(to = BaseApp,on_delete=models.CASCADE,related_name="app_feedback")
    is_feedback = models.BooleanField(default=False)
    cc_email_id = models.EmailField(null=True,blank=True)
    email_id = models.EmailField()
    email_subject = models.CharField(max_length=150)
    email_message = models.TextField()

    def __str__(self) -> str:
        return "%s" %(self.id)

class AppSettings(models.Model):
    base_app = models.OneToOneField(to = BaseApp,on_delete=models.CASCADE,related_name="app_settings")
    app_settings = models.TextField()

    def __str__(self) -> str:
        return "%s" %(self.id)

    def clean(self, *args, **kwargs):
        try:
            json.dumps(self.app_settings)
        except Exception as e:
            raise ValidationError('Invalid JSON Formate...')
        super(AppSettings,self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        self.app_settings = json.dumps(self.app_settings)
        super(AppSettings,self).save(*args, **kwargs)