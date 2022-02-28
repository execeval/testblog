from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Preference(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    value = models.TextField(null=False, blank=True)

    def __str__(self):
        return f'{self.name} : {self.value}'


class Limit(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    value = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return f'{self.name} : {self.value}'


class PostCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.SlugField(max_length=40, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(UserModel, on_delete=models.PROTECT, null=False, blank=False)
    categories = models.ManyToManyField(PostCategory, blank=True, default=[])

    title = models.CharField(null=False, blank=False, max_length=200)
    content = models.TextField(null=False, blank=False)

    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    is_active = models.BooleanField(null=False, default=True)

    def __str__(self):
        return f'Post "{self.title}" by {self.author.username} at {self.date.date()}'

    class Meta:
        ordering = ['-date']


class PostComment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(UserModel, on_delete=models.PROTECT, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.PROTECT, null=False, blank=False)

    content = models.TextField(null=False, blank=False)


class PostReaction(models.Model):
    REACTION_CHOICES = [
        ('+', 'Like'),
        ('-', 'Dislike'),
    ]

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(UserModel, on_delete=models.PROTECT, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.PROTECT, null=False, blank=False)

    reaction = models.CharField(max_length=1, choices=REACTION_CHOICES, null=False, blank=False)

    class Meta:
        unique_together = ('author', 'post')
