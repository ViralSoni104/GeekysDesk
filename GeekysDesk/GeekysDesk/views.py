from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Subscriber
from Blog.models import Post
from django.core.validators import validate_email
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core import signing
import datetime
from django.contrib import messages
from . import custom_messages
from django.http import HttpResponseRedirect
from .forms import ContactForm
from .templatetags.custom_tags import get_env_var
# from django.conf import settings
# from django.urls import URLPattern, URLResolver

# def list_urls(lis,acc=None):
#     if acc is None:
#         acc = []
#     if not lis:
#         return
#     l = lis[0]
#     if isinstance(l, URLPattern):
#         yield acc + [str(l.pattern)] + [str(l.name)]
#     elif isinstance(l,URLResolver):
#         yield from list_urls(l.url_patterns, acc + [str(l.pattern)])
#     yield from list_urls(lis[1:],acc)

# def show_urls():
#     urlconf = __import__(settings.ROOT_URLCONF,{},{},[''])
#     lst={}
#     i=0
#     for p in list_urls(urlconf.urlpatterns):
#         if p[len(p)-1] != 'None' and '^oauth/' not in p:
#             lst.update({i:''.join(p[len(p)-1])})
#             i+=1
#     lst = [(k,v) for k, v in lst.items()] #list to tupel
#     return lst

#home view
def Home(request):
    editors_pick=Post.objects.filter(feature_to_editors_pick='Yes',status='True',category__status='True').order_by('-id')[:4]
    context = {
        'editors_pick':editors_pick,
    }
    return render(request,'index.html',context=context)

#login view
def Login(request):
    #check user is already logged in or not if logged in then no need to display login page to that user
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request,'login.html')
    
#newsletter subscription view
def Subscribe_To_Newsletter(request):
    if request.is_ajax():
        email = request.POST.get('email')
        data={ 'status': custom_messages.SUCCESS_STATUS_CODE, } #data dictonary to show messages with success status code

        #check email is blank or given
        if email: 
            try: # if given validate email is in proper format or not
                validate_email(email)
                check_exsist = Subscriber.objects.filter(email=email) #check email given is already in our database or not
                if check_exsist: # if it is already in database no need to subscribe again give error already subscribed
                    #update data with message and class for alert as per code
                    data.update({
                        'class' : custom_messages.ALERT_DANGER_CLASS+' '+custom_messages.ALERT_DISMISSIBLE_CLASS+' '+custom_messages.SHOW_CLASS,
                        'msg' : custom_messages.ALREADY_SUBSCRIBED,
                    })
                else: # if not in our database then send mail to confirm email address given
                    token_time = datetime.datetime.now().strftime("%H:%M:%S")
                    
                    #create instance for subscriber but don't save now save when email is successfully sended
                    new_subscriber = Subscriber(email = email,is_verified = False,token_time=token_time)
                    
                    try: #will go in except block if email is not sended

                        #to verify email we will use email and time when mail is sended
                        token = {
                            'email' : email,
                            'time' : token_time
                        }

                        #encrpyt it so not easy to directly understand which email and on which time mail is sended
                        token = signing.dumps(token) 
                        current_site = get_current_site(request) #get current site domain
                        mail_subject = custom_messages.EMAIL_SUBSJECT_FOR_SUBSCRIPTION

                        #send mail in html format
                        message = render_to_string('email_templates\confirm_email_subscription.html', {
                            'domain': current_site.domain,
                            'token': token,
                        })
                        to_email = email
                        email = EmailMessage(
                            mail_subject, message,to=[to_email],
                        )
                        email.content_subtype='html'
                        email.send()

                        #save to database if email is sended successfully
                        new_subscriber.save()
                        #update data with message and class for alert as per code
                        data.update({
                            'class' : custom_messages.ALERT_SUCCESS_CLASS+' '+custom_messages.ALERT_DISMISSIBLE_CLASS+' '+custom_messages.SHOW_CLASS,
                            'msg' : custom_messages.SUCCESSFULLY_SUBSCRIBED,
                        })
                    except:
                        #update data with message and class for alert as per code
                        data.update({
                            'class' : custom_messages.ALERT_WARNING_CLASS+' '+custom_messages.ALERT_DISMISSIBLE_CLASS+' '+custom_messages.SHOW_CLASS,
                            'msg' : custom_messages.PROBLEM_WHILE_SENDING_EMAIL,
                        })
            except:
                #update data with message and class for alert as per code
                data.update({
                    'class' : custom_messages.ALERT_DANGER_CLASS+' '+custom_messages.ALERT_DISMISSIBLE_CLASS+' '+custom_messages.SHOW_CLASS,
                    'msg' : custom_messages.INVALID_EMAIL_ADDREDD,
                })
        else:
            #update data with message and class for alert as per code
            data.update({
                'class' : custom_messages.ALERT_WARNING_CLASS+' '+custom_messages.ALERT_DISMISSIBLE_CLASS+' '+custom_messages.SHOW_CLASS,
                'msg' : custom_messages.BLANK_EMAIL_ERROR,
            })
        return JsonResponse(data) #send data in json to template
    else:
        return redirect('invalid-url')

