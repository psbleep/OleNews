from django.shortcuts import render
from news_site.models import NewsPost
from news_site.models import Author
from django.http import Http404
from django.template import Template
from django.template.loader import get_template

def author_about(request, name):
    authors = NewsPost.objects.filter()
    authors = []
    for author in authors:
        titles.append(author.title)
    if authors.count() == 0:
        raise Http404
    return render(request, 'test.html' , {'titles': titles} )
'''
To Do: Find better naming conventions set up Author login and have it generate a
test for this URL convention
'''
def author_general(request):
    authors = Author.objects.all()
    if authors.count() == 0:
        raise Http404
    return render(request, 'Author_page.html', {'authors_names': authors})

def home(request):
    return render(request, 'home.html')
