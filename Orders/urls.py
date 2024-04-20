from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import OrdersViewSets

router = DefaultRouter()
router.register('OrdersAPI',OrdersViewSets)
urlpatterns = [
    path('',include(router.urls))
]