#verify email subscription view
def subscription_confirmation(request,token):
    try:
        #check encrypted token is given proper in link or tempared(if somemone try to tempared link if he know how token is encrypted)
        data = signing.loads(token)
        try: #check email sended in encrypted token is in our database(if somemone try to tempared link if he know how token is encrypted)
            subscriber = Subscriber.objects.get(email=data['email'])
            date_format = "%H:%M:%S"
            time_data = str(data['time'])
            time_subscriber = str(subscriber.token_time)
            diff_time= datetime.datetime.strptime(time_data,date_format) - datetime.datetime.strptime(time_subscriber,date_format)
            if (diff_time.seconds/3600) == 0.0: #verify if time in token and in our database is same otherwise problem in verification
                subscriber.is_verified = True
                subscriber.save()
                #messages to show on subscription page
                messages.success(request,custom_messages.SUBSCRIPTION_CONFIRMED)
            else:
                #messages to show on subscription page
                messages.warning(request,custom_messages.PROBLEM_AT_EMAIL_VERIFICATION+' '+custom_messages.UNSUBSCRIBE_FIRST)
        except:
            #messages to show on subscription page
            messages.error(request,custom_messages.PROBLEM_AT_EMAIL_VERIFICATION+' '+custom_messages.SUBSCRIBE_FIRST)
            return render(request,'confirm_subscription.html')
    except:
        return redirect('invalid-url')

#unsubscibe newsletter view    
def unsubscribe(request,token):
    try:
        #check encrypted token is given proper in link or tempared(if somemone try to tempared link if he know how token is encrypted)
        data = signing.loads(token)
        try: #check email sended in encrypted token is in our database then only unsubscribe them(if somemone try to tempared link if he know how token is encrypted)
            subscriber = Subscriber.objects.get(email=data['email'])
            subscriber.delete()
            #messages to show on subscription page
            messages.success(request,custom_messages.UNSUBSCRIED_SUCCESSFULLY)
        except:
            #messages to show on subscription page
            messages.error(request,custom_messages.PROBLEM_AT_EMAIL_VERIFICATION+' '+custom_messages.SUBSCRIBE_FIRST)
        return render(request,'confirm_subscription.html')
    except:
        return redirect('invalid-url')

def about_us(request):
    return render(request,'about-us.html')

def contact_us(request):
    form=ContactForm()
    if request.method == "POST":
        form=ContactForm(data=request.POST)
        if form.is_valid():
            name=request.POST.get('contact_name')
            message_by_user=request.POST.get('message')
            user_email=request.POST.get('contact_email')
            form.save()
            
            mail_subject = 'Contact Mail'
            message = 'Hey Admin, you got new contact mail from '+ name + ' By Email - '+ user_email +'.\nMessage from user is added below.\n'+message_by_user

            email = EmailMessage(
                mail_subject, message,to=[get_env_var('EMAIL_HOST_USER'),]
            )
        
            try:
                email.send()
                messages.success(request,custom_messages.CONTACT_MAIL_SENT_SUCCESS)
            except:
                messages.warning(request,custom_messages.CONTACT_MAIL_SENT_FAILED)

            return redirect('contact-us')
    return render(request,'contact-us.html', {'form':form})

def invalid_url(request):
    return render(request,'404.html')