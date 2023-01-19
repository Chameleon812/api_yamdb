from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                       UserViewSet, ReviewViewSet, CommentViewSet,
                       signup, get_token)

app_name = 'api'

router = SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register('users', UserViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename='comments'
)

authentication_urls = [
    path('signup/', signup, name='signup'),
    path('token/', get_token, name='token'),
]

urlpatterns = [
    path('v1/auth/', include(authentication_urls)),
    path('v1/', include(router.urls)),
]
