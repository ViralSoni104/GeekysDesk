"""GeekysDesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from . import settings
from django.conf.urls.static import static
from . import views as home_view
from Blog import views as blog_view
from SiteSettings.models import BasicSetting
from GeekysDesk.templatetags import custom_tags
from django.contrib.auth import views as auth_views

Site_Name = ''
if BasicSetting.objects.count()>=1:
    Site_Name = custom_tags.get_site_setting()['Basic_Settings'].Site_Name
admin.site.site_header = Site_Name + " Admin"
admin.site.index_title = "Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view.Home,name="home"),
    path('subscribe-to-newsletter/',home_view.Subscribe_To_Newsletter,name='subscribe-to-newsletter'),
    re_path(r'confirm-email/(?P<token>.*)/$',home_view.subscription_confirmation,name='subscription-confirmation'),
    re_path(r'unsubscribe/(?P<token>.*)/$',home_view.unsubscribe,name='unsubscribe'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    path('login/',home_view.Login,name="login"),
    path('archives/',blog_view.archives,name="archives"),
    path('archives/<int:year>/',blog_view.archives_yearly,name="archives-yearly"),
    path('postComment/<str:post_slug>',blog_view.postComment,name='postComment'),
    path('<slug:category>/<slug:slug>',blog_view.view_single_blog,name="single-blog"),
    path('bookmark/',blog_view.bookmark_post,name="bookmark-post"),
    re_path(r'^category/(?P<slug>.*)/$',blog_view.category,name='category'),
    path('about-us/',home_view.about_us,name='about-us'),
    path('contact-us/',home_view.contact_us,name='contact-us'),
    path('updateCount/',blog_view.update_bookmark_count,name='update-bookmark-count'),
    path('bookmark-list/',blog_view.bookmark_list,name='bookmark-list'),
    path('search_auto/',blog_view.search_auto,name="search_auto"),
    path('search/',blog_view.search,name="search"),
    path('invalid-url/',home_view.invalid_url,name="invalid-url"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)