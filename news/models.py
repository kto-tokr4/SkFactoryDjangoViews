from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    rating = models.IntegerField(default=0, blank=True)

    def update_rating(self):
        new_rating = 0

        posts = self.post_set.all()
        for post in posts:
            new_rating += post.rating * 3
            post_comments = post.comment_set.all()
            for comment in post_comments:
                new_rating += comment.rating

        comments = self.user.comment_set.all()
        for comment in comments:
            new_rating += comment.rating

        self.rating = new_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)


class Post(models.Model):
    TYPE = [
        ('NW', 'News'),
        ('ST', 'State'),
    ]

    title = models.CharField(max_length=256)
    text = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    post_type = models.CharField(max_length=2, choices=TYPE, default='NW')
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'

    def get_absolute_url(self):
        return reverse('news:detail', args=[self.id])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)


class Comment(models.Model):
    text = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
