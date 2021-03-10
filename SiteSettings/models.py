from django.db import models
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError

# Create your models here.
class BasicSetting(models.Model):
    Site_Icon = models.ImageField(upload_to='img/Site/')
    Site_Logo = models.ImageField(upload_to='img/Site/')
    Site_Name = models.CharField(max_length=255,blank=True)
    Site_Short_About_Info = models.TextField(default='')

    def icon_image_tag(self):
        if self.Site_Icon is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.Site_Icon.url))
        else:
            return ""
    
    def logo_image_tag(self):
        if self.Site_Logo is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.Site_Logo.url))
        else:
            return ""

    def remove_on_image_update(self):
        try:
            # is the object in the database yet?
            obj = BasicSetting.objects.get(id=self.id)
        except BasicSetting.DoesNotExist:
            # object is not in db, nothing to worry about
            return

        # is the save due to an update of the actual image file?
        if obj.Site_Icon and self.Site_Icon and obj.Site_Icon != self.Site_Icon:
            # delete the old image file from the storage in favor of the new file
            obj.Site_Icon.delete()
        
        # is the save due to an update of the actual image file?
        if obj.Site_Logo and self.Site_Logo and obj.Site_Logo != self.Site_Logo:
            # delete the old image file from the storage in favor of the new file
            obj.Site_Logo.delete()

    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        self.Site_Logo.delete()
        self.Site_Icon.delete()
        return super(BasicSetting, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        self.remove_on_image_update()
        return super(BasicSetting, self).save(*args, **kwargs)

class ContactSetting(models.Model):
    Contact_Type = models.CharField(max_length=50,help_text='Like. Email, Phone, Address etc.')
    Contact = models.CharField(max_length=255)

class SocialMediaSetting(models.Model):
    Social_Media_Name = models.CharField(max_length=50)
    Font_Awesome_Class_For_Icon = models.CharField(max_length=100,help_text='Ex -  fa fa-facebook')
    Social_Media_Link = models.CharField(max_length=255)

class BasicSEOSetting(models.Model):
    Home_Page_Meta_Keyword = models.TextField(default='')
    Home_Page_Meta_Description = models.TextField(default='')
    About_Page_Meta_Keyword = models.TextField(default='')
    About_Page_Meta_Description = models.TextField(default='')
    Contact_Page_Meta_Keyword = models.TextField(default='')
    Contact_Page_Meta_Description = models.TextField(default='')