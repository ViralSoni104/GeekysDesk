from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from GeekysDesk import custom_messages
from mptt.templatetags.mptt_tags import cache_tree_children
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Post, Comment
from GeekysDesk.templatetags.custom_tags import get_count_in_KMB
from django.http.response import HttpResponse
from django.db import connection
from django.contrib.auth.decorators import login_required
import json
import datetime

# Create your views here.
def check_post_is_bookmarked(request,post):
    bookmarked=False
    post = Post.objects.get(slug=post.slug)
    if post.bookmark.filter(id=request.user.id).exists():
        bookmarked=True
    else:
        bookmarked=False
    return bookmarked

def check_list_of_post_is_bookmarked(request,bookmarked,post_list):
    bookmarked=bookmarked
    for p in post_list:
        bookmark=check_post_is_bookmarked(request,p)
        if bookmark and p.id not in bookmarked:
            bookmarked[p.id]=bookmark
    return bookmarked

def get_sidebar_categories(request):
    side_category = Category.objects.filter(id__in=[category.id for category in Category.objects.filter(status='True')[:9] if category.is_leaf_node()])
    side_category_with_post_count = {}
    for rs in side_category:
        count = Post.objects.filter(category_id=rs.id,status='True').count()
        side_category_with_post_count[rs] = count
    return side_category_with_post_count

def view_single_blog(request,category,slug):
    try:
        category = Category.objects.get(slug=category).id
        if category:
            post_data = Post.objects.filter(category__status='True',status='True',category_id=category,slug=slug)
            if post_data:
                bookmarked = check_post_is_bookmarked(request=request,post=post_data.first())
                side_category_with_post_count = get_sidebar_categories(request)
                post_on_order_of_date_create = Post.objects.filter(category_id=category).order_by('-create_at')
                last = post_on_order_of_date_create.first()
                first = post_on_order_of_date_create.last()
                next_post_id = post_data.first().id + 1
                prev_post_id = post_data.first().id  - 1
                if last.id >= next_post_id:
                    next_post = Post.objects.get(pk=next_post_id)
                else:
                    next_post = ''
                if prev_post_id >= first.id:
                    prev_post = Post.objects.get(pk=prev_post_id)
                else:
                    prev_post = ''
                
                comments = Comment.objects.filter(post=post_data.first(),parent=None).order_by('-id')
                replies = Comment.objects.filter(post=post_data.first()).exclude(parent=None)
                replyDict={}
                for reply in replies:
                    if reply.parent.id not in replyDict.keys():
                        replyDict[reply.parent.id]=[reply]
                    else:
                        replyDict[reply.parent.id].append(reply)

                context ={
                    'post' : post_data.first(),
                    'bookmarked' : bookmarked,
                    'side_category_with_post_count' : side_category_with_post_count,
                    'next_post' : next_post,
                    'prev_post' : prev_post,
                    'comments' : comments,
                    'replies' : replyDict,
                }
                return render(request,'single-blog.html',context=context)
            else:
                return redirect('invalid-url')
        else:
            return redirect('invalid-url')
    except:
        return redirect('invalid-url')

@login_required
def bookmark_post(request):
    if request.is_ajax() and request.user.is_authenticated:
        post_to_save = request.POST.get('post_to_save')
        post = Post.objects.get(pk=post_to_save,status='True',category__status='True')
        data={ 'status': custom_messages.SUCCESS_STATUS_CODE, }
        if post:
            if post.bookmark.filter(pk=request.user.id).exists():
                post.bookmark.remove(request.user)
                data.update({
                    'msg' : custom_messages.POST_REMOVED_FROM_BOOKMARKED,
                    'bookmarked' : False,
                })
            else:
                post.bookmark.add(request.user)
                data.update({
                    'msg' : custom_messages.POST_BOOKMARKED,
                    'bookmarked' : True,
                })
            return JsonResponse(data) 
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def category(request,slug):
    page = request.GET.get('page', 1)
    
    slug=slug.split('/')
    complete_slug_list_before_manipulate = slug[:-1]

    if len(slug)>1:
        slug=slug[-1]
    else:
        slug=slug[0]

    category = Category.objects._mptt_filter(slug=slug,status='True')
    if category:
        
        #check for a complete url with ancestors
        found = 0
        category_ancestors = category.get_ancestors()
        for rs in category_ancestors:
            if rs.slug in complete_slug_list_before_manipulate:
                found = found + 1
        if len(category_ancestors) != found:
            new_url_to_redirect = category.first().get_absolute_url()
            return redirect(f'{new_url_to_redirect}')
        
        category_title = category.first()
        sub_categories=''
        post_list=''
        data_sended=''
        bookmarked = {}
        if category.get_descendants():
            sub_categories = cache_tree_children(category.get_descendants())
            paginator = Paginator(sub_categories, 15)
            try:
                sub_categories = paginator.page(page)
            except PageNotAnInteger:
                sub_categories = paginator.page(1)
            except EmptyPage:
                sub_categories = paginator.page(paginator.num_pages)
            data_sended='Category'
        else:
            category=category.get()
            for rs in Category.objects.all():
                if rs.title == category:
                    category = rs
                    break
                
            post_list=Post.objects.filter(category_id=category.id,status='True')
            paginator = Paginator(post_list, 8)
            try:
                post_list = paginator.page(page)
            except PageNotAnInteger:
                post_list = paginator.page(1)
            except EmptyPage:
                post_list = paginator.page(paginator.num_pages)
            
            data_sended='Post'
            bookmarked = check_list_of_post_is_bookmarked(request,bookmarked,post_list)

        side_category_with_post_count = get_sidebar_categories(request)
        context={
            'datas' : data_sended,
            'post' : post_list,
            'sub_categories' : sub_categories,
            'category' : category_title,
            'side_category_with_post_count' : side_category_with_post_count,
            'bookmarked' : bookmarked,
        }
        return render(request,"category_details.html",context)
    else:
        return redirect('home')

