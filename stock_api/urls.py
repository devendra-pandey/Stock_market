from django.urls import include, path
from rest_framework import routers
from .views import TradeViewSet

router = routers.DefaultRouter()
router.register(r'trades', TradeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
