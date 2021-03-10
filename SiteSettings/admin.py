from django.contrib import admin
from .models import BasicSetting, ContactSetting, SocialMediaSetting, BasicSEOSetting

# Register your models here.
class BasicSettingAdmin(admin.ModelAdmin):
    model=BasicSetting
    list_display = ('Site_Name','logo_image_tag','icon_image_tag')
    def has_add_permission(self, request):
        # check if generally has add permission
        permission_value = super().has_add_permission(request)
        # set add permission to False, if object already exists
        if permission_value and BasicSetting.objects.exists():
            permission_value = False
        return permission_value

class ContactSettingAdmin(admin.ModelAdmin):
    model=ContactSetting
    list_display = ('Contact_Type','Contact')
    search_fields = ('Contact_Type','Contact')

class SocialMediaSettingAdmin(admin.ModelAdmin):
    model=SocialMediaSetting
    list_display = ('Social_Media_Name','Font_Awesome_Class_For_Icon','Social_Media_Link')
    search_fields = ('Social_Media_Name',)

class BasicSEOSettingAdmin(admin.ModelAdmin):
    model=BasicSEOSetting
    list_display = ('Home_Page_Meta_Description','About_Page_Meta_Description','Contact_Page_Meta_Description')
    def has_add_permission(self, request):
        # check if generally has add permission
        permission_value = super().has_add_permission(request)
        # set add permission to False, if object already exists
        if permission_value and BasicSEOSetting.objects.exists():
            permission_value = False
        return permission_value

admin.site.register(BasicSetting,BasicSettingAdmin)
admin.site.register(ContactSetting,ContactSettingAdmin)
admin.site.register(SocialMediaSetting,SocialMediaSettingAdmin)
admin.site.register(BasicSEOSetting,BasicSEOSettingAdmin)