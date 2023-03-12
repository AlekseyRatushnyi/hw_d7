from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Avg, Count, Min, Sum
from django.urls import reverse

sport = 'sp'
policy = 'py'
education = 'ed'
world = 'wd'
economy = 'ec'
health = 'hh'
tech = 'th'
news = 'ns'
article = 'at'

list_category = [
    (sport, 'Спорт'),
    (policy, 'Политика'),
    (education, 'Образование'),
    (world, 'Мир'),
    (economy, 'Экономика'),
    (health, 'Здоровье'),
    (tech, 'Технологии'),

]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)

    def update_rating(self):
        posts_author = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum']
        s1 = 0 if not posts_author else posts_author
        comments_author = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        s2 = 0 if not comments_author else comments_author
        comments_others = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rating'))['rating__sum']
        s3 = 0 if not comments_others else comments_others
        self.rating = s1 * 3 + s2 + s3
        self.save()

    def mfoo(self):
        print(self.user)

class Category(models.Model):
    category = models.CharField(max_length=2, choices=list_category, unique=True)


class Post(models.Model):
    list_type = [(news, 'Новости'), (article, 'Статья')]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=list_type)
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=50)
    text_post = models.TextField()
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text_post[:124]}...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


