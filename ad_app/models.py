from faulthandler import disable
from django.db import models
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError

class Category(models.Model):

    CATEGORIES = (
        ("External", 'External'),
        ("Custom", 'Custom'),
    )
    cat_name = models.CharField(max_length=200,verbose_name='Category Name',help_text='Ex. Banner,Interstitial')
    priority = models.IntegerField(default=0)
    ad_type = models.CharField(choices = CATEGORIES,max_length=50,default="External")
    cr_date = models.DateTimeField(auto_now_add=True,verbose_name='Created date')

    class Meta:
        unique_together = ('cat_name', 'ad_type')
        verbose_name_plural = "1. Category"

    def __str__(self) -> str:
        return '%s' %(self.cat_name)

class ExternalAd(models.Model):
    ad_name = models.CharField(max_length=100,help_text="Ex. Google AD,Admob AD")
    category = models.ForeignKey(to = Category,on_delete=models.CASCADE,related_name='ext_cat')    
    html_data = models.TextField()
    priority = models.IntegerField()
    cr_date = models.DateTimeField(auto_now_add=True,verbose_name='Created date')

    class Meta:
        verbose_name_plural = "2. ExternalAd"
        unique_together = ('ad_name', 'category')

    def __str__(self) -> str:
        return '%s' %(self.id)

class CustomAd(models.Model):
    ad_title = models.CharField(max_length=100,help_text="Enter your AD short title")
    category = models.ForeignKey(to = Category,on_delete=models.CASCADE,related_name='custom_cat')
    # ad_image = models.ImageField(upload_to='images/custom_ad',null = True,blank=True,help_text="Upload either image or image URL")
    ad_image_url = models.URLField(null = True,blank=True)
    redirect_url = models.URLField()
    priority = models.IntegerField()
    cr_date = models.DateTimeField(auto_now_add=True,verbose_name='Created date')

    class Meta:
        verbose_name_plural = "3. CustomAd"
        unique_together = ('ad_title', 'category')
        ordering = ('id',)

    # def clean(self, *args, **kwargs):
    #     if not (bool(self.ad_image_url) or bool(self.ad_image)):
    #         raise ValidationError('Enter either Image or Image URL')
    #     super(CustomAd,self).clean(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     super(CustomAd,self).save(*args, **kwargs)

    def __str__(self) -> str:
        return '%s (%s)' %(self.ad_title,self.category)

    def ad_image_tag(self):
        # if self.ad_image:
        #     return mark_safe('<img src="%s"  height="200px" width="400px"/>' % (self.ad_image.url))
        # elif self.ad_image_url:
        if self.ad_image_url:
            return mark_safe('<img src="%s"  height="200px" width="400px"/>' % (self.ad_image_url))
    ad_image_tag.short_description = 'Ad Image'

class Analytic(models.Model):
    ad = models.OneToOneField(to = CustomAd,on_delete=models.CASCADE,related_name="ad_analytics")
    ad_click = models.CharField(max_length=250,verbose_name="No of click",default=0)
    ad_impression = models.CharField(max_length=250,verbose_name="Impression",default=0)

    class Meta:
        verbose_name_plural = "4. Analytic"

    def __str__(self) -> str:
        return '%s' %(self.id)