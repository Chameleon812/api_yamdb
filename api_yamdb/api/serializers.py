from django.shortcuts import get_object_or_404
from django.utils import timezone
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
            raise serializers.ValidationError('Rating from 0 to 10!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST' and Review.objects.filter(
            title=title, author=author
        ).exists():
            raise serializers.ValidationError('You have already left a '
                                              'review for this product!')
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
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
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

        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Invalid name'
            )
        if unique_test:
            raise serializers.ValidationError(
                'Name already taken'
            )
        return username

    def validate_email(self, email):
        unique_email = User.objects.filter(
            email=email
        ).exists()
        if unique_email:
            raise serializers.ValidationError(
                'User with this email is already registered'
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

        if data.get('username').lower() == 'me':
            raise serializers.ValidationError(
                'Username is forbidden'
            )
        if User.objects.filter(email=email, username=username).exists():
            return data
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'A user with this username already exists'
            )
        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'User with this email already exists'
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
        if value > timezone.now().year:
            raise serializers.ValidationError(
                'The year of issue cannot be greater than the current one!')
        return value
