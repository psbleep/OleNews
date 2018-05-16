from .models import NewsPost, Profile
from .forms import CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic


def home(request):
    return render(request, 'home.html', {'page': 'home'})


class AuthorsListView(generic.ListView):
    model = Profile
    template_name = "authors_list.html"

    def get_queryset(self):
        return Profile.objects.filter(user__is_staff=True)


class AuthorDetailView(generic.DetailView):
    model = Profile
    template_name = "author.html"

    def get_object(self, **kwargs):
        obj = super().get_object(**kwargs)
        if not obj.user.is_staff:
            raise Http404
        obj.articles = NewsPost.objects.filter(user=obj.user)
        return obj


class AuthorArticlesView(generic.DetailView):
    model = Profile
    template_name = "author_articles.html"

    def get_object(self, **kwargs):
        obj = super().get_object(**kwargs)
        obj.articles = obj.user.newspost_set.all()
        return obj


class ArticlesListView(generic.ListView):
    model = NewsPost
    template_name = "articles_list.html"


class ArticleDetailView(LoginRequiredMixin, generic.DetailView):
    model = NewsPost
    template_name = "article.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.object.id
        user_pk = self.request.user.id
        form = CommentForm(post_pk=post_pk, user_pk=user_pk)
        context.update({'form': form})
        return context


class CreateCommentView(LoginRequiredMixin, generic.CreateView):
    form_class = CommentForm
    template_name = 'create_comment.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['post_pk'] = self.kwargs.get('pk')
        kwargs['user_pk'] = self.request.user.id
        return kwargs

    def get_success_url(self):
        return reverse('article', kwargs={'pk': self.object.post.id})


class UserProfileView(generic.DetailView):
    model = Profile
    template_name = "user_profile.html"


class UserProfileSettingsView(LoginRequiredMixin, generic.UpdateView):
    model = Profile
    fields = ['user_bio']

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id != kwargs.get('pk'):
            return reverse('home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('user_profile', kwargs={'pk': self.object.id})


class UserSignupView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/sign_up.html'

    def get_success_url(self):
        return reverse('home')


class LikeArticleView(generic.DetailView):
    model = NewsPost

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.request.user.profile.like(self.object)
        return HttpResponseRedirect(
            reverse('article', kwargs={'pk': self.object.id}))
