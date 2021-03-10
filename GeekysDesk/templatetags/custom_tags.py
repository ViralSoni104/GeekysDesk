from django import template
from SiteSettings.models import BasicSetting, ContactSetting, SocialMediaSetting, BasicSEOSetting
from Blog.models import Post, Category, Comment
import os

register = template.Library()

#here we will define template tags which is needes in templates like data filters etc so each and every time don't need to define and send in every page view

#getting site setting like social handle, site name, contacts
@register.simple_tag
def get_site_setting():
    Site_Basic_Setting = BasicSetting.objects.all().order_by('-id')[:1] #only one site basic data will be fetch which is last inserted
    Site_Basic_Setting = Site_Basic_Setting.first()

    Site_Contact_Settings = ContactSetting.objects.all() #contact have multiple contacts so here we will fetch all contacts data

    Site_Social_Media_Settings = SocialMediaSetting.objects.all() # same for social multiple social handle can be provided to show

    Site_Basic_Seo = BasicSEOSetting.objects.all().order_by('-id')[:1]
    Site_Basic_Seo = Site_Basic_Seo.first()

    Site_Settings = {
        'Basic_Settings' : Site_Basic_Setting,
        'Contact_Settings' : Site_Contact_Settings,
        'Socail_Media_Settings' : Site_Social_Media_Settings,
        'Basic_SEO_Settings' : Site_Basic_Seo,
    }
    return Site_Settings
    
@register.simple_tag
def get_user_profile_picture(user_id):
    user_profile = ''
    try:
        user_p = user_id.social_auth.get(pk=user_id.id) # getting extra data from social auth
        user_profile = user_p.extra_data
    except:
        user_profile = False
    return user_profile

@register.simple_tag
def get_comments_count(post):
    comments_count = Comment.objects.filter(post=post).count()
    comments_count = get_count_in_KMB(comments_count)
    return comments_count

@register.simple_tag
def to_int(value):
    try:
        new_val = int(value)
    except:
        new_val=str(value[:-3])[0]
        new_val=int(new_val) *1000
    return new_val

@register.filter(name='get_val')
def get_val(dict, key):
    return dict.get(key)

@register.simple_tag
def get_comment_plus_replies_total_count(comment_count,replies_count):
    total_count = int(comment_count) + int(replies_count)
    total_count = get_count_in_KMB(total_count)
    return total_count

@register.simple_tag
def get_count_in_KMB(count_to_convert):
    converted_count = ''
    if count_to_convert >= 1000:
        if count_to_convert >= 1000000:
            count_to_convert = count_to_convert/1000000
            converted_count = str(count_to_convert) + "M"
        else:
            count_to_convert = count_to_convert/1000
            converted_count = str(count_to_convert) + "K"
    else:
        converted_count = str(count_to_convert)
    return converted_count    

@register.simple_tag
def get_menu_categories():
    menu_categories = Category.objects.filter(status='True',show_to_main_menu='Yes').exclude(parent__title='Programming Langauages')[:4]
    programming_langauages = Category.objects.filter(status='True',show_to_main_menu='Yes',parent__title='Programming Langauages').order_by('id')[:4]
    main_menu_categories = {
        'menu_categories' : menu_categories,
        'programming_langauages' : programming_langauages,
    }
    return main_menu_categories

@register.simple_tag
def get_latest_posts():
    latest_posts = Post.objects.filter(status='True',category__status='True').order_by('-id')[:4]
    return latest_posts

@register.simple_tag
def get_env_var(key):
    return os.environ.get(key)