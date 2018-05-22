from news_site.models import NewsPost, Profile, Comment
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

'''
Common Use Functions
'''
def create_new_test_user():
    return User.objects.create(username='new_user',
                               email='new_user@host.com',
                               password='new_user_password')

def create_new_test_author(user=None):
    if user is None:
        user = create_new_test_user()
    user.is_staff = True
    user.save()
    return user

def create_test_news_post(title='Hello World', slug='hello-world',
                          content='Hello World, what more is there to say?',
                          user=None):
    user = user or create_new_test_user()
    news_post = NewsPost.objects.create(
        title=title, slug=slug, content=content, user=user)
    return news_post
'''
Test Cases
'''

class ArticlesListViewTests(TestCase):
    def test_articles_list_with_no_articles(self):
        response = self.client.get(reverse('articles_list'))
        self.assertContains(response, 'No articles')

    def test_articles_list_with_articles(self):
        author = create_new_test_author()
        article = create_test_news_post(user=author)
        article2 = create_test_news_post(user=author, slug='article2')
        response = self.client.get(reverse('articles_list'))
        self.assertContains(response, article.title)
        self.assertContains(response, article2.title)

'''
class UserTestCase(TestCase):
    def setup(self):
        User.objects.create(username='new_user',
                           email='new_user@host.com',
                           password='new_user_password')

    def test_user_profile_creaton(self):
        user = User.objects.get(username='new_user')
        profile = Profile.objects.get(user=user)
        self.assertEqual(user.profile, profile)





class ProfileTestCase(TestCase):

    def test_profile_is_created_for_new_user(self):
        create_new_test_user()
        self.assertEqual(Profile.objects.count(), 1)

    def test_new_profile_is_not_created_when_saving_existing_user(self):
        user = create_new_test_user()
        user.username = 'updated_user'
        user.save()
        self.assertEqual(Profile.objects.count(), 1)

    def test_like_news_post(self):
        user = create_new_test_user()
        user2 = create_new_test_user(username='test2')
        news_post = create_test_news_post(user=user)
        user2.profile.like(news_post)
        # Must be a better way to test queryset results
        self.assertEqual(user2.profile.news_posts_liked.count(), 1)
        self.assertEqual(user2.profile.news_posts_liked.all()[0], news_post)

    def test_like_news_post_that_does_not_exist(self):
        user = create_new_test_user()
        with self.assertRaises(AttributeError) as e:
            user.profile.like(None)
        self.assertTrue(e)
        self.assertEqual(user.profile.news_posts_liked.count(), 0)

    def test_like_your_own_news_post(self):
        user = create_new_test_user()
        news_post = create_test_news_post(user=user)
        user.profile.like(news_post)
        self.assertEqual(user.profile.news_posts_liked.count(), 0)

    def test_like_same_post_more_than_once(self):
        user = create_new_test_user()
        user2 = create_new_test_user(username='test2')
        news_post = create_test_news_post(user=user)
        user2.profile.news_posts_liked.add(news_post)
        user2.profile.like(news_post)
        self.assertEqual(user2.profile.news_posts_liked.count(), 1)


class NewsPostTestCase(TestCase):

    def test_likes_with_no_likes(self):
        news_post = create_test_news_post()
        self.assertEqual(news_post.likes, 0)

    def test_likes_with_likes(self):
        user = create_new_test_user()
        user2 = create_new_test_user(username='test2')
        news_post = create_test_news_post(user=user)
        news_post.users_liked.add(user2.profile)
        self.assertEqual(news_post.likes, 1)

    def test_save_with_existing_slug_retains_slug(self):
        news_post = create_test_news_post()
        news_post.save()
        self.assertEqual(news_post.slug, 'hello-world')

    def test_save_without_slug_creates_slug(self):
        news_post = create_test_news_post(slug=None)
        news_post.save()
        self.assertEqual(news_post.slug, 'hello-world')


class CommentTestCase(TestCase):

    def create_test_comment(self):
        news_post = create_test_news_post()
        user2 = create_new_test_user(username='test2')
        return Comment.objects.create(post=news_post, user=user2,
                                      content='hello world')

    def test_approve_on_not_yet_approved_comment(self):
        comment = self.create_test_comment()
        comment.approve()
        self.assertTrue(comment.approved)

    def test_approve_on_alredy_approved_comment(self):
        comment = self.create_test_comment()
        comment.approved = True
        comment.save()
        comment.approve()


class AuthorsListViewTests(TestCase):

    def test_authors_list_no_authors(self):
        response = self.client.get(reverse('authors_list'))
        self.assertContains(response, 'No authors here!')

    def test_authors_list_with_authors(self):
        author = create_new_test_author()
        author2 = create_new_test_author(
            create_new_test_user(username='test2'))
        response = self.client.get(reverse('authors_list'))
        self.assertContains(response, author.username)
        self.assertContains(response, author2.username)

    def test_authors_list_non_author_users_do_not_get_listed(self):
        non_author = create_new_test_user()
        author = create_new_test_author(
            create_new_test_user(username='test_author'))
        response = self.client.get(reverse('authors_list'))
        self.assertContains(response, author.username)
        self.assertNotContains(response, non_author.username)


class AuthorDeatilViewTests(TestCase):

    def test_author_view_user_exists_and_is_author(self):
        author = create_new_test_author()
        response = self.client.get(reverse('author', kwargs={'pk': author.id}))
        self.assertContains(response, author.username)

    def test_author_view_user_does_not_exist(self):
        response = self.client.get(reverse('author', kwargs={'pk': 123456}))
        self.assertEquals(response.status_code, 404)

    def test_author_view_user_exists_but_is_not_author(self):
        non_author = create_new_test_user()
        response = self.client.get(
            reverse('author', kwargs={'pk': non_author.id}))
        self.assertEquals(response.status_code, 404)


class AuthorArticlesViewTests(TestCase):

    def test_author_articles_without_articles(self):
        author = create_new_test_author()
        response = self.client.get(
            reverse('author_articles', kwargs={'pk': author.id}))
        self.assertContains(response, 'no articles')

    def test_author_articles_with_articles(self):
        author = create_new_test_author()
        article = create_test_news_post(user=author)
        article2 = create_test_news_post(user=author, slug='article2')
        response = self.client.get(
            reverse('author_articles', kwargs={'pk': author.id}))
        self.assertContains(response, article.title)
        self.assertContains(response, article2.title)

'''
