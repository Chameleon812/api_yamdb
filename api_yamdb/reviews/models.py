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
    email = models.EmailField('Электронная почта', unique=True)


class Category(models.Model):
    name = models.CharField('Название', unique=True, max_length=100)
    slug = models.SlugField('Идентификатор', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название', unique=True, max_length=100)
    slug = models.SlugField('Идентификатор', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=100)
    year = models.PositiveSmallIntegerField('Год выпуска')
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', verbose_name='Категория',
        blank=True, null=True
    )
    genre = models.ManyToManyField(
        Genre, through='Genre_Title', verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Genre_Title(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='title_genre',
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='genre_title',
        verbose_name='Жанр'
    )

    class Meta:
        unique_together = ['title', 'genre']
        verbose_name = 'Отнесение произведения к жанру'
        verbose_name_plural = 'Отнесение произведений к жанрам'


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        'Рейтинг', blank=True, null=True
     )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self) -> str:
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text[:15]
