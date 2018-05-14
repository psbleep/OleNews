from django.contrib import admin
from news_site.models import NewsPost, Comment


admin.site.register(NewsPost)
admin.site.register(Comment)
