from django.contrib import admin
from insert_app.push_in_github import github_push
from .models import CustomAd,Analytic,Category,ExternalAd
from django.forms import ModelChoiceField
from import_export.admin import ImportExportModelAdmin
from django import forms
import uuid 

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display= ["id","cat_name","priority","ad_type","cr_date"]
    search_fields=["cat_name",]
    list_filter = ["cr_date",]
    readonly_fields = ["id","cr_date"]
    list_display_links = list_display

@admin.register(ExternalAd)
class ExternalAdAdmin(ImportExportModelAdmin):
    list_display= ["id","ad_name","category","priority","cr_date"]
    list_filter = ["cr_date",]
    readonly_fields = ["id","cr_date"]
    list_display_links = list_display

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(queryset=Category.objects.filter(ad_type='External'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class CustomAdAdminForm(forms.ModelForm):

    ad_image = forms.ImageField(required=False)

    def save(self, commit=True):

        _ad_image = self.cleaned_data.get('ad_image', None)

        # Get the form instance so I can write to its fields
        instance = super(CustomAdAdminForm, self).save(commit=commit)
        if _ad_image:
            img_name = uuid.uuid4().hex[:6] + '.' + _ad_image.name.split('.')[-1]
            github_push(app_name = "AdImages",data = _ad_image.file.read(),file_name = img_name)
            instance.ad_image_url = f'https://github.com/kp-bitcoding/ad-manager/blob/main/AdImages/{img_name}?raw=true'
        if commit:
            instance.save()
        return instance

    class Meta:
        model = CustomAd
        fields = "__all__"

@admin.register(CustomAd)
class CustomAdAdmin(ImportExportModelAdmin):
    list_display= ["id","ad_title","category","priority","cr_date"]
    search_fields=["id","ad_title","redirect_url","priority"]
    list_per_page = 10
    list_filter = ["cr_date",]
    list_display_links = list_display
    readonly_fields = ["ad_image_url","ad_image_tag","id","cr_date"]
    form = CustomAdAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(queryset=Category.objects.filter(ad_type='Custom'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Analytic)
class AnalyticAdmin(ImportExportModelAdmin):
    list_display= ["id","ad","ad_click","ad_impression"]
    search_fields=["id","ad__ad_title"]
    list_per_page = 10
    list_filter = ['ad_click','ad_impression']
    readonly_fields = ["id",'ad_click','ad_impression','ad']
    list_display_links = list_display