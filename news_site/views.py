from .models import NewsPost, Author
from .forms import SignupForm, LoginForm, CommentForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import json


def author_articles(request, author_id):
    author = Author.objects.get(id=author_id)
    articles = NewsPost.objects.filter(author=author)
    return render(request, 'home.html', {'page': 'author_articles',
                                         'titles': articles})


def author_about(request, author_id):
    author = Author.objects.get(id=author_id)
    articles = NewsPost.objects.filter(author=author)
    print(articles)
    return render(request, 'home.html', {'page': 'author_about',
                                         'author': author_id,
                                         'articles': articles})


def articles_main(request):
    return render(request, 'home.html')  # Will need to make Articles.html
    '''
    Atricles will need to display articles based on user like or new.
    '''


def author_article_show(request, author_id, article):
    author = Author.objects.get(id=author_id)
    main_article = NewsPost.objects.get(slug=article)
    like_count = main_article.users_liked.distinct().count()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.post = main_article
            post.user = request.user
            post.created = timezone.now()
            post.updated = timezone.now()
            post.approved = True
            post.save()
    else:
        form = CommentForm()
    return render(request, 'display_article_base.html',
                  {'page': 'author_articles_news_articles',
                   'article': main_article,
                   'author': author,
                   'file_name': main_article.file_upload,
                   'form': form,
                   'likes': like_count,
                   'post': article}
                  )


'''
To Do: Find better naming conventions set up Author login and have it generate
a test for this URL convention
'''


def comment_submit(request):
    return ''


def author_general(request):
    authors = Author.objects.all()
    if authors.count() == 0:
        raise Http404
    return render(request, 'home.html', {'page': 'authors',
                                         'authors_names': authors})


def home(request):
    return render(request, 'home.html', {'page': 'home'})


@login_required
def user_profile(request, user_name):
    if(user_name == request.user.username):
        liked_articles = request.user.users_liked.all()
        total_likes = len(liked_articles)
        return render(request, 'user_profile.html',
                      {'likes': total_likes,
                       'liked_articles': liked_articles})
    else:
        return redirect('/user/{}'.format(request.user.username))

@login_required
def user_settings(request):
    return render(request, 'user_pages/user_settings.html')

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
                return HttpResponseRedirect('user/', status=201)
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
            return HttpResponseRedirect('/user/{}'.format(username))
    else:
        form_lin = LoginForm()
        return render(request, 'registration/login.html', {'form': form_lin})


# Working on Likes May be very Buggy
def like(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        newspost = NewsPost.objects.get(slug=slug)
        if newspost.users_liked.filter(id=user.id).exists():
            print("Removing User")
            newspost.users_liked.remove(user)
            newspost.save()
        else:
            print("Adding User")
            newspost.users_liked.add(user)
            newspost.save()
    ctx = {'likes_count': newspost.total_likes}
    return HttpResponse(json.dumps(ctx), content_type='application/json')
