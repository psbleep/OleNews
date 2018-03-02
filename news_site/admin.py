from django.contrib import admin
from news_site.models import NewsPost
from news_site.models import Comment

admin.site.register(NewsPost)
admin.site.register(Comment)
