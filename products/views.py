from django.shortcuts import render
from rest_framework import viewsets
from .models import Categories,Product,ProductImages,Menu
from .serializer import CategoriesSerializer,ProductSerializer,ProductImagesSerializer,MenuSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import QueryDict
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

class CategoriesView(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
class ProductImagesView(viewsets.ModelViewSet):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImagesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def list(self, request):
        product_id = request.query_params.get('product')
        if product_id:
            queryset = self.queryset.filter(product_id=product_id)
        else:
            queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        print(request.data)
        data = request.data.getlist('multiple_images')
        pid = request.data['product']
        print("**")
        print(data)
        res = []
        for i in data:
            values = {'product': pid,'multiple_images': i}
            query_dict = QueryDict('', mutable=True)
            query_dict.update(values)
            print(query_dict)
            serializer = ProductImagesSerializer(data=query_dict)
            if serializer.is_valid():
                serializer.save()
                res.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_201_CREATED)
        
        
class MenuView(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [JWTAuthentication]

    
    
  
        