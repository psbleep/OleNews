from django.shortcuts import render
from news_site.models import NewsPost
from news_site.models import Author
from django.http import Http404
from django.template import Template
from django.template.loader import get_template
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm, SigninForm
from django.http import HttpResponseRedirect

def author_articles(request, author_id):
    author = Author.objects.get(id=author_id)
    articles = NewsPost.objects.filter(author = author)
    return render(request, 'home.html', {'page': 'author_articles',
                                         'titles': articles})

def author_about(request, name):
    articles = NewsPost.objects.filter(author__last_name = name)
    return render(request, 'home.html' , {'page': 'author_about',
                                          'titles': articles} )
'''
To Do: Find better naming conventions set up Author login and have it generate a
test for this URL convention
'''
def author_general(request):
    authors = Author.objects.all()
    if authors.count() == 0:
        raise Http404
    return render(request, 'home.html', {'page': 'authors',
                                         'authors_names': authors})

def home(request):
    return render(request, 'home.html', {'page': 'home'})

def sign_in(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            #login(request, user)
            return HttpResponseRedirect('/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SigninForm()
    return render(request, 'registration/sign_in.html', {'form': form})

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignupForm()
    return render(request, 'registration/sign_up.html', {'form': form})

def login_check(request):
    username = request.POST['username']
    password = request.POST['password']
    print(password)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
