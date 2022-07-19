from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout

from account.forms import RegistrationForm, AccountAuthenticationForm
from account.models import  Acount
from django.conf import settings

# Create your views here.

def register_view(request, *args, **kwargs):
    user =request.user
    if user.is_authenticated:
        return HttpResponse(f"you are already authenticated as {user.email}.")

    context = {}

#creating a new registration object and passing all the data that is included into the post request to that form
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            #this part is to log user in  
            email = form.cleaned_data.get('email').lower()
            raw_password =form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = get_redirect_if_eists(request)
            if destination: # check if destination != NONE
                return redirect(destination)
            return redirect('homeview')

        else:
            context['registration_form'] = form


    return render(request, 'account/register.html', context)




def login_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('homeview')

    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_eists(request)
                if destination:
                    return redirect(destination)
                return redirect('homeview')
        else:
            context['login_form'] = form


    return render(request, 'account/login.html', context)


def logout_view(request):
    logout(request) #MAKE SURE TO IMPORT LOGOUT FROM THE TOP IN LINE 3
    return redirect("homeview")


def get_redirect_if_eists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect




def account_view(request, *args, **kwargs):


    context = {}
    user_id = kwargs.get("user_id") # we will get the keyword argument from the url
    # finding the account(if i cant find the accout the program will take me to the execpt to return error)
    try:
       account = Acount.objects.get(pk=user_id)

    except Acount.DoesNotExist:
        return HttpResponse("that user doesnt exist")

    # if the account exists the variables will now be passed into the template( using the context)
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email

        # define state template variable(like if this is your profile or u are looking at someones profile)
        is_self = True
        is_friend = False
        user = request.user
        if user.is_authenticated and user != account:
            is_self  = False
        elif not user.is_authenticated:
             is_self  = False

        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL

    return render(request,'account/account.html', context)
