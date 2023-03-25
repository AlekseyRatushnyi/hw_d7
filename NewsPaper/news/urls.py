from django.urls import path
from .views import PostsList, PostDetail, NewsCreate, PostUpdate, PostDelete, \
    SearchList, NewsList, NewsDetail, ArticlesList, ArticlesCreate, ArticleDetail

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', SearchList.as_view(), name='search_publications'),
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>', NewsDetail.as_view(), name='post_detail'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/', ArticlesList.as_view(), name='articles_list'),
    path('articles/create/', ArticlesCreate.as_view(), name='article_create'),
    path('articles/<int:pk>', ArticleDetail.as_view(), name='article_detail'),
    path('articles/<int:pk>/update/', PostUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
]



# articles
# urlpatterns = [
#     path('', PostsList.as_view(), name='all_post'),
#     path('<int:pk>', PostDetail.as_view(), name='new'),
#     path('search', SearchList.as_view()),
#     path('create/', ArticleCreate.as_view(), name='article_create'),
#     path('<int:pk>/edit/', PostUpdate.as_view(), name='article_edit'),
#     path('<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
# ]