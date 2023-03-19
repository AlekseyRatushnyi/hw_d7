from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),
   # Делаем так, чтобы все адреса из нашего приложения (simpleapp/urls.py)
   # подключались к главному приложению с префиксом products/.
   path('news/', include('news.urls')),
   path('articles/', include('news.articles_urls')),
   path('', include('protect.urls')),
   path('sign/', include('sign.urls')),
]