@login_required
def postComment(request,post_slug):
    if request.method == "POST":
        try:
            post = Post.objects.get(slug=post_slug)
            if request.user.is_authenticated:
                user = request.user
                comment_text = request.POST.get('comment')
                parent = request.POST.get('parent','')
                if parent:
                    comment = Comment(user=user,comment_text=comment_text,post=post,parent_id=parent)
                    comment.save()
                    messages.success(request,custom_messages.COMMENT_REPLY_SUCCESS)
                else:
                    comment = Comment(user=user,comment_text=comment_text,post=post)
                    comment.save()
                    messages.success(request,custom_messages.COMMENT_POSTED_SUCCESS)

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def update_bookmark_count(request):
    if request.is_ajax():
        post_to_save = request.POST.get('post_to_save')
        post = Post.objects.get(pk=post_to_save,status='True',category__status='True')
        updated_count = str(get_count_in_KMB(post.bookmark.count()))
        return HttpResponse(updated_count)

@login_required
def bookmark_list(request):
    page = request.GET.get('page', 1)
    if request.user.is_authenticated:
        all_posts=Post.objects.all()
        post_list = []
        
        cursor = connection.cursor()
        user_id = request.user.id
        sql_query = "SELECT blog_post.id from blog_post,blog_post_bookmark WHERE blog_post.id=blog_post_bookmark.post_id and blog_post_bookmark.user_id="+str(user_id)+" and blog_post.status='True' ORDER BY blog_post_bookmark.id DESC"
        cursor.execute(sql_query)
        for r in cursor:
            post = Post.objects.get(id=r[0])
            post_list.append(post)
        
        # for p in all_posts:
        #     if p.bookmark.filter(id=request.user.id).exists():
        #         post_list.append(p)
        
        paginator = Paginator(post_list, 15)
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
            
        context = {
            'bookmark_posts' : post_list,
        }
        return render(request,'bookmark-list.html',context)

def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        posts = Post.objects.filter(title__icontains=q)

        results = []
        for rs in posts:
            post_json = {}
            post_json = rs.title
            results.append(post_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def search(request):
    if request.method == 'POST':
        query = request.POST.get('search_post')
        if query:
            bookmarked={}
            post_list = Post.objects.filter(title__icontains=query)

            page = request.GET.get('page', 1)
            paginator = Paginator(post_list, 15)

            try:
                post_list = paginator.page(page)
            except PageNotAnInteger:
                post_list = paginator.page(1)
            except EmptyPage:
                post_list = paginator.page(paginator.num_pages)

            side_category_with_post_count = get_sidebar_categories(request)
            bookmarked = check_list_of_post_is_bookmarked(request,bookmarked,post_list)
            context = {
                'search' : query,
                'post' : post_list,
                'side_category_with_post_count' : side_category_with_post_count,
                'bookmarked' : bookmarked,
            }
            return render(request, 'search.html', context)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('invalid-url')

def archives(request):
    first_year_when_started_blog = Post.objects.all().order_by('create_at').first().create_at.year
    years = []
    i=datetime.datetime.now().year
    while i>=first_year_when_started_blog:
        year_post_count = Post.objects.filter(create_at__year=i).count()
        years.append([i,year_post_count])
        i = i-1
    
    page = request.GET.get('page', 1)
    paginator = Paginator(years, 15)

    try:
        years = paginator.page(page)
    except PageNotAnInteger:
        years = paginator.page(1)
    except EmptyPage:
        years = paginator.page(paginator.num_pages)
    
    context = {
        'years' : years
    }
    return render(request,'archives.html',context=context)

def archives_yearly(request,year):
    if (len(str(year))==4):
        first_year_when_started_blog = Post.objects.all().order_by('create_at').first().create_at.year
        if year<=datetime.datetime.now().year and year>=first_year_when_started_blog:
            post_list = Post.objects.filter(create_at__year=year)

            page = request.GET.get('page', 1)
            paginator = Paginator(post_list, 15)

            try:
                post_list = paginator.page(page)
            except PageNotAnInteger:
                post_list = paginator.page(1)
            except EmptyPage:
                post_list = paginator.page(paginator.num_pages)
            
            context = {
                'post_list' : post_list,
                'year_for_canonical' : str(year),
            }
            return render(request,'archives.html',context=context)
    return redirect('invalid-url')