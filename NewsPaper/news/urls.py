from django.urls import path
from .views import PostsList, PostDetail, NewsCreate, PostUpdate, PostDelete, SearchList

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', SearchList.as_view(), name='search_publications'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
]
