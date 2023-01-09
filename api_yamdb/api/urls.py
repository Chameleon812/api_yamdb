from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import CategoryViewSet, GenreViewSet


app_name = 'api'

router = SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
