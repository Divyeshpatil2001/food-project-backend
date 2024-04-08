from django.urls import path,include
from rest_framework.routers import DefaultRouter
from accounts.views import *

router = DefaultRouter()

router.register('RegisterUserAPI',UserViews)


urlpatterns = [
    path('',include(router.urls)),
    path('api-login/',LoginViews.as_view({'post':'login'}),name='user-login'),
    path('refreshtoken/',RefreshTokenView.as_view(),name='refresh-token'),
    path('api-logout/',LogoutViews.as_view({'post':'logout'}),name='user-logout'),
    # path('auth/',include('rest_framework.urls')),
    # path('RegisterUserAPI/logout/', UserViews.as_view({'get': 'logout'}), name='logout'),
]

