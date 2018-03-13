from django.shortcuts import render
from news_site.models import NewsPost
from news_site.models import Author
from django.http import Http404
from django.template import Template
from django.template.loader import get_template

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


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

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'home.html', {'form': form, 'page': 'register'})
