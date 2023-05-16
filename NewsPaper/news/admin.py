from django.contrib import admin
from .models import Post, Author, Category, Comment

# Обнуление рейтинга
def nullfy_rating(modeladmin, request, queryset):
    queryset.update(rating=0)
nullfy_rating.short_description = 'Обнулить рейтинг'


# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с постами
    list_display = ('post_type', 'title', 'preview', 'rating') # генерируем список имён всех полей для более красивого отображения
    list_filter = ('post_type', 'title', 'time_create', 'rating') # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'text_post') # Поля, в которых будет выполняться поиск
    actions = [nullfy_rating]

# Register your models here.

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)