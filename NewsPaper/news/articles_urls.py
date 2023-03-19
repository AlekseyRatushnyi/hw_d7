from django.urls import path
from .views import PostsList, PostDetail, SearchList, ArticleCreate, PostUpdate, PostDelete

urlpatterns = [
    path('', PostsList.as_view(), name='all_post'),
    path('<int:pk>', PostDetail.as_view(), name='new'),
    path('search', SearchList.as_view()),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='article_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
]
