from django.db import models

class Categories(models.Model):
    category_name=models.CharField(max_length=200)
    category_image=models.ImageField(upload_to='categoryimage',blank=True)
    
    def __str__(self):
        return self.category_name   
    
product_rating = [
    (i,i) for i in range(1,6)
]

class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    categories = models.ForeignKey(Categories,on_delete=models.CASCADE)
    price = models.IntegerField()
    recommended = models.BooleanField()
    rating = models.IntegerField(choices=product_rating)
    quantity = models.IntegerField()
    product_image = models.ImageField(upload_to='productimage')
    
    def __str__(self):
        return self.title  
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    multiple_images = models.ImageField(upload_to='productimages')
    
    def __str__(self):
        return self.product.title  
    
    
class Menu(models.Model):
    menu_name = models.CharField(max_length=200)
    select_product = models.ManyToManyField(Product)
    menu_desc = models.TextField()
    availablity = models.BooleanField()
    rating = models.IntegerField(choices=product_rating)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def total_price(self):
        return sum(i.price for i in self.select_product.all())