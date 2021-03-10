from django.contrib import admin
from .models import Category, Post, Comment
from mptt.admin import DraggableMPTTAdmin

# Register your models here.
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title','image_tag','status','show_to_main_menu')
    list_display_links = ('indented_title',)
    search_fields = ('name',)
    list_filter = ('status','create_at','update_at')
    actions = ['make_published','make_unpublished','show_to_main_menu','hide_from_main_menu']
    prepopulated_fields = {'slug': ('title',)}

    def make_published(modeladmin, request, queryset):
        queryset.update(status='True')
    make_published.short_description = "Make category visible to user"
    

    def make_unpublished(modeladmin, request, queryset):
        queryset.update(status='False')
    make_unpublished.short_description = "Hide category from user"

    def show_to_main_menu(modeladmin, request, queryset):
        queryset.update(show_to_main_menu='Yes')
    show_to_main_menu.short_description = "Show category to main menu"
    

    def hide_from_main_menu(modeladmin, request, queryset):
        queryset.update(show_to_main_menu='No')
    hide_from_main_menu.short_description = "Hide category from main menu"

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','category','image_tag','status','feature_to_editors_pick']
    list_filter = ['category','status','feature_to_editors_pick']
    search_fields = ('title','category',)
    actions = ['make_published','make_unpublished','show_to_editors_pick','hide_from_editors_pick']
    prepopulated_fields = {'slug': ('title',)}
    
    def make_published(modeladmin, request, queryset):
        queryset.update(status='True')
    make_published.short_description = "Make post visible to user"
    

    def make_unpublished(modeladmin, request, queryset):
        queryset.update(status='False')
    make_unpublished.short_description = "Hide post from user"

    def show_to_editors_pick(modeladmin, request, queryset):
        queryset.update(feature_to_editors_pick='Yes')
    show_to_editors_pick.short_description = "Feature post to show as editor's pick"
    

    def hide_from_editors_pick(modeladmin, request, queryset):
        queryset.update(feature_to_editors_pick='No')
    hide_from_editors_pick.short_description = "Remove post from editor's pick"

    class Media:
        js= ('js/tinyInject.js',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment_text',]
    list_filter = ['timestamp',]
    search_fields = ('comment_text',)

    
admin.site.register(Category,CategoryAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)