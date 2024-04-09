from rest_framework import serializers
from .models import Categories,Product,ProductImages,Menu

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'
        
# class MenuSerializer(serializers.ModelSerializer):
#     # select_product = serializers.ListField(child=serializers.IntegerField(),write_only=True)
#     # select_product = serializers.IntegerField()
#     # select_product = serializers.PrimaryKeyRelatedField(many=True,queryset=Product.objects.all(),write_only=True)
#     select_product = serializers.ListField(child=serializers.IntegerField(),write_only=True)

#     total_price = serializers.SerializerMethodField()
    
#     def get_total_price(self,i):
#         return i.total_price()
    
#     class Meta:
#         model = Menu
#         fields = '__all__'
        
    
class MenuSerializer(serializers.ModelSerializer):
    select_product = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Menu
        fields = '__all__'

    def create(self, validated_data):
        select_product_data = validated_data.pop('select_product', [])
        menu = Menu.objects.create(**validated_data)
        menu.select_product.set(select_product_data)
        menu.total_price = menu.calculate_total_price()
        menu.save()
        return menu

    def get_total_price(self, instance):
        return instance.total_price  
        
    # def create(self, validated_data):
    #     print()
    #     print(validated_data)
        # images_data = validated_data.pop('multiple_images')  
        # product = validated_data.get('product')
        # product_images = []
        # for image_data in images_data:
        #     product_image = ProductImages.objects.create(
        #         product=product,
        #         multiple_images=image_data
        #     )
        #     product_images.append(product_image)

        # return product_images
        # return []
        
        
        
# class ProductImagesSerializer(serializers.ModelSerializer):
    
#     multiple_images = serializers.ListField(child=serializers.ImageField(), required=True)

#     class Meta:
#         model = ProductImages
#         fields = ['product', 'multiple_images']  

#     def create(self, validated_data):
#         images_data = validated_data.pop('multiple_images')  
#         product = validated_data.get('product')

#         product_images = []
#         for image_data in images_data:
#             product_image = ProductImages.objects.create(
#                 product=product,
#                 multiple_images=image_data
#             )
#             product_images.append(product_image)

#         return product_images
        
# class ProductImagesSerializer(serializers.Serializer):
#     product = serializers.IntegerField()
#     count = serializers.IntegerField()
#     print(product)
    # multiple_images = serializers.ListField(child=serializers.ImageField())

    # def create(self, validated_data):
        # images_data = validated_data.get('multiple_images')
        # product_id = validated_data.get('product')
        # image_count = validated_data.get('count')
        # product = Product.objects.get(pk=product_id)
        # product_images = []
        # for i in range(image_count):
        #     images_data = validated_data.get('multiple_images_'+i+1)
        #     product_image = ProductImages.objects.create(
        #         product=product,
        #         multiple_images=images_data
        #     )
        #     product_images.append(product_image)
        # return product_images  
            
        # try:
        #     product = Product.objects.get(pk=product_id)
        # except Product.DoesNotExist:
        #     raise serializers.ValidationError("Product does not exist")

        # product_images = []
        # for image_data in images_data:
        #     print(image_data)
        #     product_image = ProductImages.objects.create(
        #         product=product,
        #         multiple_images=image_data
        #     )
        #     product_images.append(product_image)

        # return product_images   
    
        
        
        
# class ProductImagesSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = ProductImages
#         fields = '__all__'
        
#     def create(self, validated_data):
#         images_data = self.context['request'].FILES.getlist('multiple_images')
#         product = validated_data.get('product')

#         product_images = []
#         for image_data in images_data:
#             product_image = ProductImages.objects.create(
#                 product=product,
#                 multiple_images=image_data
#             )
#             product_images.append(product_image)

#         return product_images
#     def create(self, validated_data):
#         images_data = validated_data.pop('multiple_images')
#         product_images = []
#         for image_data in images_data:
#             product_image = ProductImages.objects.create(
#                 multiple_images=image_data, **validated_data
#             )
#             product_images.append(product_image)
#         return product_images


# class ProductImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductImages
#         fields = ['id', 'multiple_images']

# class ProductImagesSerializer(serializers.ModelSerializer):
#     multiple_images = ProductImageSerializer(many=True)

#     class Meta:
#         model = ProductImages
#         fields = '__all__'
        # fields = ['product', 'multiple_images']

    # def create(self, validated_data):
        # images_data = validated_data.pop('multiple_images')
        # print(self.request.data)
        # product = validated_data.pop('product')
        # product_images = []
        # for image_data in images_data:
        #     product_image = ProductImages.objects.create(
        #         product=product, multiple_images=image_data['multiple_images']
        #     )
        #     product_images.append(product_image)
        # return product_images