from django.shortcuts import render
from news_site.models import NewsPost
from django.http import Http404
from django.shortcuts import render_to_response


def author_about(request, name):
    print("trying to get html")
    author = NewsPost.objects.filter(author=name)
    print("test")
    print(author[0].file_upload)
    if author.count() == 0:
        raise Http404

    return render_to_response(author[0].file_upload)
'''
To Do: Find better naming conventions set up Author login and have it generate a
test for this URL convention
'''
