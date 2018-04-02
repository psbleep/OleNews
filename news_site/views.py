from django.shortcuts import render
from news_site.models import NewsPost
from news_site.models import Author
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import SignupForm
from django.http import HttpResponseRedirect,Http404


def author_articles(request, author_id):
    author = Author.objects.get(id=author_id)
    articles = NewsPost.objects.filter(author=author)
    return render(request, 'home.html', {'page': 'author_articles',
                                         'titles': articles})


def author_about(request, name):
    articles = NewsPost.objects.filter(author__user__last_name=name)
    return render(request, 'home.html', {'page': 'author_about',
                                         'titles': articles})


'''
To Do: Find better naming conventions set up Author login and have it generate
a test for this URL convention
'''


def author_general(request):
    authors = Author.objects.all()
    if authors.count() == 0:
        raise Http404
    return render(request, 'home.html', {'page': 'authors',
                                         'authors_names': authors})


def home(request):
    return render(request, 'home.html', {'page': 'home'})


def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                #new_user = User.objects.create(user=user)
                user.save()#new_user.save()
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/sign_up.html')
                #To Do: raise flag for non-authentication
        else:
            raise ValueError(form.errors)#The error is thrown here. I only make vauge comments 
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignupForm()
    return render(request, 'registration/sign_up.html', {'form': form})
