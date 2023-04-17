from rest_framework import generics
from store.models import Product
from .serializers import ProductSerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class LaptopList(generics.ListCreateAPIView):
    queryset = Product.objects.filter(Type = 'Máy tính cá nhân')
    serializer_class = ProductSerializer
    
class PhoneList(generics.ListCreateAPIView):
    queryset = Product.objects.filter(Type = 'Điện thoại')
    serializer_class = ProductSerializer

