from django.contrib import admin
from .models import Subscriber, Contact

class SubscriberAdmin(admin.ModelAdmin):
    model=Subscriber
    list_display = ('email','is_verified','token_time')
    list_filter = ('is_verified',)

class ContactAdmin(admin.ModelAdmin):
    model=Contact
    ordering=('-contacted_on',)
    list_display = ('contact_email','contact_name','message')
    list_filter = ('contacted_on',)
    search_fields = ('contact_name','contact_mail','message')

admin.site.register(Subscriber,SubscriberAdmin)
admin.site.register(Contact,ContactAdmin)