from news_site.models import NewsPost
from django.test import TestCase

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class NewsPostTestCase(TestCase):
    def create_news_post(self, title='Hello World', slug='hello-world',
                         content='Hello World, what more is there to say?',
                         author='Test Author'):
        print("Creating Test NewsPost")
        return NewsPost(title=title, slug=slug, content=content, author=author)

    def test_news_post_author_url(self):
        news_post = self.create_news_post()
        url = '/articles/{0}'.format(news_post.author)
        print("Asserting Url Creation")
        print(url.replace(' ', '%'))
        response = self.client.get(url.replace(' ', '%'), follow=True)
        print(response.status_code)
        self.assertEqual(response.status_code,200)

    def test_news_post_creation(self):
        news_post = self.create_news_post()
        print("Asserting Title")
        self.assertEqual(news_post.title, 'Hello World')

    def test_save_slugify_when_no_slug(self):
        news_post = self.create_news_post(slug=None)
        news_post.save()
        print("Asserting Slug")
        self.assertEqual(news_post.slug, 'hello-world')

    def test_save_retains_values(self):
        news_post = self.create_news_post()
        news_post.content = 'Changed Content'
        news_post.save()
        print("Asserting Changed Content")
        self.assertEqual(news_post.content, 'Changed Content')

    def test_get_absolute_url(self):
        news_post = self.create_news_post()
        print("Asserting URL")
        self.assertEqual(news_post.get_absolute_url(),
                         '/news_post_detail/hello-world/')

    def test_get_absolute_url_no_slug(self):
        news_post = self.create_news_post(slug=None)
        print("Asserting Slug Constructor")
        self.assertEqual(news_post.get_absolute_url(),
                         '/news_post_detail/None/')
