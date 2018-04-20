from .models import NewsPost, Author
from .forms import SignupForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

def author_articles(request, author_id):
    author = Author.objects.get(id=author_id)
    articles = NewsPost.objects.filter(author=author)
    return render(request, 'home.html', {'page': 'author_articles',
                                         'titles': articles})


def author_about(request, author_id):
    author   = Author.objects.get(id=author_id)
    articles = NewsPost.objects.all().filter(id=author_id)
    #print(articles[0])
    return render(request, 'home.html', {'page': 'author_about',
                                         'author': author_id ,
                                         'articles': articles})
def articles_main(request):
    return render(request, 'home.html')#Will need to make Articles.html
    '''
    Atricles will need to display articles based on user like or new.
    '''

def author_article_show(request,author_id,article):
    author   = Author.objects.get(id=author_id)
    main_article = NewsPost.objects.filter(slug=article)
    print(author.last_name)
    print("___________________________________")
    return render(request, 'display_article_base.html', {'page': 'author_articles_news_articles',
                                         'article': main_article[0], 'author': author, 'file_name':main_article[0].file_upload})


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


@login_required
def user_profile(request):
    return render(request, 'user_profile.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            if len(User.objects.filter(email=email).all()) > 1:
                form.add_error('email',
                               'A user with that email already exists.')
                return render(request, 'registration/sign_up.html',
                              {'form': form}, status=400)
            user = authenticate(username=username, password=password)
            if user is not None:
                user.save()
                login(request, user)
                return HttpResponseRedirect('user/',status=201)
            else:
                return render(request, 'registration/sign_up.html',
                              {'form': form}, status=404)
        else:
            return render(request, 'registration/sign_up.html',
                          {'form': form}, status=400)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignupForm()
    return render(request, 'registration/sign_up.html', {'form': form})



def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/user')
        else:
            return render(request, 'registration/sign_up.html',
                          {'form': form}, status=400)
    else:
        form_lin = LoginForm()
        return render(request, 'registration/login.html', {'form': form_lin})
