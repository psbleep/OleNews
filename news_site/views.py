from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def author_about(request, name):
    print(name)
    return HttpResponse("Just A temp string!")
'''
To Do: Find better naming conventions set up Author login and have it generate a
test for this URL convention
'''
