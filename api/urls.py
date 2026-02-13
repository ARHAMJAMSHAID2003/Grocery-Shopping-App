
## to make our endpoints accessible from views
# we define url endpoints here
from django.urls import path, include
# path is used to define url patterns

from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, UserViewSet, CartViewSet, OrderViewSet,
    OrderItemsViewSet, StoresViewSet, LocationsViewSet, register, login,
    send_otp, verify_otp, resend_otp
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'users', UserViewSet)
router.register(r'cart', CartViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemsViewSet)
router.register(r'stores', StoresViewSet)
router.register(r'locations', LocationsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('send-otp/', send_otp, name='send-otp'),
    path('verify-otp/', verify_otp, name='verify-otp'),
    path('resend-otp/', resend_otp, name='resend-otp'),
]