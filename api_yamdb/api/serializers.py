from datetime import datetime
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from reviews.models import (Review, Comment, Category, User, Genre, Title)


class ReviewSerializer(serializers.ModelSerializer):

    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Оценка от 0 до 10!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST' and Review.objects.filter(
            title=title, author=author
        ).exists():
            raise serializers.ValidationError('Вы уже оставили отзыв'
                                              'к этому произведению!')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class UserMeSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    email = serializers.CharField(max_length=254)
    last_name = serializers.CharField(max_length=150)

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'

        )
        model = User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    email = serializers.CharField(max_length=254)

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'

        )
        model = User

    def validate_username(self, username):
        unique_test = User.objects.filter(
            username=username
        ).exists()

        if username == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя'
            )
        if unique_test:
            raise serializers.ValidationError(
                'Имя уже занято'
            )
        return username

    def validate_email(self, email):
        unique_email = User.objects.filter(
            email=email
        ).exists()
        if unique_email:
            raise serializers.ValidationError(
                'Пользователь с таким email уже зарегистрирован'
            )
        return email


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z', max_length=150, required=True
    )

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'username запрещен'
            )
        if User.objects.filter(email=email, username=username).exists():
            return data
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )
        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return data

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z', max_length=150, required=True)
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class TitleSafeSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!')
        return value
