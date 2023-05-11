from rest_framework import generics
from rest_framework.views import APIView
from store.models import Product, Configuration, Promotion, Feature
from .serializers import ProductSerializer, ProductDetailSerializer
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.db.models import Q, Max


import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ProductList(APIView):
    def changeToNum(myString):
        myString = myString.replace(' ', '')
        myString = myString[:-1].strip()
        num = myString.split(' ')[0]
        num = "".join(num.split('.'))
        print("number: ", num)
        return int(num)

    def get(self, request, *args, **kwargs):
        detail = request.GET.get('detail')

        if detail != None:
            product = Product.objects.get(ProductID=detail)
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
            config = Configuration.objects.filter(ProdID=detail)
            for item in config:
                temp[item.ConfigName] = item.Detail
            response_data["Configuration"] = temp

            response_data["Promotion"] = Promotion.objects.get(
                ProdID=detail).Detail

            from django.contrib.postgres.search import TrigramSimilarity

            results = Product.objects.filter(
                Q(Type=response_data['Type']) & ~Q(ShopName=response_data['ShopName']))
            results = results.annotate(similarity=TrigramSimilarity(
                'ProductName', response_data['ProductName']),).filter(similarity__gte=0.1).order_by('-similarity')[:20]

            shopmapping = {
                "FPTShop": 0,
                "TGDD": 0,
                "PhongVu": 0,
                "CellPhoneS": 0
            }

            shopresults = {
                "FPTShop": {
                    "ProductLink": "",
                    "SalePrice": "",
                },
                "TGDD": {
                    "ProductLink": "",
                    "SalePrice": "",
                },
                "PhongVu": {
                    "ProductLink": "",
                    "SalePrice": "",
                },
                "CellPhoneS": {
                    "ProductLink": "",
                    "SalePrice": "",
                },
            }

            del shopresults[response_data['ShopName']]
            del shopmapping[response_data['ShopName']]

            for item in results:
                if item.similarity > shopmapping[item.ShopName]:
                    shopmapping[item.ShopName] = item.similarity
                    shopresults[item.ShopName]["ProductLink"] = item.ProductLink
                    shopresults[item.ShopName]["SalePrice"] = item.SalePrice

            # delete shop with no product link
            _shopresults = shopresults.copy()
            for key in _shopresults:
                if _shopresults[key]["ProductLink"] == "" or _shopresults[key]["SalePrice"] == "":
                    del shopresults[key]
                    continue

            response_data['PriceCompare'] = shopresults

            results = {}
            for item in Product.objects.filter(Q(Type=response_data['Type'])):
                relevantRating = 0
                for i in Configuration.objects.filter(ProdID=item.ProductID):
                    if i.ConfigName in response_data['Configuration']:
                        try:
                            vectorizer = TfidfVectorizer()

                            vectors = vectorizer.fit_transform([i.Detail, response_data['Configuration'][i.ConfigName]])
                            relevantRating += cosine_similarity(vectors)[0][1]
                        except ValueError:
                            continue
                results[item.ProductID] = relevantRating

            response_data['ProductRelevant'] = []
            sorted_dict = dict(
                sorted(results.items(), key=lambda item: item[1], reverse=True))
            idx = 1
            for key in sorted_dict:
                if idx > 5:
                    break
                # khong chon cai dau tien boi vi cai dau tien se la san pham dang duoc xem
                if idx > 1:
                    tmp = Product.objects.filter(ProductID=key)
                    response_data['ProductRelevant'].append({
                        "ProductID": key,
                        "ProductName": tmp[0].ProductName,
                        "ProductLink": tmp[0].ProductLink,
                        "ImageLink": tmp[0].ImageLink,
                        "SalePrice": tmp[0].SalePrice,
                        "NormalPrice": tmp[0].NormalPrice,
                    })

                idx += 1
            return Response(response_data, status=status.HTTP_200_OK)

        search = request.GET.get('search')
        if search != None:
            search = " ".join(search.split('+'))
            from django.contrib.postgres.search import TrigramSimilarity
            results = Product.objects.annotate(similarity=TrigramSimilarity(
                'ProductName', search),).filter(similarity__gte=0.2).order_by('-similarity', '-SalePrice')
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
            mapType = {"laptop": "Máy tính cá nhân",
                       "dienthoai": "Điện thoại", "tablet": "Máy tính bảng"}
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
                'doanhnhan': 'Doanh nhân',
                'gaming': 'Gaming',
                'thietkedohoa': 'Thiết kế đồ hoạ',
                'vanphong': 'Văn phòng',
                'hocsinhsinhvien': 'Học sinh - Sinh viên',
            }
            feature = featureMapping[feature]
            for item in dataList:
                tmp = Feature.objects.filter(
                    ProdID=item.ProductID, FeatureName=feature)
                if len(tmp):
                    temp.append(item)
            dataList = temp

        ram = request.GET.get('ram')
        if ram != None:
            temp = []
            for item in dataList:
                tmp = Configuration.objects.filter(
                    ProdID=item.ProductID, ConfigName="RAM")
                if tmp and ram in tmp[0].Detail.lower():
                    temp.append(item)
            dataList = temp

        screen = request.GET.get('screen')
        if screen != None:
            temp = []
            for item in dataList:
                tmp = Configuration.objects.filter(
                    ProdID=item.ProductID, ConfigName="Màn hình")
                if tmp and screen in tmp[0].Detail.lower():
                    temp.append(item)
            dataList = temp

        rom = request.GET.get('rom')
        if rom != None:
            if rom == "1tb":
                rom = "1 tb"
            temp = []
            for item in dataList:
                tmp = Configuration.objects.filter(
                    ProdID=item.ProductID, ConfigName="Lưu trữ")
                if tmp and rom.lower() in tmp[0].Detail.lower():
                    temp.append(item)
            dataList = temp

        price = request.GET.get('price')
        if price != None:
            price = price.split('-')
            price[0] = int(price[0]) * 1000000
            if price[1] != '+':
                price[1] = int(price[1]) * 1000000
            else:
                price[1] = 200000000
            temp = []
            for item in dataList:
                tmp = Product.objects.filter(ProductID=item.ProductID)
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
