from django.contrib import admin
from .models import Categories,Product,ProductImages,Menu
# Register your models here.
admin.site.register(Categories)


admin.site.register(Product)
admin.site.register(ProductImages)

admin.site.register(Menu)