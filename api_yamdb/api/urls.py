from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import CategoryViewSet


app_name = 'api'

router = SimpleRouter()
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
