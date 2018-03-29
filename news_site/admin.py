from django.contrib import admin
from news_site.models import NewsPost, Comment, Author


admin.site.register(Author)
admin.site.register(NewsPost)
admin.site.register(Comment)
