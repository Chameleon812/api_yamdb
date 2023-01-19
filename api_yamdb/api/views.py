import django_filters
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, mixins, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import permission_classes
from rest_framework.decorators import action

from .serializers import (CommentSerializer, ReviewSerializer,
                          CategorySerializer, GenreSerializer,
                          SignUpSerializer, TokenSerializer,
                          TitleSerializer, TitleSafeSerializer,
                          UserSerializer, UserMeSerializer,
                          )
from reviews.models import Review, Title, Category, Genre, User, Comment
from api.permissions import IsAdminOrReadOnly, IsAdmin, IsAdminOrModeratorOrAuthor


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrModeratorOrAuthor,)

    def title_query(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return Review.objects.filter(title=self.title_query().id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.title_query())


class CommentViewSet(ReviewViewSet):
    serializer_class = CommentSerializer

    def review_query(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return Comment.objects.filter(review=self.review_query().id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.review_query())


class ListCreateDeleteViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug',
                                         lookup_expr='icontains')
    genre = django_filters.CharFilter(field_name='genre__slug',
                                      lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    serializer_class = TitleSerializer
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSafeSerializer
        return TitleSerializer


@api_view(['POST'])
@permission_classes([AllowAny, ])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    try:
        user, _ = User.objects.get_or_create(
            username=username,
            email=email,
        )
    except Exception:
        return Response(
            request.data,
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = default_token_generator.make_token(user)
    User.objects.filter(username=username).update(
        confirmation_code=confirmation_code
    )
    send_mail(
        'Регистрация', f'Ваш код подтверждения: {confirmation_code}',
        'admin', [email]
    )
    return Response(
        request.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny, ])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
        user,
        serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response(
            {'token': f'{token}'},
            status=status.HTTP_200_OK
        )
    return Response(
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    permission_classes = [IsAdmin]

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated]
    )
    def me_page(self, request):
        if request.method == 'GET':
            serializer = UserMeSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            serializer = UserMeSerializer(
                request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(role=request.user.role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
