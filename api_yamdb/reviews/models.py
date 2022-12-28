from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils import Choices


class User(AbstractUser):
    ROLE = Choices('user', 'moderator', 'admin')
    role = models.CharField(
        'Пользовательская роль',
        choices=ROLE, default=ROLE.user, max_length=20
    )
    bio = models.TextField('Биография', blank=True)


class Category(models.Model):
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField('Год выпуска')
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )
    genre = models.ManyToManyField(Genre, through='Genre_Title')

    def __str__(self):
        return self.name


class Genre_Title(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='title_genre'
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='genre_title'
    )

    class Meta:
        unique_together = ['title', 'genre']


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        'Рейтинг', blank=True, null=True
     )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
