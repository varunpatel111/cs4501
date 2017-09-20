from rest_framework import routers
from marketplace.views import CustomUserViewSet

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)