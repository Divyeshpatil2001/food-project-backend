from django.shortcuts import render
from rest_framework import viewsets
from .models import Categories,Product,ProductImages,Menu
from .serializer import CategoriesSerializer,ProductSerializer,ProductImagesSerializer,MenuSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import QueryDict

class CategoriesView(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    
class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ProductImagesView(viewsets.ModelViewSet):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImagesSerializer
    
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

    
    
    # def create(self, request, *args, **kwargs):
    #     product_id = request.data["product"]
    #     count = request.data["count"]
    #     print(count)
    #     if Product.objects.filter(id=product_id).exists():
    #         product = Product.objects.get(id=product_id)
    #         product_images = []
    #         for i in range(int(count)):
    #             i = i + 1
    #             print(i)
    #             images_data = request.data['multiple_images_'+str(i)]
    #             product_image = ProductImages.objects.create(
    #             product=product,
    #             multiple_images=images_data
    #             )
    #             product_images.append(product_image)
    #         serializer = ProductImagesSerializer(product_images, many=True)
    #         return Response({'msg':'success','product_images':serializer.data}, status=status.HTTP_201_CREATED)
    #     return Response({'msg':'error'}, status=status.HTTP_201_CREATED)
        
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        