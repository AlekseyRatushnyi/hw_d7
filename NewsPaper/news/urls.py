from django.urls import path

from . import views
from .views import PostsList, PostDetail, NewsCreate, PostUpdate, PostDelete, \
    SearchList, NewsList, NewsDetail, ArticlesList, ArticlesCreate, ArticleDetail, upgrade_me, CategoryListView, \
    subscribe, index_log, IndexTranslate, IndexTime

from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    # path('', cache_page(60)(PostsList.as_view()), name='post_list'), При кешировании
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', SearchList.as_view(), name='search_publications'),
    path('news/', cache_page(60*5)(NewsList.as_view()), name='news_list'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>', NewsDetail.as_view(), name='post_detail'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/', cache_page(60*5)(ArticlesList.as_view()), name='articles_list'),
    path('articles/create/', ArticlesCreate.as_view(), name='article_create'),
    path('articles/<int:pk>', ArticleDetail.as_view(), name='article_detail'),
    path('articles/<int:pk>/update/', PostUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('log/', views.index_log, name='index_log'),
    path('translate/', IndexTranslate.as_view(), name='translate'),
    path('time/', IndexTime.as_view(), name='time'),
]

