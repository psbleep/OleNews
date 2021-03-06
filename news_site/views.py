from .models import NewsPost, Profile
from .forms import CommentForm, UserChange, UserChangeProfile,SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import authenticate, login
from django.views.generic import FormView


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
    model = User
    template_name = "user_profile.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        print(request.user.profile)
        if request.user.profile is None:
            p = Profile(user=request.user)
            p.save()
        return self.render_to_response(context)


def user_settings(request, pk):
    if request.method == 'POST':
        user_change_form = UserChange(request.POST,
                                      instance=request.user)
        user_change_profile_form = UserChangeProfile(request.POST,
                                                     instance=request.user.profile)
        if user_change_form.is_valid():
            user_change_form.save()
            print(request.user.profile.avitar)

        if user_change_profile_form.is_valid():
            user_change_profile_form.save()

        return HttpResponseRedirect('/users/{}/'.format(request.user.id))

    else:
        user_change_form = UserChange(instance=request.user)
        user_change_profile_form = UserChangeProfile(instance=request.user.profile)
        return render(request, 'user_pages/user_settings.html', {
            'form': user_change_form,
            'form2': user_change_profile_form,
            })


class UserSignupView(FormView):
    form_class = SignUpForm
    template_name = 'registration/sign_up.html'

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        # save the new user first
        form.save()
        # get the username and password
        username = self.request.POST['username']
        password = self.request.POST['password1']
        # authenticate user then login
        user = authenticate(username=username, password=password)

        login(self.request, user)
        return super(UserSignupView, self).form_valid(form)


class LikeArticleView(generic.DetailView):
    model = NewsPost

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.request.user.profile.like(self.object)
        return HttpResponseRedirect(
            reverse('article', kwargs={'pk': self.object.id}))


class PasswordChangeView(PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('home')
