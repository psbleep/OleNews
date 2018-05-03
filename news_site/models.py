from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
# from forum.models import Thread


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
    file_upload = models.FileField(
        upload_to="news_site/templates/news_atricles/".format(
            author.get_attname()), null=True
    )
    users_liked = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name='users_liked')

    @property
    def total_likes(self):
        '''
        Return total_likes
        '''
        return self.users_liked.count()

    def get_author_id(self):
        return self.author.id

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
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE,
                             null=True, blank=True, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()

    def __getattr__(self, attribute):
        return getattr(self.user, attribute)

    def __str__(self):
        return 'Comment by "{}" on "{}" is approved {}'.format(self.user,
                                                               self.post,
                                                               self.approved)

    class Meta:
        ordering = ('created',)
