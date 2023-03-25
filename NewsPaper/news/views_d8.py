from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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
        return context

class NewsList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['time_now'] = datetime.utcnow()
        return context



class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class SearchList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'search_page.html'
    context_object_name = 'posts'
    paginate_by = 10

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



class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'ns'
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.post_type = 'at'
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post

    def get_template_names(self):
        post = self.get_object()
        if post.post_type == 'ns':
            self.template_name = 'news_edit.html'
        else:
            self.template_name = 'article_edit.html'
        return self.template_name


class PostDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
