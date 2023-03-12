from django.urls import path
from .views import PostsList, PostDetail, NewsCreate, NewsUpdate, PostDelete, SearchList


urlpatterns = [
   path('', PostsList.as_view()),
   # path('search/', PostsList.as_view()),
   path('<int:pk>', PostDetail.as_view()),
   path('search/', SearchList.as_view(), name='search_publications'),
]