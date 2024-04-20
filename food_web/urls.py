from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls'),name='auth'),
    path('products/',include('products.urls'),name='products'),
    # path('products/',include('products.urls'),name='products'),
    path('orders/',include('Orders.urls'),name='order'),
    path('razorpay/',include("razorpay_backend.api.urls"),name="razorpay"),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
