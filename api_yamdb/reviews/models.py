from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator


class RoleChoices(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    role = models.CharField(
        'User role',
        choices=RoleChoices.choices, default=RoleChoices.USER, max_length=20
    )
    bio = models.TextField('Biography', blank=True)
    email = models.EmailField('Email', unique=True)
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
    name = models.CharField('Name', unique=True, max_length=100)
    slug = models.SlugField('Identifier', unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Name', unique=True, max_length=100)
    slug = models.SlugField('Identifier', unique=True)

    class Meta:
        verbose_name = 'Ganre'
        verbose_name_plural = 'Ganres'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Name', max_length=100)
    year = models.PositiveSmallIntegerField(
        'Year of issue',
        validators=[year_validator]
    )
    description = models.TextField('Description', blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', verbose_name='Category',
        blank=True, null=True
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', verbose_name='Ganre'
    )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Product'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='title_genre',
        verbose_name='Product'
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='genre_title',
        verbose_name='Ganre'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'genre'],
                                    name='unique_genre')
        ]
        verbose_name = 'Assigning a work to a genre'
        verbose_name_plural = 'Assigning a works to a genres'


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
        validators=[MinValueValidator(1, 'Rating from 1 to 10'),
                    MaxValueValidator(10, 'Rating from 1 to 10')]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Reviews'
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
        verbose_name = 'Comments'
        ordering = ['id', ]
