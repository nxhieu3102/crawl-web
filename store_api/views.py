from rest_framework import generics
from rest_framework.views import APIView
from store.models import Product, Configuration, Promotion
from .serializers import ProductSerializer, ProductDetailSerializer
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer


# class ProductList(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    
#     def get_queryset(self):
#         slug = self.kwargs['pk']
#         if slug == '1':
#            serializer = ProductSerializer(self.queryset)
#            return Response(serializer.data)
    
    #def query_set(self,)
class ProductList(APIView):
    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        if id == 'all':
            dataList = []
            for item in Product.objects.all():
                dataList.append(item)
            serializer = ProductSerializer(dataList, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif id == 'laptop':
            dataList = []
            for item in Product.objects.filter(Type = "Máy tính cá nhân"):
                dataList.append(item)
            serializer = ProductSerializer(dataList, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif id == 'dienthoai':
            dataList = []
            for item in Product.objects.filter(Type = "Điện thoại"):
                dataList.append(item)
            serializer = ProductSerializer(dataList, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif id == 'tablet':
            dataList = []
            for item in Product.objects.filter(Type = "Máy tính bảng"):
                dataList.append(item)
            serializer = ProductSerializer(dataList, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        #elif id == 'all'



class ProductDetail(APIView):
    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        
        product = Product.objects.get(ProductID = id)
        #serializer = ProductSerializer(product)
        response_data = {}
        response_data["ProductName"] = product.ProductName
        response_data["BrandName"] = product.BrandName
        response_data["ShopName"] = product.ShopName
        response_data["ImageLink"] = product.ImageLink
        response_data["ProductLink"] = product.ProductLink
        response_data["SalePrice"] = product.SalePrice
        response_data["NormalPrice"] = product.NormalPrice
        response_data["Type"] = product.Type
        
        temp = {}
        config = Configuration.objects.filter(ProdID = id)
        for item in config:
            temp[item.ConfigName] = item.Detail
        response_data["Configuration"] = temp
        
        response_data["Promotion"] = Promotion.objects.get(ProdID = id).Detail
        
        #response_data[]
        # from django.contrib.postgres.search import TrigramSimilarity
        # results = Product.objects.annotate(similarity=TrigramSimilarity('ProductName', product.ProductName),).filter(similarity__gte=0.1).order_by('-similarity')
        # results = Product.objects.filter(ProductName__search=product.ProductName).order_by('SalePrice')[:10]
        # for item in results:
        #     if item.ShopName == product.ShopName:
        #         continue
        #     response_data["ProdCompare"]["ProductName"] = item.ProductName
        #     response_data["ProdCompare"]["ProductLink"] = item.ProductLink
        #     response_data["ProdCompare"]["SalePrice"] = item.SalePrice
        
        return Response(response_data, status=status.HTTP_200_OK)
    
        
        

        

# class LaptopList(generics.ListCreateAPIView):
#     queryset = Product.objects.filter(Type = 'Máy tính cá nhân')
#     serializer_class = ProductSerializer
    
# class PhoneList(generics.ListCreateAPIView):
#     queryset = Product.objects.filter(Type = 'Điện thoại')
#     serializer_class = ProductSerializer

#class ProductDetail()