from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from news_site.choices import STATUS_CHOICES


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='profile')
    user_bio = models.TextField(default="Fill out your Bio")
    email_consent = models.BooleanField(default=False)
    avitar = models.CharField(choices=STATUS_CHOICES,
                              default="img/avitars/1.jpeg",
                              max_length=200)

    def __str__(self):
        return self.user.username

    def like(self, news_post):
        if news_post.user == self.user:
            return
        try:
            self.news_posts_liked.add(news_post)
        except NewsPost.DoesNotExist:
            pass

    @receiver(post_save, sender=User)
    def create_profile(sender,  instance, created, **kwargs):
        if created:
            # create Profile for user
            p = Profile(user=instance)
            p.save()


class NewsPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             limit_choices_to={'is_staff': True,
                                               'is_active': True},
                             on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    content = models.TextField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    article = models.FileField(upload_to='news_atricles/',
                               default=' ')
    users_liked = models.ManyToManyField(
        Profile, related_name='news_posts_liked', blank=True)

    def likes(self):
        return self.users_liked.count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def full_name(self):
        return "{}, {}".format(self.user.last_name, self.user.first_name)

    class Meta:
        ordering = ['created_on']

        def __unicode__(self):
            return self.title


class Comment(models.Model):
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE,
                             null=True, blank=True, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='user_comments')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True,
                               on_delete=models.CASCADE, related_name='reply')

    def approve(self):
        if not self.approved:
            self.approved = True
            self.save()

    def __getattr__(self, attribute):
        return getattr(self.user, attribute)

    def __str__(self):
        return 'Comment by "{}" on "{}" is approved {}'.format(self.user,
                                                               self.post,
                                                               self.approved)

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False

        return True

    class Meta:
        ordering = ('created',)
