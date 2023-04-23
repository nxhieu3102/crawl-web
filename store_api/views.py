from rest_framework import generics
from rest_framework.views import APIView
from store.models import Product, Configuration, Promotion, Feature
from .serializers import ProductSerializer, ProductDetailSerializer
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.db.models import CharField
#from django.db.models.functions import Search

#CharField.register_lookup()

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
    def changeToNum(myString):
        myString = myString.replace(' ', '')
        myString = myString[:-1].strip()
        num = myString.split(' ')[0]
        num = "".join(num.split('.'))
        return int(num)

    def get(self, request, *args, **kwargs):
        detail = request.GET.get('detail')
        if detail != None:
            product = Product.objects.get(ProductID = detail)
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
            config = Configuration.objects.filter(ProdID = detail)
            for item in config:
                temp[item.ConfigName] = item.Detail
            response_data["Configuration"] = temp
            
            response_data["Promotion"] = Promotion.objects.get(ProdID = detail).Detail
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        search = request.GET.get('search')
        if search != None:
            search = " ".join(search.split('+'))
            from django.contrib.postgres.search import TrigramSimilarity
            results = Product.objects.annotate(similarity=TrigramSimilarity('ProductName', search),).filter(similarity__gte=0.1).order_by('-similarity')
            #results = Product.objects.filter(ProductName__search = search)
            dataList = []
            for item in results:
                dataList.append(item)
            serializer = ProductSerializer(dataList, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        dataList = []
        for item in Product.objects.all():
            dataList.append(item)
            
        type = request.GET.get('list')
        if type != None and type != 'all':
            mapType = {"laptop": "Máy tính cá nhân", "dienthoai": "Điện thoại", "tablet": "Máy tính bảng"}
            type = mapType[type]
            temp = []
            for item in dataList:
                if item.Type == type:
                    temp.append(item)
            dataList = temp
                
        brand = request.GET.get('brand')
        if brand != None:
            temp = []
            for item in dataList:
                if item.BrandName == brand.upper():
                    temp.append(item)
            dataList = temp
        
        shop = request.GET.get('shop')
        if shop != None:
            temp = []
            for item in dataList:
                if item.ShopName == shop.upper():
                    temp.append(item)
            dataList = temp
        
        feature = request.GET.get('feature')
        if feature != None:
            temp = []
            featureMapping = {
                'doanhnhan': ['Doanh nghiệp', 'Doanh nhân'],
                'gaming': 'Gaming',
                'thietkedohoa': 'Thiết kế đồ hoạ',
                'vanphong': 'Văn phòng',
                'hocsinhsinhvien': 'Học sinh - Sinh viên',
            }
            feature = featureMapping[feature]
            for item in dataList:
                tmp = Feature.objects.filter(ProdID = item.ProductID, FeatureName = feature)
                if len(tmp):
                    temp.append(item)
            dataList = temp
        
        ram = request.GET.get('ram')
        if ram != None:
            temp = []
            for item in dataList:
                tmp = Configuration.objects.filter(ProdID = item.ProductID, ConfigName = "RAM")
                if tmp and ram in tmp[0].Detail.lower():
                    temp.append(item)
            dataList = temp
            
        screen = request.GET.get('screen')
        if screen != None:
            temp = []
            for item in dataList:
                tmp = Configuration.objects.filter(ProdID = item.ProductID, ConfigName = "Màn hình")
                if tmp and screen in tmp[0].Detail.lower():
                    temp.append(item)
            dataList = temp
                
        rom = request.GET.get('rom')
        if rom != None:
            if rom == "1tb":
                rom = "1 tb"
            temp = []
            for item in dataList:
                tmp = Configuration.objects.filter(ProdID = item.ProductID, ConfigName = "Lưu trữ")
                if tmp and rom.lower() in tmp[0].Detail.lower():
                    temp.append(item)
            dataList = temp

        price = request.GET.get('price')
        if price != None:
            price = price.split('-')
            price[0] = int(price[0]) * 1000000
            if price[1] != '+':
                price[1] = int(price[1]) * 1000000       
            else: price[1] = 200000000
            temp = []
            for item in dataList:
                tmp = Product.objects.filter(ProductID = item.ProductID)
                if tmp and tmp[0].SalePrice and ProductList.changeToNum(tmp[0].SalePrice) >= price[0] and ProductList.changeToNum(tmp[0].SalePrice) <= price[1]:
                    temp.append(item)
            dataList = temp
            print(len(dataList))
                
        if len(dataList):
            serializer = ProductSerializer(dataList, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: 
            response_msg = {
                "error_code": status.HTTP_404_NOT_FOUND,
                "description": "Không tồn tại sản phẩm!"
            }
            return Response(response_msg, status=status.HTTP_200_OK)

# class ProductSearch(APIView):
#     def get(self, request, *args, **kwargs):
#            pass
        
        # ram = request.GET.get('ram')
        # if ram != None:
        #     for item in dataList:
        #         tmp = Configuration.objects.get(ProdID = item.ProductID, ConfigName = "RAM")
        #         if ram not in tmp.Detail.lower():
        #             dataList.remove(item)
        
        # screen = request.GET.get('screen')
        # if screen != None:
        #     screen1 = screen + " inch"
        #     screen2 = screen + "inch"
        #     for item in dataList:
        #         tmp = Configuration.objects.get(ProdID = item.ProductID, ConfigName = "Màn hình")
        #         if not (screen1 in tmp.Detail.lower() or screen2 in tmp.Detail.lower()):
        #             dataList.remove(item)
        # cpu = request.GET.get('ra')
        
        
        
        
        # if tmp == 'lap':
        #     dataList = []
        #     for item in Product.objects.filter(Type = "Máy tính cá nhân"):
        #         dataList.append(item)
        #     serializer = ProductSerializer(dataList, many=True)
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # elif id == 'dienthoai':
        #     dataList = []
        #     for item in Product.objects.filter(Type = "Điện thoại"):
        #         dataList.append(item)
        #     serializer = ProductSerializer(dataList, many=True)
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # elif id == 'tablet':
        #     dataList = []
        #     for item in Product.objects.filter(Type = "Máy tính bảng"):
        #         dataList.append(item)
        #     serializer = ProductSerializer(dataList, many=True)
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # #elif id == 'all'



# class ProductDetail(APIView):
#     def get(self, request, *args, **kwargs):
#         id = self.kwargs['pk']
        
#         product = Product.objects.get(ProductID = id)
#         #serializer = ProductSerializer(product)
#         response_data = {}
#         response_data["ProductName"] = product.ProductName
#         response_data["BrandName"] = product.BrandName
#         response_data["ShopName"] = product.ShopName
#         response_data["ImageLink"] = product.ImageLink
#         response_data["ProductLink"] = product.ProductLink
#         response_data["SalePrice"] = product.SalePrice
#         response_data["NormalPrice"] = product.NormalPrice
#         response_data["Type"] = product.Type
        
#         temp = {}
#         config = Configuration.objects.filter(ProdID = id)
#         for item in config:
#             temp[item.ConfigName] = item.Detail
#         response_data["Configuration"] = temp
        
#         response_data["Promotion"] = Promotion.objects.get(ProdID = id).Detail
        
#         #response_data[]
#         # from django.contrib.postgres.search import TrigramSimilarity
#         # results = Product.objects.annotate(similarity=TrigramSimilarity('ProductName', product.ProductName),).filter(similarity__gte=0.1).order_by('-similarity')
#         # results = Product.objects.filter(ProductName__search=product.ProductName).order_by('SalePrice')[:10]
#         # for item in results:
#         #     if item.ShopName == product.ShopName:
#         #         continue
#         #     response_data["ProdCompare"]["ProductName"] = item.ProductName
#         #     response_data["ProdCompare"]["ProductLink"] = item.ProductLink
#         #     response_data["ProdCompare"]["SalePrice"] = item.SalePrice
        
#         return Response(response_data, status=status.HTTP_200_OK)
    
        
        

        

# class LaptopList(generics.ListCreateAPIView):
#     queryset = Product.objects.filter(Type = 'Máy tính cá nhân')
#     serializer_class = ProductSerializer
    
# class PhoneList(generics.ListCreateAPIView):
#     queryset = Product.objects.filter(Type = 'Điện thoại')
#     serializer_class = ProductSerializer

#class ProductDetail()