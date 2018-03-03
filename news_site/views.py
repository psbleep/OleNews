from django.shortcuts import render
from news_site.models import NewsPost
from django.http import Http404
from django.template import Template
from django.template.loader import get_template

def author_about(request, name):
    authors = NewsPost.objects.filter(author=name)
    titles = []
    for author in authors:
        titles.append(author.title)
    if authors.count() == 0:
        raise Http404
    return render(request, 'test.html' , {'titles': titles} )
'''
To Do: Find better naming conventions set up Author login and have it generate a
test for this URL convention
'''
