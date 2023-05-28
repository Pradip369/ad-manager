import json
from django import forms
from django.urls import reverse
from django.contrib import admin

from .serializers import BaseAppSerializer
from .models import *
import requests as send_request
from .push_in_github import github_push
import uuid 
from import_export.admin import ImportExportModelAdmin

class AdMobAdInline(admin.StackedInline):
    model = AdMobAd
    can_delete = False
    min_num = 1

class GoogleAdInline(admin.StackedInline):
    model = GoogleAd
    can_delete = False
    min_num = 1

class UnityAdInline(admin.StackedInline):
    model = UnityAd
    can_delete = False
    min_num = 1

class CustomAdInline(admin.StackedInline):
    model = CustomAd
    can_delete = False
    min_num = 1

class AppUpdateInformationInline(admin.StackedInline):
    model = AppUpdateInformation
    can_delete = False
    min_num = 1

class AboutAppInline(admin.StackedInline):
    model = AboutApp
    can_delete = False
    min_num = 1

class RateAppInline(admin.StackedInline):
    model = RateApp
    can_delete = False
    min_num = 1

class MoreAppsInline(admin.StackedInline):
    model = MoreApps
    can_delete = False
    min_num = 1

class ShareAppInline(admin.StackedInline):
    model = ShareApp
    can_delete = False
    min_num = 1

class OfficialWebsiteInline(admin.StackedInline):
    model = OfficialWebsite
    can_delete = False
    min_num = 1

class PrivacyPolicyInline(admin.StackedInline):
    model = PrivacyPolicy
    can_delete = False
    min_num = 1

class TermsOfUseInline(admin.StackedInline):
    model = TermsOfUse
    can_delete = False
    min_num = 1

class SplashScreenInline(admin.StackedInline):
    model = SplashScreen
    can_delete = False
    min_num = 1

class FeedbackSupportInline(admin.StackedInline):
    model = FeedbackSupport
    can_delete = False
    min_num = 1

class AppSettingsInline(admin.StackedInline):
    model = AppSettings
    can_delete = False
    min_num = 1

class BaseAppForm(forms.ModelForm):

    app_thubnail = forms.ImageField(required=False)

    def save(self, commit=True):

        app_thubnail = self.cleaned_data.get('app_thubnail', None)

        # Get the form instance so I can write to its fields
        instance = super(BaseAppForm, self).save(commit=commit)
        if app_thubnail:
            img_name = uuid.uuid4().hex[:6] + '.' + app_thubnail.name.split('.')[-1]
            # github_push(app_name = "AppImages",data = app_thubnail.file.read(),file_name = img_name)
            instance.thumbnail = f'https://github.com/kp-bitcoding/ad-manager/blob/main/AppImages/{img_name}?raw=true'
        if commit:
            instance.save()

        return instance

    class Meta:
        model = BaseApp
        fields = "__all__"


@admin.register(BaseApp)
class BaseAppAdmin(ImportExportModelAdmin):
    list_display= ["id","app_thumb_tag","title","package_id","created_date"]
    search_fields=["id","title","package_id"]
    list_per_page = 10
    list_filter = ['created_date',]
    readonly_fields = ["id","thumbnail","app_thumb_tag",'created_date']
    list_display_links = list_display
    form = BaseAppForm
    inlines = [
                AdMobAdInline,
                GoogleAdInline,
                UnityAdInline,
                CustomAdInline,
                AppUpdateInformationInline,
                AboutAppInline,
                RateAppInline,
                MoreAppsInline,
                ShareAppInline,
                OfficialWebsiteInline,
                PrivacyPolicyInline,
                TermsOfUseInline,
                SplashScreenInline,
                FeedbackSupportInline,\
                AppSettingsInline
            ]

    def save_model(self, request, obj, form, change):
        obj.save()
        data = BaseAppSerializer(obj).data
        # github_push(app_name = obj.title,data=json.dumps(data,indent = 1))