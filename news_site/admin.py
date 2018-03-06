from django.contrib import admin
from news_site.models import NewsPost
from news_site.models import Comment
from news_site.models import Author

admin.site.register(Author)
admin.site.register(NewsPost)
admin.site.register(Comment)
