from django.shortcuts import render

# Come here from home/urls.py
def index(request):
    return render(request, 'home/home.html')
