from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import mptt
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Category(MPTTModel):
    STATUS=(
        ('True','True'),
        ('False','False'),
    )
    SHOW=(
        ('Yes','Yes'),
        ('No','No'),
    )
    title = models.CharField(max_length=50)
    meta_description=models.TextField(null=True,blank=True)
    meta_keywords=models.TextField(null=True,blank=True)
    status=models.CharField(max_length=10,choices=STATUS)
    show_to_main_menu=models.CharField(max_length=10,choices=SHOW,default='No')
    image=models.ImageField(blank=True,upload_to='img/Category/')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',db_index=True)
    slug = models.SlugField(null=False,unique=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name_plural = 'categories'
    
    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [ i.slug for i in ancestors]
            slugs = []
            for i in range(len(ancestors)):
                slugs.append('/'.join(ancestors[:i+1]))
            return slugs

    def __str__(self):
        return self.title
    
    def get_child_count(self):
        if self._mpttfield('right') is None:
            return 0
        else:
            childs=self.get_children()
            count=0
            for n in childs:
                count+=1
            return count
            #return ( self._mpttfield('right') - self._mpttfield('left') - 1 ) // 2 


    def get_absolute_url(self):
        slugs=''
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [ i.slug for i in ancestors]
            for i in range(len(ancestors)):
                if i==0:
                    slugs+=ancestors[i]
                else:
                    slugs+='/'
                    slugs+=ancestors[i]
            return reverse('category', kwargs={'slug': slugs})

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    def remove_on_image_update(self):
        try:
            # is the object in the database yet?
            obj = Category.objects.get(id=self.id)
        except Category.DoesNotExist:
            # object is not in db, nothing to worry about
            return
        # is the save due to an update of the actual image file?
        if obj.image and self.image and obj.image != self.image:
            # delete the old image file from the storage in favor of the new file
            obj.image.delete()

    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        self.image.delete()
        return super(Category, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        self.remove_on_image_update()
        return super(Category, self).save(*args, **kwargs)

class Post(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    EDITORS_PICK=(
        ('Yes','Yes'),
        ('No','No'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #many to one relation with Category
    title=models.CharField(max_length=255,default=None)
    feature_image = models.ImageField(blank=False,upload_to='img/Post/',default='')
    short_description = models.TextField(default='',blank=False)
    content = models.TextField()
    slug = models.SlugField(null=False, unique=True)
    meta_description=models.TextField(null=True,blank=True)
    meta_keywords=models.TextField(null=True,blank=True)
    status=models.CharField(max_length=10,choices=STATUS,default=True)
    feature_to_editors_pick=models.CharField(max_length=10,choices=EDITORS_PICK,default='No')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    bookmark = models.ManyToManyField(User,related_name='bookmark',blank=True)
    
    def __str__(self):
        return self.title

    def image_tag(self):
        if self.feature_image is not None:
            return mark_safe('<img src="/media/{}" height="50"/>'.format(self.feature_image))
        else:
            return ""
    
    def remove_on_image_update(self):
        try:
            # is the object in the database yet?
            obj = Post.objects.get(id=self.id)
        except Post.DoesNotExist:
            # object is not in db, nothing to worry about
            return
        # is the save due to an update of the actual image file?
        if obj.feature_image and self.feature_image and obj.feature_image != self.feature_image:
            # delete the old image file from the storage in favor of the new file
            obj.feature_image.delete()

    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        self.feature_image.delete()
        return super(Post, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        self.remove_on_image_update()
        return super(Post, self).save(*args, **kwargs)

class Comment(models.Model):
    comment_text = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
