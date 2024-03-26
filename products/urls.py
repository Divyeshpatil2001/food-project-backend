from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('CategoriesAPI',CategoriesView)
router.register('ProductAPI',ProductView)
router.register('ProductImagesAPI',ProductImagesView)
router.register('menuAPI',MenuView)

urlpatterns = [
    path('',include(router.urls))
]
