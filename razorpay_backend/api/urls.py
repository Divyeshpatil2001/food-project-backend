from django.urls import path
from .api_razorpay import CreateOrderAPIView,TransactionAPIView

urlpatterns = [
    path("order/create/",CreateOrderAPIView.as_view(),name="create-order-api"),
    path("order/complete/",TransactionAPIView.as_view(),name="complete-order-api"),
    
]
