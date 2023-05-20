from datetime import datetime
import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404, render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy, resolve
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.core.cache import cache
from .tasks import new_post_subscription
import pytz


class PostsList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['time_now'] = datetime.utcnow()
        # context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('post_list')



class NewsList(ListView):
    model = Post
    queryset = Post.objects.filter(post_type='ns')
    ordering = '-time_create'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['time_now'] = datetime.utcnow()
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('news_list')

class ArticlesList(ListView):
    model = Post
    queryset = Post.objects.filter(post_type='at')
    ordering = '-time_create'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['time_now'] = datetime.utcnow()
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('articles_list')

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f"post-{self.kwargs['pk']}", None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f"post-{self.kwargs['pk']}", obj)

        return obj


class NewsDetail(DetailView):
    model = Post
    # template_name = 'post.html'
    context_object_name = 'post'

    def get_template_names(self):
        post = self.get_object()
        if post.post_type == 'ns':
            self.template_name = 'post.html'
        elif post.post_type == 'at':
            self.template_name = 'errornews.html'
        else:
            self.template_name = 'page404.html'
        return self.template_name


class ArticleDetail(DetailView):
    model = Post
    # template_name = 'post.html'
    context_object_name = 'post'

    def get_template_names(self):
        post = self.get_object()
        if post.post_type == 'at':
            self.template_name = 'post.html'
        elif post.post_type == 'ns':
            self.template_name = 'errornews.html'
        else:
            self.template_name = 'page404.html'
        return self.template_name


class SearchList(ListView):
    model = Post
    template_name = 'search_page.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        return context


class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'ns'
        news.author = Author.objects.get(user_id=self.request.user.id)
        news.save()
        new_post_subscription.apply_async([news.pk])
        return super().form_valid(form)


class ArticlesCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    success_url = reverse_lazy('articles_list')

    def form_valid(self, form):
        article = form.save(commit=False)
        article.post_type = 'at'
        article.author = Author.objects.get(user_id=self.request.user.id)
        article.save()
        new_post_subscription.apply_async([article.pk])
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    success_url = reverse_lazy('post_list')

    def get_template_names(self):
        post = self.get_object()
        if post.post_type == 'ns':
            self.template_name = 'news_edit.html'
        elif post.post_type == 'at':
            self.template_name = 'article_edit.html'
        else:
            self.template_name = 'page404.html'
        return self.template_name


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/news')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-time_create')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей по выбранной категории: '
    return render(request, 'subscribe.html', {'category': category, 'message': message})


logger = logging.getLogger(__name__)


def index_log(request):
    logger.error("Test!!!")
    return HttpResponse("Hello, it's a log!!!")


class IndexTranslate(View):
    def get(self, request):
        # . Translators: This message appears on the home page only
        models = Category.objects.all()

        context = {
            'models': models,
        }

        return HttpResponse(render(request, 'indextranslate.html', context))


class IndexTime(View):
    def get(self, request):
        context = {'time': timezone.now(), 'timezones': pytz.common_timezones}

        return HttpResponse(render(request, 'indextime.html', context))

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')

