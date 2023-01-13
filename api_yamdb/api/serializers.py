from rest_framework import serializers

from reviews.models import (Review, Comment, Category, User, 
                            Genre, Title, Genre_Title)


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
       
    class Meta:
        fields = '__all__'
        model = Review


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


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    email = serializers.CharField(max_length=254)

    class Meta:
        fields = (
            'username',
            'email'
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


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150, required=True)

    def validate_username(self, username):
        return UserSerializer.validate_username(self, username)

    def validate_email(self, email):
        return UserSerializer.validate_email(self, email)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150, required=True)
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class TitleSafeSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    def get_rating(self, obj):
        return 10


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(many=True, slug_field='slug', queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
