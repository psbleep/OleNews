from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify


class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    def __getattr__(self, attribute):
        return getattr(self.user, attribute)
    def __str__(self):
        return "{0}, {1}".format(self.last_name, self.first_name)

class NewsPost(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    content = models.TextField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    file_upload = models.FileField(upload_to="templates/",
                                   null=True)

    def get_absolute_url(self):
        return '/news_post_detail/{}/'.format(self.slug)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(NewsPost, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_on']

        def __unicode__(self):
            return self.title


class Comment(models.Model):
    name = models.CharField(max_length=42)
    email = models.EmailField(max_length=75)
    website = models.URLField(max_length=200, null=True, blank=True)
    content = models.TextField()
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
