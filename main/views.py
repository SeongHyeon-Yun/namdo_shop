from django.shortcuts import render, redirect

# Create your views here.
def index(reqeust):
    return render(reqeust, 'main/index.html')