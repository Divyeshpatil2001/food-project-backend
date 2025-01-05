from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action

from .models import Orders
from .serializer import OrderSerializer

class OrdersViewSets(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Orders.objects.all()
        elif user.is_authenticated:
            return Orders.objects.filter(user=user)
        else:
            raise PermissionDenied("You must be logged in to access this resource.")
   
    def perform_create(self, serializer):
        # Automatically assign the logged-in user
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.user:
            raise PermissionDenied("You are not allowed to delete this order.")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
