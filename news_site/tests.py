from news_site.models import NewsPost, Author
from django.test import TestCase
from django.contrib.auth.models import User


class NewsPostTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            'tauthor', 'test@author.com', 'tauthorpass',
            first_name='Test', last_name='Author')
        self.author = Author.objects.create(user=user)

    def create_news_post(self, title='Hello World', slug='hello-world',
                         content='Hello World, what more is there to say?',
                         author=None):
        print("Creating Test NewsPost")
        author = author or self.author
        return NewsPost(title=title, slug=slug, content=content,
                        author=author)

    def test_news_post_author_url(self):
        news_post = self.create_news_post()
        url = '/articles/{}'.format(news_post.author.id)
        print("Asserting Url Creation")
        print(url.replace(' ', '%'))
        response = self.client.get(url.replace(' ', '%'), follow=True)
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

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


class UserSignupTestCase(TestCase):

    def test_user_gets_created(self):
        response = self.client.post(
            '/signup/',
            {'username': 'tauthor',
             'email': 'test@author.com',
             'password1': 'setec_astronomy',
             'password2': 'setec_astronomy',
             'first_name': 'Test',
             'last_name': 'Author'}
        )
        self.assertEqual(response.status_code, 201)
        test_user = User.objects.first()
        self.assertEqual(test_user.username, 'tauthor')

    def test_sign_up_passwords_do_not_match(self):
        response = self.client.post(
            '/signup/',
            {'username': 'tauthor',
             'email': 'test@author.com',
             'password1': 'setec_astronomy',
             'password2': 'other_astronomy',
             'first_name': 'Test',
             'last_name': 'Author'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('The two password fields didn&#39;t match',
                      response.content.decode())

    def test_sign_up_username_already_exists(self):
        user = User.objects.create_user('tauthor', 'test@author.com',
                                        'setec_astronomy')
        user.save()
        response = self.client.post(
            '/signup/',
            {'username': 'tauthor',
             'email': 'test@author.com',
             'password1': 'setec_astronomy',
             'password2': 'setec_astronomy',
             'first_name': 'Test',
             'last_name': 'Author'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('A user with that username already exists',
                      response.content.decode())

    def test_sign_up_email_already_exists(self):
        user = User.objects.create_user('first_author', 'test@author.com',
                                        'setec_astronomy')
        user.save()
        response = self.client.post(
            '/signup/',
            {'username': 'tauthor',
             'email': 'test@author.com',
             'password1': 'setec_astronomy',
             'password2': 'setec_astronomy',
             'first_name': 'Test',
             'last_name': 'Author'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('A user with that email already exists',
                      response.content.decode())
