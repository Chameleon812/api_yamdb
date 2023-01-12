from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import CategoryViewSet, signup, get_token


app_name = 'api'

router = SimpleRouter()
router.register('categories', CategoryViewSet)

authentication_urls = [
    path('signup/',signup, name='signup'),
    path('token/', get_token, name='token'),
]

urlpatterns = [
    path('v1/auth/', include(authentication_urls)),
    path('v1/', include(router.urls)),
]
