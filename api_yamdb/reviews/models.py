from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class RoleChoices(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    role = models.CharField(
        'Пользовательская роль',
        choices=RoleChoices.choices, default=RoleChoices.USER, max_length=20
    )
    bio = models.TextField('Биография', blank=True)
    email = models.EmailField('Электронная почта', unique=True)
    confirmation_code = models.CharField(max_length=120, default='')

    class Meta:
        ordering = ['username']

    @property
    def is_admin(self):
        return self.role == RoleChoices.ADMIN

    @property
    def is_moderator(self):
        return self.role == RoleChoices.MODERATOR


class Category(models.Model):
    name = models.CharField('Название', unique=True, max_length=100)
    slug = models.SlugField('Идентификатор', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название', unique=True, max_length=100)
    slug = models.SlugField('Идентификатор', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=100)
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=[MaxValueValidator(timezone.now().year,
                    'Год не может быть больше текущего')]
    )
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', verbose_name='Категория',
        blank=True, null=True
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='title_genre',
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='genre_title',
        verbose_name='Жанр'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'genre'],
                                    name='unique_genre')
        ]
        verbose_name = 'Отнесение произведения к жанру'
        verbose_name_plural = 'Отнесение произведений к жанрам'


class ParentingModel(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Review(ParentingModel):

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1, 'Оценка от 1 до 10'),
                    MaxValueValidator(10, 'Оценка от 1 до 10')]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='one-review-per-title'
            ),
        ]


class Comment(ParentingModel):

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Комментарии'
        ordering = ['id', ]
