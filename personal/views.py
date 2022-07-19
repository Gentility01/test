from django.shortcuts import render

# Create your views here.

def homeview(request, *args, **kwargs):
    context = {}
    return render(request, 'personal/home.html',context)